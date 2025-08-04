import os
from config import MAX_CHARS


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
