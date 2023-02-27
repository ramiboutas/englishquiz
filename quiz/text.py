import random


def get_correct_message():
    messages = [
        "Great!",
        "Correct!",
        "Well done!",
        "Terrific!",
        "Fantastic!",
        "Excellent!",
        "Super!",
        "Marvelous!",
        "Outstanding!",
        ":)",
    ]
    return random.choice(messages)


def get_incorrect_message():
    messages = [
        "Next time you'll get it!",
        "There's a more accurate answer!",
        "Oops!",
        "Wrong :(",
        "Not quite correct!",
        ":(",
        "Not quite right!",
    ]
    return random.choice(messages)
