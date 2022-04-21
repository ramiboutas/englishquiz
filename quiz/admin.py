# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from django.contrib import admin
from .models import Quiz, Lection, Question, Answer

class LectionInline(admin.StackedInline):
    model = Lection
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


class QuizAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    inlines = [LectionInline,]


class LectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'quiz__name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [QuestionInline,]


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'lection__name']
    inlines = [AnswerInline,]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Lection, LectionAdmin)
admin.site.register(Question, QuestionAdmin)
