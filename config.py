from groq import Groq
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'data', 'api.env')
load_dotenv(dotenv_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"

def get_completion(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
