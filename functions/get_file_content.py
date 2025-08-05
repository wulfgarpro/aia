import os
from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_dir, file_path):
    target_file = os.path.abspath(os.path.join(working_dir, file_path))

    if not target_file.startswith(os.path.abspath(working_dir)):
        return f"Error: Cannot read '{target_file}' as it is outside the permitted working directory"

    if not os.path.isfile(target_file):
        return f"Error: File not found or is not a regular file: '{file_path}'"

    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(target_file) > MAX_CHARS:
                content += (
                    f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
                )
            return content
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
