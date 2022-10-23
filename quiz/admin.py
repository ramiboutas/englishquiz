# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from __future__ import annotations

from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Answer, DeeplLanguage, Lection, Question, Quiz, TranslatedQuestion


class LectionInline(admin.StackedInline):
    model = Lection
    extra = 5


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["views"]
    list_filter = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        LectionInline,
    ]


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 3
    fk_name = "question"


class QuestionInline(NestedStackedInline):
    search_fields = ["text_one"]
    list_filter = ["lection"]
    readonly_fields = [
        "promoted",
    ]
    model = Question
    extra = 10
    fk_name = "lection"
    inlines = [AnswerInline]


@admin.register(Lection)
class LectionAdmin(NestedModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["views"]
    list_filter = ["name", "quiz__name"]
    prepopulated_fields = {"slug": ("name",)}
    model = Quiz
    inlines = [QuestionInline]


# Translation models


@admin.register(DeeplLanguage)
class DeeplLanguageAdmin(admin.ModelAdmin):
    list_filter = ["supports_formality"]
    readonly_fields = [
        "views",
    ]
    list_display = ["name", "code", "supports_formality", "views"]


@admin.register(TranslatedQuestion)
class TranslatedQuestionAdmin(admin.ModelAdmin):
    list_filter = ["language"]
    list_display = ["original_text", "language", "created"]
    readonly_fields = ["language", "question", "original_text", "created", "updated"]
