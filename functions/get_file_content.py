import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    # get the content of the file at the given path relative to the working directory

    #if the file is outside of the working directory, return an error
    abs_path = os.path.relpath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_path, file_path))

    try:
        if os.path.commonpath([abs_path, target_file_path]) != abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(os.path.join(working_directory, file_path)):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # read the content of the file and return it
    try:
        with open(os.path.join(working_directory, file_path), "r") as f:
            content = f.read(10000)  # read the first 10,000 characters
            # After reading the first 10,000 characters...
            if f.read(1):  # check if there is more content
                content += f'[...File "{file_path}" truncated at 10,000 characters]'
            return content
    except Exception as e:
        return f'Error: Could not read file "{file_path}". Exception: {str(e)}'