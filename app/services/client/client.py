from openai import OpenAI
from app.utils.load_env import get_OPENAI_key, get_org
from output_models import Cards_List

def send_request(topic: str):
    client = OpenAI(
    api_key = get_OPENAI_key(),
    organization= get_org(),
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an assistant that creates flashcards. Each flashcard consists of a question and an answer."},
                {"role": "user", "content": f"Generate 5 flashcards about {topic}."}
            ],
        response_format = Cards_List
    )
    
    return completion