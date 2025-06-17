import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    file_extension = os.path.splitext(file_path)[-1]

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if file_extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            abs_file_path, timeout=30, capture_output=True, cwd=abs_working_dir
        )
        if result.stdout != "":
            output = f"STDOUT: {result.stdout}, "
        if result.stderr != "":
            output += f"STDERR: {result.stderr}, "
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
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
