# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from __future__ import annotations

from django.contrib import admin
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedStackedInline

from .models import Answer
from .models import DeeplLanguage
from .models import Lection
from .models import Question
from .models import Quiz
from .models import TranslatedQuestion


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
    exclude = ("created_by", "promoted", )
    model = Question
    extra = 10
    fk_name = "lection"
    inlines = [AnswerInline]



# Lection


@admin.register(Lection)
class LectionAdmin(NestedModelAdmin):
    search_fields = ["name"]
    readonly_fields = ["views"]
    list_filter = ["name", "quiz__name"]
    prepopulated_fields = {"slug": ("name",)}
    model = Quiz
    inlines = [QuestionInline]

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            question_list = formset.save(commit=False)
            for question in question_list:
                question.created_by = request.user
        return super().save_related(request, form, formsets, change)


# Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["full_text"]
    readonly_fields = [
        "lection",
        "text_one",
        "text_two",
        "text_three",
        "type",
        "explanation",
        "created_by",
    ]
    list_filter = ["type", "promoted"]
    list_display = ["full_text", "type", "promoted"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


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
