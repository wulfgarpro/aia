import os


def get_files_info(working_dir, dir="."):
    target_dir = os.path.abspath(os.path.join(working_dir, dir))

    if not target_dir.startswith(os.path.abspath(working_dir)):
        return f"Error: Cannot list '{dir}' as it is outside the permitted working directory"

    if not os.path.isdir(target_dir):
        return f"Error: '{dir}' is not a directory"

    try:
        with os.scandir(target_dir) as entries:
            lines = [
                f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}"
                for entry in entries
            ]
            return "\n".join(lines)
    except Exception as e:
        return f"Error listing files: {e}"
