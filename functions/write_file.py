import os

def write_file(working_directory, file_path, content):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_abs.startswith(wd_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        dir_name = os.path.dirname(target_abs)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(target_abs, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'