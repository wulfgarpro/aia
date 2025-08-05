import argparse
import os
from dotenv import load_dotenv
from google import genai
from functions import get_file_content, get_files_info, run_python_file, write_file
from google.genai import types

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="aia",
    )
    parser.add_argument("user_prompt")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Keep track of the user's conversation with the Gemini LLM.
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, args.verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result")
        function_response = function_call_result.parts[0].function_response.response
        if args.verbose:
            print(f"-> {function_response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")


if __name__ == "__main__":
    main()
