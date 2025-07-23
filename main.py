import os
import anthropic
import openai
import ollama
from google import genai
from dotenv import load_dotenv

def main():
    print("Hello from aiagenttutorial!")

def run_llm_call(prompt, provider, model):
    load_dotenv()
    print(f"User: {prompt}")
    if provider == "openai":
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        system_message = "You are a helpful assistant."

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    elif provider == "gemini":
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=GEMINI_API_KEY)
        history=[]
        #history.append("You are a helpful assistant.")

        chat = client.chats.create(model=model, history=history)
        response = chat.send_message(prompt)
        print(f"Assistant: {response.text}\n")
        return response.text
    elif provider == "anthropic":
        ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        print(f"Assistant: {response.content[0].text}\n")
        return response.content[0].text
    elif provider == "Ollama":
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        print(f"Assistant: {response['message']['content']}\n")
        return response['message']['content']

if __name__ == "__main__":
    #run_llm_call("What is the capital of Japan?", "openai", "gpt-4o")
    #run_llm_call("What is the capital of Japan?", "gemini", "gemini-2.0-flash-exp")
    #run_llm_call("What is the capital of Japan?", "anthropic", "claude-3-5-sonnet-20241022")
    run_llm_call("What is the capital of Japan?", "Ollama", "gemma3")
