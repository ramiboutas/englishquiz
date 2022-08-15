from django import template
from django.urls import reverse
register = template.Library()

from quiz.models import DeeplLanguage, Question

@register.simple_tag
def get_question_translation_url(id_language, id_question):
    return reverse('quiz_translate_question_text', kwargs={'id_question': id_question, 'id_language': id_language})
