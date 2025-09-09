import os
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


def google_search(query):
    """Fetch search results using Google Custom Search API."""
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }
    response = requests.get(GOOGLE_SEARCH_URL, params=params)

    if response.status_code != 200:
        return f"⚠️ Error fetching search results: {response.status_code}"

    data = response.json()
    results = []
    if "items" in data:
        for item in data["items"]:
            results.append(f"{item['title']}: {item['snippet']}")
    return "\n".join(results[:5]) if results else "No results found."


def ollama_chat(prompt):
    """Send prompt to Ollama Llama model and return reply."""
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8").strip()


def football_chatbot(user_input):
    
    search_results = google_search(user_input)
    context = f"Relevant search results:\n{search_results}"

    
    system_prompt = (
        "You are a professional football analyst AI. "
        "Use the search results as factual reference, "
        "then provide tactical breakdowns, player analysis, or match insights."
    )

    full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_input}\nAI:"
    return ollama_chat(full_prompt)


if __name__ == "__main__":
    print("⚽ Football Chatbot — type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", football_chatbot(user_input))
