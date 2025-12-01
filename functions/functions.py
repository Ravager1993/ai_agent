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
    
def run_python_file(working_directory, file_path, args=[]):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_abs.startswith(wd_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: File "{file_path}" not found.'
        if not target_abs.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Execute the Python file and capture output
        import subprocess
        result = subprocess.run(['python', target_abs], capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return f'Error executing "{file_path}": {result.stderr}\n Process exited with code {result.returncode}'
        
        return_string = f'STDOUT: {result.stdout}STDERR: {result.stderr}\n{result}'
        return return_string
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
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