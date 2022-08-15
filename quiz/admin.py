# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
from django.contrib import admin
from .models import Quiz, Lection, Question, Answer, DeeplLanguage, TranslatedQuestion

class LectionInline(admin.StackedInline):
    model = Lection
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3

admin.site.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['views']
    list_filter = ['name']
    inlines = [LectionInline,]


admin.site.register(Lection)
class LectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    readonly_fields = ['views']
    list_filter = ['name', 'quiz__name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [QuestionInline,]


admin.site.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['text_one']
    list_filter = ['lection']
    inlines = [AnswerInline,]


admin.site.register(DeeplLanguage)
class DeeplLanguageAdmin(admin.ModelAdmin):
    list_filter = ['formality']
    list_display = ['name', 'code', 'formality']


admin.site.register(TranslatedQuestion)
class TranslatedQuestionAdmin(admin.ModelAdmin):
    list_filter = ['language']
    list_display = ['name', 'code', 'formality']
    readonly_fields = ['language', 'question', 'original_text', 'created', 'updated']
    
