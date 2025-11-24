import os

def get_files_info(working_directory, directory="."):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, directory))

        if not target_abs.startswith(wd_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_abs):
            return f'Error: The directory "{directory}" does not exist.'
        
        dir_entries = os.listdir(target_abs)
        return_string = ""

        for entry in dir_entries:
            entry_path = os.path.join(target_abs, entry)
            try:
                size = os.path.getsize(entry_path)
            except Exception as e:
                return_string += f'- {entry}: Error getting size: {e}\n'
                continue
            return_string += f'- {entry}: file_size={size} bytes, is_dir={os.path.isdir(entry_path)}\n'
        
        return return_string
    
    except Exception as e:
        return f'Error: {e}'

