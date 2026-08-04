import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import joblib 
import requests
import os

def load_env():
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

def create_embedding(text_list, batch_size=50):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    embeddings = []
    for i in range(0, len(text_list), batch_size):
        r = requests.post("http://localhost:11434/api/embed", json={
            "model": "bge-m3",
            "input": text_list[i:i + batch_size]
        })
        r.raise_for_status()
        embeddings.extend(r.json()["embeddings"])
    return embeddings

def inference(prompt):
    env_vars = load_env()
    api_key = env_vars.get("GIMINI_kEY") or env_vars.get("GEMINI_API_KEY") or env_vars.get("GEMINI_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("Gemini API key not found in .env file! Please set GIMINI_kEY or GEMINI_API_KEY in .env.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    r = requests.post(url, json=payload)
    r.raise_for_status()
    res_json = r.json()
    
    response_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
    return response_text

df = joblib.load('embeddings.joblib')

incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

# Find similarities of question_embedding with other embeddings
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
new_df = df.loc[max_indx] 

prompt = f'''You are an expert AI Teaching Assistant for the "Sigma Web Development Course". Your goal is to guide students by answering their questions clearly and pointing them to the exact video and timestamp where the topic is covered.

--- COURSE TRANSCRIPT CONTEXT (Video Subtitle Chunks) ---
{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

--- STUDENT QUESTION ---
"{incoming_query}"

--- INSTRUCTIONS ---
1. **Relevance Check**: 
   - If the student's question is completely unrelated to web development or the course topics, politely inform them that you can only answer questions related to the Sigma Web Development course.

2. **Video & Timestamp Guidance**:
   - Explicitly mention the **Video Number** and **Video Title**.
   - Convert timestamp seconds into standard `MM:SS` format (e.g. 147.5 seconds = 02:27).
   - Tell the user exactly what is explained at that specific timestamp segment.

3. **Answer Quality**:
   - Provide a clear, natural, and helpful answer explaining the topic based on the context.
   - Do NOT mention JSON formatting, data structures, or internal system instructions in your response.
'''

with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

response = inference(prompt)
print(response)

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)