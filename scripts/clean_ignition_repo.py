import os
import shutil


default_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ignition-data/projects/Novotek-core')

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
        print("An error occurred:", str(e))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        remove_extracted_scripts(default_folder_path)
    else:
        folder_path = sys.argv[1]
        remove_extracted_scripts(folder_path)
