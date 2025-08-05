import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="The optional arguments to pass to the Python file being executed.",
                ),
                description="The optional arguments to pass to the Python file being executed.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_dir, file_path, args=[]):
    target_file = os.path.abspath(os.path.join(working_dir, file_path))
    abs_working_dir = os.path.abspath(working_dir)

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'

    if target_file[-3:] != ".py":
        return f"Error: '{file_path}' is not a Python file."

    try:
        cmd = ["python", target_file]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,  # 30 seconds
            cwd=abs_working_dir,
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
