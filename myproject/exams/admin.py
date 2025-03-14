# filepath: c:\Users\Sarthak\OneDrive\ドキュメント\AssignmentE\myproject\exams\admin.py
from django.contrib import admin # type: ignore
from .models import Question

admin.site.register(Question)