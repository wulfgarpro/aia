import os
from config import MAX_CHARS


def write_file(working_dir, file_path, content):
    target_file = os.path.abspath(os.path.join(working_dir, file_path))

    if not target_file.startswith(os.path.abspath(working_dir)):
        return f"Error: Cannot write '{file_path}' as it is outside the permitted working directory"

    try:
        with open(target_file, "w+") as f:
            f.write(content)
        # Feedback loops... let the LLM know the action it took worked with a success message.
        return (
            f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        )
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
