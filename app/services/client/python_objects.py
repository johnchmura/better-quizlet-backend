import pickle

def save_object(output):
    if not output.refusal:
        raw_cards_data = output.parsed
        with open("flashcards_output.pkl", "wb") as file:
            pickle.dump(raw_cards_data, file)
        print("Output saved to flashcards_output.pkl")
    else:
        print(output.refusal)

def load_object():
    with open("flashcards_output.pkl", "rb") as file:
        test_cards_data = pickle.load(file)
    return test_cards_data
