import openai
from dotenv import load_dotenv
import os
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    # ... (implementation of the weather function) ...
    return {"location": location, "temperature": "85", "unit": unit, "forecast": ["sunny", "windy"]
}

available_functions = {
    "get_current_weather": get_current_weather,
}

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o"

user_msg = "What's the weather like in San Jose, CA?"
messages = [{"role": "user", "content": user_msg}]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto",  # auto is default, but we'll be explicit
)
print ("tooling llm response: " + str(response))

response_message = response.choices[0].message
if response_message.tool_calls:
    messages.append(response_message)  # extend conversation with the LLM's reply
    for tool_call in response_message.tool_calls: # Loop through all requested tool calls
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_result = function_to_call(**function_args) # executing get_current_weather(**function_args) 
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_result),
            }
        )
print("final llm message: " + str(messages))

final_response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
    )  # get a new response from the model where it can see the function response
print(final_response.choices[0].message.content)        
