from email.mime import message
import json
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def initialize_environment():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user","content": args.user_prompt,}
    ]
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    
    return args, messages, client


def agent_loop(messages, client, args):
    for _ in range(20):  # Limit to 3 iterations for safety
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )
        
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                if not result_message:
                    raise Exception(f"Function call failed: {result_message}")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                # Append the tool call result to the messages for context
                messages.append({"role": "tool", "content": result_message["content"], "tool_call_id": result_message["tool_call_id"]})
        else:
                if not response.usage:
                    raise RuntimeError("Response does not contain usage information.")

                return response.choices[0].message, response.usage

        #if the loop reaches the maximum number of iterations and does not return exit with code 1 and print an error message
    print("Error: Maximum iterations reached without a final response.")
    exit(1)
        
    




def main():

    args, messages, client = initialize_environment()

    message, response = agent_loop(messages, client, args)
    

    #print the response content
    print(message.content)

    
    #if verbose flag is set, print the user prompt and token usage
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.prompt_tokens}")
        print(f"Response tokens: {response.completion_tokens}")

if __name__ == "__main__":
    main()
