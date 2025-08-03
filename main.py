import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
        model="gemini-2.0-flash-001", contents=messages
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
