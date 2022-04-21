import random
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, unique=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def get_detail_url(self):
        return reverse('quiz_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Quiz, self).save(*args, **kwargs)


class Lection(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, unique=True)

    def get_first_question(self):
        return self.question_set.all().first()

    def __str__(self):
        return f'{self.name} ({self.quiz.name})'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lection, self).save(*args, **kwargs)


class Question(models.Model):
    lection = models.ForeignKey(Lection, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    explanation = models.CharField(blank=True, null=True, max_length=128)

    def get_detail_url(self):
        return reverse('question_detail', kwargs={'slug_quiz': self.lection.quiz.slug, 'slug_lection': self.lection.slug, 'id_question': self.id})

    def is_first(self):
        return self.__class__.objects.all().first() == self

    def is_last(self):
        return self.__class__.objects.all().last() == self

    def __str__(self):
        return f'{self.lection.quiz.name} - {self.lection.name} - {self.name}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name
