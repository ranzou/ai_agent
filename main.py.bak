import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

verbose = False

if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
    prompt = sys.argv[1]
else:
    print("Usage: " + sys.argv[0] + " '<prompt>'")
    print("Optional flag: --verbose")
    sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
    #    config=types.GenerateContentConfig(system_instruction=system_prompt),
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)
if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if not response.function_calls:
    print(response.text)

function_responses = []
for function_call_part in response.function_calls:
    function_call_result = call_function(function_call_part, verbose)
    if (
        not function_call_result.parts
        or not function_call_result.parts[0].function_response
    ):
        raise Exception("empty function call result")
    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting")
