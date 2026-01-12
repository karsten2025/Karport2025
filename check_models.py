import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def list_my_models():
    try:
        models = client.models.list()
        print("Verfügbare Modelle für deinen Key:")
        # Wir filtern nach den neuesten Modellen, um die Liste übersichtlich zu halten
        for model in sorted([m.id for m in models.data]):
            if "gpt-5" in model or "o1" in model or "gpt-4.1" in model:
                print(f" - {model}")
    except Exception as e:
        print(f"Fehler beim Abrufen der Modelle: {e}")

if __name__ == "__main__":
    list_my_models()