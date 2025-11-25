import os

def get_file_content(working_directory, file_path):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))
        MAX_CHARS = 10000

        if not target_abs.startswith(wd_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_abs, 'r') as file:
            content = file.read(MAX_CHARS)
            if file.read():
                content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    
    except Exception as e:
        return f'Error: {e}'