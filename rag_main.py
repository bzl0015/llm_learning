import re
import os
import vertexai
#! uv add chromadb
import chromadb
from google import genai
from dotenv import load_dotenv

text = """
Garfield, a plump orange tabby, spent most of his days in a blissful state of napping. He loved undoubtedly
  eating, especially lasagna, which he considered the pinnacle of culinary achievement. When not devouring food or sleeping,
  Garfield enjoyed tormenting his owner, Jon Arbuckle, and kicking Odie, the cheerful beagle, off the table. Jon often tried to get Garfield to exercise, but the cat preferred to watch TV, another one of his cherished pastimes. Despite his lazy demeanor, Garfield had a sharp wit and a deep philosophical appreciation for Mondays (or rather, his disdain for them).
Doraemon, the blue robotic cat from the future, found Nobita crying again. "Suneo and Gian took my new comic book!" Nobita
  wailed. Doraemon sighed, then pulled out the "Anywhere Door" from his four-dimensional pocket. "Let's go get it back," he
  said, and they stepped through, appearing instantly in Gian's room. Gian, startled, quickly returned the comic, and Nobita
  cheered, forgetting his tears.
"""

chunks = re.split(r'(?<=[.!?])\s+', text) ## split by ., !, or ? followed by a space
chunks = [s.strip() for s in chunks if s.strip()] ## filter out empty strings
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
print (GEMINI_API_KEY)
embedding_model = "models/text-embedding-004"
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.embed_content(
  model="models/text-embedding-004",
  contents=chunks,
)
embeddings = [e.values for e in response.embeddings]

DB_NAME = "my_story_knowledge_base"

db_client = chromadb.Client()
db_collection = db_client.get_or_create_collection(name=DB_NAME)
db_collection.add(
    embeddings=embeddings,
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)
print("Vector db format:")
print(db_collection.peek(1))

query = "what are Garfield's favorate hobbies?"
print("Question:" + query)
response = client.models.embed_content(
    model=embedding_model,
    contents=[query],
    config=genai.types.EmbedContentConfig(
        task_type="retrieval_query",
    )
)
query_embeddings  = [e.values for e in response.embeddings]

results = db_collection.query(
    query_embeddings=query_embeddings, 
    n_results=3)
print("Close queries:")
print(results["documents"])

context = "\n".join(results["documents"][0])
prompt = f"""
Answer the user's query based ONLY on the provided context. If the context does not contain the answer, say 'The provided context does not have the answer to this question'.

    Context:
    {context}

    Query: {query}

    Answer:
"""
model="gemini-2.5-flash"
response = client.models.generate_content(
    model=model,
    contents=prompt,
)
print("Answer is:")
print(response.text)