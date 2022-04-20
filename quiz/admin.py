from django.contrib import admin

from .models import Quiz, Lection, Question, Answer


admin.site.register(Quiz)
admin.site.register(Lection)
admin.site.register(Question)
admin.site.register(Answer)
