import argparse
import os
from dotenv import load_dotenv
from google import genai
from functions import get_files_info
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

function_call_map = {"get_files_info": get_files_info}


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="aia",
    )
    parser.add_argument("user_prompt")
    parser.add_argument("-v", "--verbose", action="store_false")

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
        print(response.text)

    for function_call_part in response.function_calls:
        if args.verbose:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
        else:
            print(f"Calling function: {function_call_part.name}")


if __name__ == "__main__":
    main()
