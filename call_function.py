from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_call_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose=True):
    function_name = function_call_part.name

    # if verbose:
    print(f"Calling function: {function_name}({function_call_part.args})")

    if function_name not in function_call_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call_part.args)
    args["working_dir"] = WORKING_DIR

    function_call = function_call_map.get(function_name)
    function_result = function_call(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                # `from_function_response` requires the response to be a
                # dictionary, so we assign the result to a "result" field.
                response={"result": function_result},
            )
        ],
    )
