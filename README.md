uv init
uv venv
source .venv/bin/activate
uv add openai google-genai anthropic requests python-dotenv ollama vertexai

ollama serve
ollama run gemma
