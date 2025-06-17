import os
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    combined_path = os.path.join(abs_working, file_path)
    abs_file = os.path.abspath(combined_path)

    #    print(f"Working directory: {abs_working}")
    #    print(f"Target directory: {abs_file}")

    common_path = os.path.commonpath([abs_working, abs_file])
    #    print(f"Common path: {common_path}")

    if common_path == abs_working and len(abs_file) >= len(abs_working):
        try:
            file = os.path.isfile(abs_file)
        except Exception:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 10000:
            file_content_string += (
                f'[...File "{file_path}" truncated at 10000 characters]'
            )
    else:
        return f'Cannot read "{file_path}" as it is outside the permitted working directory'

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieve the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file",
            ),
        },
    ),
)
