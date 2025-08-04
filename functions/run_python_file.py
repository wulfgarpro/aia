from ast import arg
import os
import subprocess


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
