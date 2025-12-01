import os
from functions.functions import *
from google.genai import types # type: ignore

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"

    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)
    elif function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )