from client import send_request
from python_objects import save_object, load_object

loaded = load_object()

for i in loaded.cards:
    question = i.question
    answer = i.answer
    print(f"Q: {question}\nA: {answer}\n")    