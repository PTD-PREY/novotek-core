# -*- coding: utf-8 -*-
import json
import os
import re
import shutil
import ast

default_folder_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../ignition-data/projects/Novotek-core'
)

# Folders whose exports we should skip (but we still ensure __init__.py exists)
EXPORT_EXCLUDE_DIRS = {'tests', '__pycache__'}

def remove_extracted_scripts(folder_path):
    try:
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in dirs:
                    if name == 'extracted_scripts':
                        folder_to_remove = os.path.join(root, name)
                        shutil.rmtree(folder_to_remove)
                        print(f"Removed folder: {folder_to_remove}")
        else:
            print(f"{folder_path} is not a valid directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# --- Heuristics to avoid saving plain text as code ----------------------------

SKIP_TEXT_KEYS = {
    'custom', 'label', 'title', 'description', 'tooltip',
    'text', 'message', 'placeholder', 'hint'
}

def last_key_segment(path_key):
    if not path_key:
        return ''
    return path_key.split('_')[-1].lower()

def is_probably_code(s):
    if not isinstance(s, str):
        return False
    t = s.strip()
    if not t:
        return False
    if '\n' not in t and len(t) < 10 and not re.search(r'[;{}()=<>]|==|===|!=|:=', t):
        return False
    patterns = [
        r'\bdef\b', r'\breturn\b', r'\bclass\b', r'\bimport\b', r'\bfrom\b.+\bimport\b',
        r'\bfunction\b', r'\basync\b', r'\bawait\b', r'\btry\b.*\bexcept\b', r'\bcatch\b',
        r'\bvar\b', r'\blet\b', r'\bconst\b',
        r'=>', r';', r'\{', r'\}', r'\bif\s*\(', r'\bfor\s*\(', r'\bwhile\s*\(',
        r'\)\s*=>', r'==|===|!=|<=|>=|:=', r'\bnew\s+[A-Za-z_]\w*', r'system\.'
    ]
    for p in patterns:
        if re.search(p, t):
            return True
    indented_lines = sum(1 for line in t.splitlines() if line.startswith(('  ', '\t')))
    if indented_lines >= 2:
        return True
    return False

# --- Sorting only dict keys (do not sort lists) -------------------------------

def sort_keys_recursive(obj):
    if isinstance(obj, dict):
        return {k: sort_keys_recursive(v) for k, v in sorted(obj.items(), key=lambda kv: kv[0])}
    elif isinstance(obj, list):
        return [sort_keys_recursive(item) for item in obj]
    else:
        return obj

# --- Resource cleaners ---------------------------------------------------------

def resource_clean(input_file):
    template_resource = [
        (r'"actor": ".*?"', '"actor": "system"'),
        (r'"timestamp": ".*?"', '"timestamp": "2022-01-01T00:00:00Z"'),
        (r'"lastModificationSignature": ".*?"',
         '"lastModificationSignature": "4a15e0122c9a955ca05b407bd9fa06810c1a05bd02f35e6ab4cc38c0654af46"')
    ]
    try:
        with open(input_file, 'r+', encoding='utf-8', errors='replace') as file:
            content = file.read()
            json_data = json.loads(content)
            sorted_data = sort_keys_recursive(json_data)

            json_data_str = json.dumps(sorted_data, indent=2, ensure_ascii=False)
            for before, after in template_resource:
                json_data_str = re.sub(before, after, json_data_str)

            content = json_data_str.replace('\r\n', '\n').replace('\r', '\n')
            file.seek(0)
            file.write(content)
            file.truncate()
        print(f"Success with file: {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def thumbnail_clean(input_file):
    try:
        with open(input_file, 'wb') as file:
            file.write(b'')
            print(f"Success with file: {input_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def scan_folder_toclean(folder_path):
    try:
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for element in files:
                    path = os.path.join(root, element)
                    if element.endswith('thumbnail.png'):
                        thumbnail_clean(path)
                    elif element.endswith('resource.json'):
                        resource_clean(path)
    except Exception as e:
        print("Error during main process - " + str(e))

# --- Script extraction ---------------------------------------------------------

def make_code_readable(code: str) -> str:
    return (
        code.replace('\\t', '    ')
            .replace('\\n', '\n')
            .replace('\\u003d\\u003d', '==')
            .replace('\\u003d', '=')
    )

def process_json(
    data,
    parent_key='',
    meta_info=None,
    config_info=None,
    prop_key=None,
    script_type=None,
    base_dir='extracted_scripts'
):
    if isinstance(data, dict):
        current_meta = data.get('meta', meta_info)
        current_config = data.get('config', config_info)

        for key, value in data.items():
            if key == 'propConfig':
                for prop_key_inner, prop_value in value.items():
                    if isinstance(prop_value, dict) and 'binding' in prop_value:
                        binding_data = prop_value['binding']
                        new_script_type = 'binding'
                        process_json(
                            binding_data,
                            parent_key,
                            current_meta,
                            current_config,
                            prop_key_inner,
                            new_script_type,
                            base_dir
                        )
            elif key in ["code", "script"] and isinstance(value, str):
                tail = last_key_segment(parent_key)
                if tail in SKIP_TEXT_KEYS:
                    print(f"Skipped non-code text under '{tail}' at path '{parent_key}'.")
                    continue
                if not is_probably_code(value):
                    print(f"Skipped non-code text at path '{parent_key}.{key}'.")
                    continue

                readable_code = make_code_readable(value)
                save_code_to_file(
                    readable_code, parent_key, current_meta,
                    current_config, prop_key, script_type, base_dir, data
                )
            elif key == 'binding':
                new_script_type = 'binding'
                new_key = f"{parent_key}_{key}" if parent_key else key
                process_json(value, new_key, current_meta, current_config,
                             key, new_script_type, base_dir)
            elif key in [
                'onChange', 'onClick', 'onActionPerformed',
                'messageHandlers', 'onResizeEvent', 'onStartup', 'onMoveEvent'
            ]:
                new_script_type = key
                new_key = f"{parent_key}_{key}" if parent_key else key
                process_json(value, new_key, current_meta, current_config,
                             key, new_script_type, base_dir)
            else:
                new_key = f"{parent_key}_{key}" if parent_key else key
                process_json(value, new_key, current_meta, current_config,
                             prop_key, script_type, base_dir)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}_{i}" if parent_key else str(i)
            process_json(item, new_key, meta_info, config_info,
                         prop_key, script_type, base_dir)

def create_filename(prop_key, parent_key, meta_info, script_type=None, message_type=None):
    if script_type == 'binding' and prop_key:
        filename = prop_key.replace('/', '_').replace('[', '_').replace(']', '_')
    elif message_type:
        filename = message_type
    else:
        parts = [meta_info['name']] if meta_info and 'name' in meta_info else []
        if prop_key:
            if script_type not in [
                "onChange", "onClick", "onActionPerformed",
                "messageHandlers", "onResizeEvent", "onStartup", "onMoveEvent"
            ]:
                parts.append(prop_key.replace('/', '_').replace('[', '_').replace(']', '_'))
        else:
            parts.append(parent_key.replace('.', '_').replace('[', '_').replace(']', '_'))
        filename = '_'.join(parts).strip('_')
    return filename

def save_code_to_file(code, parent_key, meta_info, config_info,
                      prop_key, script_type, base_dir, data):
    folder_path = os.path.join(base_dir, script_type) if script_type else os.path.join(base_dir, 'other')
    os.makedirs(folder_path, exist_ok=True)

    message_type = None
    if script_type == 'messageHandlers':
        message_type = data.get('messageType', None)

    filename = create_filename(prop_key, parent_key, meta_info, script_type, message_type)
    filename = os.path.join(folder_path, f"{filename}.py")

    base_filename, extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1

    if script_type == 'binding' and config_info:
        config_json = json.dumps(config_info, indent=4, ensure_ascii=False)
        commented_config = "\n".join([f"# {line}" for line in config_json.splitlines()])
        code = f"{commented_config}\n\n{code}"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(code)
    print(f"Saved script to: {filename}")

def process_view_json_files(folder_path):
    try:
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('view.json'):
                        file_path = os.path.join(root, file)
                        print(f"Processing file: {file_path}")
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as json_file:
                            data = json.load(json_file)
                            script_dir = os.path.join(root, 'extracted_scripts')
                            os.makedirs(script_dir, exist_ok=True)
                            process_json(data, base_dir=script_dir)
    except Exception as e:
        print("Error processing view.json files - " + str(e))

# --- NEW: package initializers and exports for script-python -------------------
def _list_functions_from_code(code_file):
    """Return top-level function names from code.py, excluding private (_...)."""
    try:
        with open(code_file, 'r', encoding='utf-8', errors='replace') as f:
            tree = ast.parse(f.read(), filename=code_file)
        names = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                names.append(node.name)
        return names
    except Exception as e:
        print(f"Could not parse functions from {code_file}: {e}")
        return []

def _write_init_if_changed(path, content):
    """Write content to path if it differs from existing; create parent dirs."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = None
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                existing = f.read()
        except Exception:
            existing = None
    if existing != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Wrote: {path}")

def _generate_init_content(func_names):
    header = "# Auto-generated by packaging script. Do not edit manually.\n"
    if func_names:
        imports = ",\n    ".join(func_names)
        all_list = ",\n    ".join(f'"{n}"' for n in func_names)
        return (
            f"{header}from .code import (\n"
            f"    {imports},\n"
            f")\n\n__all__ = [\n"
            f"    {all_list},\n]\n"
        )
    else:
        return header

def ensure_script_python_packages(root_folder):
    """
    For each directory under 'script-python', ensure __init__.py exists.
    If code.py is present (and not in an excluded dir), export its functions.
    """
    if not os.path.isdir(root_folder):
        return

    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Always ensure __init__.py exists
        init_path = os.path.join(dirpath, '__init__.py')

        # Determine whether to export functions from code.py here
        rel_parts = os.path.relpath(dirpath, root_folder).split(os.sep)
        should_export = not any(p in EXPORT_EXCLUDE_DIRS for p in rel_parts if p)

        code_file = os.path.join(dirpath, 'code.py')
        if os.path.isfile(code_file) and should_export:
            func_names = _list_functions_from_code(code_file)
            content = _generate_init_content(func_names)
            _write_init_if_changed(init_path, content)
        else:
            # Just ensure an empty (header-only) __init__.py exists
            content = "# Auto-generated by packaging script.\n"
            _write_init_if_changed(init_path, content)

def ensure_all_script_python_roots(folder_path):
    """
    Walk the provided folder and run ensure_script_python_packages()
    on every directory named 'script-python'.
    """
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for d in list(dirnames):
            if d == 'script-python':
                root = os.path.join(dirpath, d)
                print(f"Ensuring package __init__ and exports under: {root}")
                ensure_script_python_packages(root)


if __name__ == "__main__":
    import sys
    # Usage:
    #   python this_script.py [optional-root]
    #
    # If a root is provided, we run against it; otherwise we use default_folder_path.
    if len(sys.argv) != 2:
        folder_path = default_folder_path
        remove_extracted_scripts(folder_path)
        scan_folder_toclean(folder_path)
        process_view_json_files(folder_path)
        # NEW: create __init__.py files & exports under every script-python/ inside folder_path
        ensure_all_script_python_roots(folder_path)
    else:
        folder_path = sys.argv[1]
        remove_extracted_scripts(folder_path)
        scan_folder_toclean(folder_path)
        process_view_json_files(folder_path)
        ensure_all_script_python_roots(folder_path)
