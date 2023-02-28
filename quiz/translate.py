import deepl
from deepl.exceptions import DeepLException
from django.conf import settings

from quiz.models import TranslatedQuestion


def get_translated_question_text(question, language):
    try:
        translated_question = TranslatedQuestion.objects.get(
            language=language, question=question
        )

    except TranslatedQuestion.DoesNotExist:
        # https://github.com/DeepLcom/deepl-python
        translator = deepl.Translator(settings.DEEPL_AUTH_KEY)

        try:
            if language.supports_formality:
                result = translator.translate_text(
                    question.full_text, target_lang=language.code, formality="less"
                )

            else:
                result = translator.translate_text(
                    question.full_text, target_lang=language.code
                )
        except DeepLException:
            return (
                "⚠️ Problem with the translation... We apologize for the inconvenience."
            )

        translated_question = TranslatedQuestion.objects.create(
            language=language,
            question=question,
            original_text=question.full_text,
            translated_text=result.text,
        )
        return translated_question.translated_text

    return "⚠️ Problem with the translation... We apologize for the inconvenience."
