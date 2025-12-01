import os
import sys
import traceback
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
from functions.schema import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt here>'")
        sys.exit(1)
    prompt = sys.argv[1]
    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files
        - Never modify main.py directly.

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    i = 0
    max = 20

    try:
        while i < max:
            i += 1
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
                )
            
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if not response.function_calls:
                print(response.text)
                break
            
            #if response.function_calls:
            #    for function_call in response.function_calls:
            #        print(f"Calling function: {function_call.name}({function_call.args})")
            if response.function_calls:
                function_responses = []
                for function_call in response.function_calls:
                    # Call the function and capture the result
                    func_content = call_function(function_call, verbose="--verbose" in sys.argv)

                    # Validate the returned types.Content has parts[0].function_response.response
                    if not func_content.parts or len(func_content.parts) == 0:
                        raise RuntimeError(f"Fatal: call_function returned no parts for {function_call.name}")
                    if not func_content.parts[0].function_response or not func_content.parts[0].function_response.response:
                        raise RuntimeError(f"Fatal: Missing function response for {function_call.name}")

                    # Append the part (we'll use these later)
                    function_responses.append(func_content.parts[0])

                    if "--verbose" in sys.argv:
                        print(f"-> {func_content.parts[0].function_response.response}")
                    
                messages.append(types.Content(role="user", parts=function_responses))
            else:
                print(response.text)
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred on iteration {i}: {e}")
        if "--verbose" in sys.argv:
            traceback.print_exc()
        sys.exit(1)
    else:
        if i >= max:
            print(f"Reached maximum iterations ({max}) without completing the task.")

if __name__ == "__main__":
    main()
