# aia

A dumb AI agent powered by the Gemini LLM to interact with a filesystem. It allows you to perform
various tasks such as listing files, reading file contents, executing Python files, and writing
files through a message feedback loop.

The agent is a _very_ simple example of an "agentic" style generative AI tool.

## Capabilities

- **List Files:** You can list files and directories within the working directory.
- **Read Files:** You can read the content of text-based files.
- **Execute Python Code:** You can execute Python files.
- **Write Files:** You can create or overwrite files with specified content.

## Limitations

- The agent operates within a constrained working directory. All file paths are relative to this
  directory (see `WORKING_DIR` in `config.py`).
- File reads are limited to the first 10000 characters (see `MAX_CHARS` in `config.py`).
- An agentic conversation with the LLM is limited to 20 iterations (see `MAX_ITER` in `config.py`).
- Free Gemini access is subject to resource exhaustion (i.e. `429 RESOURCE_EXHAUSTED`).

## Setup

1. Set up a [free API key for Gemini](https://ai.google.dev/gemini-api/docs/api-key).
2. Create a `.env` file in the working directory.
3. Add the following line to the `.env` file, replacing `<YOUR_GEMINI_API_KEY>` with your actual
   Gemini API key:

   ```sh
   GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
   ```

4. Create a Python virtual environment with [uv](https://docs.astral.sh/uv/getting-started/installation/),
   install dependencies, and run `aia`:

   ```sh
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   uv run main.py --help
   ```

## Examples

Note that LLM behavior is inherently variable, so your results might vary when testing the below
examples.

```sh
$ uv run main.py "tell me what files exist in the root directory?"
Okay, I see the following files in the root directory: `main.py`, `pkg`, and `tests.py`. The `pkg` item is a directory.

$ uv run main.py "what sort of program is this project?"
The program is a calculator application. It takes a mathematical expression as a command-line argument, evaluates it using a `Calculator` class from the `pkg.calculator` module, and then renders the expression and result using a `render` function from the `pkg.render` module.

$ uv run main.py "run the calculator for me with expression 10 - 5 and give me the result"
The result of the expression "10 - 5" is 5.

$ uv run main.py "there's a bug in the calculator's code, tell me what it is, but don't fix it"
The bug lies in the precedence of operators. The `precedence` dictionary assigns precedence values where subtraction has the lowest precedence (1), multiplication and division have a higher precedence (2), and addition has the highest precedence (3). This is incorrect because multiplication and division should have higher precedence than addition and subtraction. Specifically, the precedence of '+' and '-' should be lower than '*' and '/'.

$ uv run main.py "run the calculator program and tell me what it calculates for 5 + 2 * 5"
The calculator program evaluates "5 + 2 * 5" as 35, which is incorrect. The correct answer, following the order of operations, is 15.

$ uv run main.py "fix the bug and run the calculator program again with 5 + 2 * 5"
The calculator program now correctly evaluates the expression "5 + 2 * 5" and returns the result 15.
```

## Prompt Engineering

The system prompt in `prompts.py` guides Gemini on how to approach tasks, utilise available
functions, and communicate effectively.

`aia`'s performance is highly dependent on the quality and structure of this prompt.
