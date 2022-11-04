from __future__ import annotations

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def get_question_translation_url(id_language, id_question):
    return reverse(
        "quiz_translate_question_text",
        kwargs={"id_question": id_question, "id_language": id_language},
    )
