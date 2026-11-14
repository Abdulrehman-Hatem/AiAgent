import os,subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
     #if the file is outside of the working directory, return an error
    abs_path = os.path.relpath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_path, file_path))
    
    try:
        if os.path.commonpath([abs_path, target_file_path]) != abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    #check that the file exists and is a regular file
    if not os.path.isfile(os.path.join(working_directory, file_path)):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    #check that the file has a .py extension
    if not file_path.endswith(".py"):
         return f'Error: "{file_path}" is not a Python file'

    #run the python file and return the output
    try:
        command = ["python", os.path.join(working_directory, file_path)]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)

        returnstring = ""
        if result.returncode != 0:
            returnstring += f"Process exited with code {result.returncode}\n"
        returnstring += f"STDOUT:\n{result.stdout}\n"
        returnstring += f"STDERR:\n{result.stderr}\n"
        if not result.stderr and not result.stdout:
            returnstring += "No output produced"
        return returnstring
    except Exception as e:
        return f"Error: executing Python file: {e}"


