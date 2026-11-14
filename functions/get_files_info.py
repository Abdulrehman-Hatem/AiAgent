import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    ## get the relative path of the directory from the working directory
    ## the relative path is set by the llm and the working directory is the root of the project
    
    returnstring:str= f"Result for {directory} directory:\n" if directory != "." else f"Result for current directory:\n"
    

    abs_path = os.path.relpath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path, directory))

    ## check if the target directory is outside of the working directory
    try:
        if os.path.commonpath([abs_path, target_dir]) != abs_path:
            return returnstring + f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except ValueError:
        return returnstring + f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #if the diectory is not a directory return an error
    if not os.path.isdir(os.path.join(working_directory, directory)):
            return returnstring + f'Error: "{directory}" is not a directory'
    else:
            # list all the files in the directory as filename: file_size=size bytes, isdir_=bool
            for filename in os.listdir(os.path.join(working_directory, directory)):
                file_path = os.path.join(working_directory, directory, filename)
                file_size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                returnstring += f"  - {filename}: file_size={file_size} bytes, is_dir={is_dir}\n"

            return returnstring
    

    