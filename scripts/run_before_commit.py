# -*- coding: utf-8 -*-
import json
import os
import re
import shutil

default_folder_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../ignition-data/projects/Novotek-core'
)

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

# Keys that are very likely to be plain text even if found under a "code/script" path.
SKIP_TEXT_KEYS = {
    'custom', 'label', 'title', 'description', 'tooltip',
    'text', 'message', 'placeholder', 'hint'
}

def last_key_segment(path_key):
    """Get the trailing segment of our synthesized parent_key (split on '_')."""
    if not path_key:
        return ''
    return path_key.split('_')[-1].lower()

def is_probably_code(s):
    """
    Conservative heuristic to detect code vs plain text.
    We look for common code tokens/keywords across JS/TS/Python.
    """
    if not isinstance(s, str):
        return False
    t = s.strip()
    if not t:
        return False

    # If it's extremely short and a single line without punctuation, likely text.
    if '\n' not in t and len(t) < 10 and not re.search(r'[;{}()=<>]|==|===|!=|:=', t):
        return False

    # Common code-ish patterns (don’t need all; any hit suggests code).
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

    # Heuristic: multiple indented lines often mean code.
    indented_lines = sum(1 for line in t.splitlines() if line.startswith(('  ', '\t')))
    if indented_lines >= 2:
        return True

    # Otherwise treat as text.
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

            # Normalize line endings to LF and write back
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
                # Skip if the path's trailing key looks like a plain-text field
                tail = last_key_segment(parent_key)
                if tail in SKIP_TEXT_KEYS:
                    print(f"Skipped non-code text under '{tail}' at path '{parent_key}'.")
                    continue

                # Skip if content doesn't look like code
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

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        remove_extracted_scripts(default_folder_path)
        scan_folder_toclean(default_folder_path)
        process_view_json_files(default_folder_path)
    else:
        folder_path = sys.argv[1]
        remove_extracted_scripts(folder_path)
        scan_folder_toclean(folder_path)
        process_view_json_files(folder_path)
