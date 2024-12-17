from openai import OpenAI
from loadenv import get_key, get_org
from output_models import Flash_Card, Cards_List

def send_request(topic: str):
    client = OpenAI(
    api_key = get_key(),
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