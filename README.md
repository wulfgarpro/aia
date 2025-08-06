# aia

A dumb AI agent powered by the Gemini LLM to interact with a filesystem. It allows you to perform
various tasks such as listing files, reading file contents, executing Python files, and writing
files through a message feedback loop.

The agent is a _very_ simple example of an "agentic" style generative AI tool.

## Capabilities

* **List Files:** You can list files and directories within the working directory.
* **Read Files:** You can read the content of text-based files.
* **Execute Python Code:** You can execute Python files.
* **Write Files:** You can create or overwrite files with specified content.

## Limitations

* The agent operates within a constrained working directory. All file paths are relative to this
  directory (see `WORKING_DIR` in `config.py`).
* File reads are limited to the first 10000 characters (see `MAX_CHARS` in `config.py`).
* An agentic conversation with the LLM is limited to 20 iterations (see `MAX_ITER` in `config.py`).
* Free Gemini access is subject to resource exhaustion (i.e. `429 RESOURCE_EXHAUSTED`).

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
