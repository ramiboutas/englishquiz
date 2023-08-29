from __future__ import annotations

import random

from django.conf import settings


def get_salutation_text():
    salutation_options = [
        "Hey there!",
        "Hey, how is it going?",
        "Hi!",
        "Hey!",
        "Hey, what's up?",
    ]
    return random.choice(salutation_options)


def get_poll_explanation_text(question_obj):
    text_options = [
        "Guess the answer!",
        "What do you think the answer is?",
        "What goes in the gap?",
    ]
    text = random.choice(text_options)
    text += "\n\nCheck the right answer here 👉 "
    text += f"{settings.SITE_BASE_URL}{question_obj.get_detail_url()}"

    return text


def get_blog_post_promotion_text(blog_post):
    """
    It generates text for promoting a blog post
    """
    text = ""
    text += f"✍ Blog post: {blog_post.title}\n\n"
    text += f"{blog_post.description}\n\n"
    text += f"More under: {settings.SITE_BASE_URL}{blog_post.get_detail_url()}\n\n"

    return text


def get_question_text(question):
    """
    It generates text from a Question instance
    """
    text = ""
    if question.type == 1 or question.type == 2:
        text += "What do you think that comes in the gap of the next sentence? 🤔\n\n"
        text += f"📚 {question.text_one} ____ {question.text_two}"
        if question.text_three:
            text += f" ____ {question.text_three}\n"
    if question.type == 5:
        text += "Which option fits better in the gap of the next sentence? 🤔\n\n"
        text += f"📚 {question.text_one}\n"
        if question.text_two:
            text += f"📚 {question.text_two}\n"
        if question.text_three:
            text += f"📚 {question.text_three}\n"
        text += "\n💡 Options:\n"
        for answer in question.answer_set.all():
            text += f" 🔹 {answer.name}\n"

    return text


def get_question_promotion_text(instance, make_short=False):
    """
    It generates text from a question instance
    """

    question_text = get_question_text(instance)

    # Producing text
    text = ""
    if not make_short:
        text += f"Here a small question for you!\n\n"
    text += f"{question_text} \n\n"
    text += "Check out the right answer here:\n"
    text += f"👉 {settings.SITE_BASE_URL}{instance.get_detail_url()} \n\n"

    return text
