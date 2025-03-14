# filepath: c:\Users\Sarthak\OneDrive\ドキュメント\AssignmentE\myproject\exams\models.py
from django.db import models # type: ignore

class Question(models.Model):
    set_name = models.CharField(max_length=10)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField()

    def __str__(self):
        return self.question_text
