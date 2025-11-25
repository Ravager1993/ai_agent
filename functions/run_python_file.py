import os

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