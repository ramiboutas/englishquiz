from __future__ import annotations

import random

common_hashtags = "#englishtips #learnenglish #englishquizzes"


def get_hashtag_str_from_post_instance_tags(instance):
    hashtag_str = ""
    for tag in instance.tags.all():
        hashtag_str += "#" + tag.name + " "
    return hashtag_str


def get_cool_random_emoji():
    cool_emojis = ["🤙", "😎", "🙃", "🤟"]
    return random.choice(cool_emojis)


def get_salutation_text():
    salutation_options = [
        "Hey there!",
        "Hey, how is it going?",
        "Hi!",
        "Hey!",
        "Hey, what's up?",
    ]
    return random.choice(salutation_options)


# Blog Post
def get_blog_post_promotion_text(instance):
    """
    It generates text for promoting a blog post
    """
    hashtags_from_instance_tags = get_hashtag_str_from_post_instance_tags(instance)
    text = ""
    text += f"✍ Blog post: {instance.title}\n \n"
    text += f"{instance.description}\n \n"
    text += (
        f"More under: https://www.englishstuff.online{instance.get_detail_url()} \n \n"
    )
    text += f"{hashtags_from_instance_tags}"

    return text


# Quiz


def get_quiz_promotion_text(instance):
    """
    It generates text from a quiz instance
    """
    text = f"Check out this quiz: {instance.name} \n \n"
    text += f"👉 https://www.englishstuff.online{instance.get_detail_url()} \n \n"
    text += f'{common_hashtags} #{instance.name.replace(" ", "").lower()}'
    return text


# Question


def get_question_text(instance):
    """
    It generates text from a Question instance
    """
    text = ""
    if instance.type == 1:
        text += "What do you think that comes in the gap of the next sentence? 🤔\n\n"
        text += f"📚 {instance.text_one} ____ {instance.text_two}"
        if instance.text_three:
            text += f" ____ {instance.text_three}\n"
    if instance.type == 5:
        text += "Which option fits better in the gap of the next sentence? 🤔\n\n"
        text += f"📚 {instance.text_one}\n\n"
        text += "💡 Options:\n"
        for answer in instance.answer_set.all():
            text += f" 🔹 {answer.name}\n"

    return text


def get_question_promotion_text(instance, make_short=False):
    """
    It generates text from a question instance
    """

    cool_emoji = get_cool_random_emoji()
    question_text = get_question_text(instance)

    # Producing text
    text = ""
    if not make_short:
        text += f"Here a small question for you {cool_emoji} \n\n"
    text += f"{question_text} \n\n"
    text += "Check out the right answer here:\n"
    text += f"👉 https://www.englishstuff.online{instance.get_detail_url()} \n \n"
    text += f'{common_hashtags} #{instance.lection.quiz.name.replace(" ", "")}'

    return text
