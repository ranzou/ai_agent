import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    output = ""
    abs_working = os.path.abspath(working_directory)
    combined_path = os.path.join(abs_working, directory)
    abs_directory = os.path.abspath(combined_path)

    #    print(f"Working directory: {abs_working}")
    #    print(f"Target directory: {abs_directory}")

    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'

    common_path = os.path.commonpath([abs_working, abs_directory])
    #    print(f"Common path: {common_path}")

    if common_path == abs_working and len(abs_directory) >= len(abs_working):
        files = os.listdir(abs_directory)
        for file in files:
            try:
                file_path = os.path.join(abs_directory, file)
            except Exception:
                return f"Error: Couldn't join {abs_directory} and {file}"

            try:
                size = os.path.getsize(file_path)
            except Exception:
                return f"Error: Couldn't get size of {file_path}"

            try:
                dir = os.path.isdir(file_path)
            except Exception:
                return f"Error: Couldn't check whether {file_path} is a directory"

            output += f"- {file}: file_size={size} bytes, is_dir={dir}\n"
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    return output


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
