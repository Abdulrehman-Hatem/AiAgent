import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # write the content to the file at the given path relative to the working directory

    #if the file is outside of the working directory, return an error
    abs_path = os.path.relpath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_path, file_path))

    try:
        if os.path.commonpath([abs_path, target_file_path]) != abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    #check if the directory of the file already exists
    if os.path.dirname(file_path) and not os.path.exists(os.path.join(working_directory, os.path.dirname(file_path))):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    #make sure all the directories in the path exist, if not create them
    os.makedirs(os.path.dirname(os.path.join(working_directory, file_path)), exist_ok=True)

    # write the content to the file
    try:
        with open(os.path.join(working_directory, file_path), "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Could not write to file "{file_path}". Exception: {str(e)}'