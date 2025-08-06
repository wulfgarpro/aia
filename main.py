import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt


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

    iters = 0
    while True:
        iters += 1

        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if response.usage_metadata:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

        if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                if function_call_content:
                    messages.append(function_call_content)

        if not response.function_calls:
            print(response.text)  # Finished - there're no more function calls to make.
            break

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

        for response in function_responses:
            messages.append(response)


if __name__ == "__main__":
    main()
