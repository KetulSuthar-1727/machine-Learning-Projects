from ddgs import DDGS
from openai import OpenAI
import os
from dotenv import load_dotenv

# This code is for the loading the api key and storing it into the variable
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

client = OpenAI(api_key=api_key)


# This fucntion search in the google for the asked data
def search_web(query, max_results=10):
    snippets = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if r.get("body"):
                snippets.append(r["body"])
            elif r.get("title"):
                snippets.append(r["title"])
            else:
                snippets.append(r.get("href", ""))
    return "\n\n".join(snippets)


# This fucntion generartes the answer using the opeai
def get_answer(user_input):   # <- This is the getanwser fucntion
    search_results = search_web(user_input)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer concisely using only the provided web data."},
        {"role": "user", "content": f"Question: {user_input}\nWeb data:\n{search_results}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.0
    )
    return response.choices[0].message.content

user_name = input("Enter Your Name Cheif : ")
# It loops untill the user exits
print("Search Chatbot (type 'exit' to quit)")
while True:
    
    user_text = input(f"{user_name}: ")
    if user_text.lower() in ["exit", "quit"]:
        print(f"Ramsy: Goodbye {user_name} see you later!")
        break
    answer = get_answer(user_text)
    print("Ramsy:", answer)
