# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from django.contrib import admin
from .models import Quiz, Lection, Question, Answer

class LectionInline(admin.StackedInline):
    model = Lection
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3


class QuizAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['views']
    list_filter = ['name']
    inlines = [LectionInline,]


class LectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['views']
    list_filter = ['name', 'quiz__name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [QuestionInline,]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text_one']
    list_filter = ['lection']
    inlines = [AnswerInline,]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Lection, LectionAdmin)
admin.site.register(Question, QuestionAdmin)
