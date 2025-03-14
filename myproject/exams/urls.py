
# filepath: c:\Users\Sarthak\OneDrive\ドキュメント\AssignmentE\myproject\exams\urls.py
from django.urls import path
from .views import login_view, rules_view, set_selection_view, question_entry_view, question_view, result_view

urlpatterns = [
    path('', login_view, name='login'),
    path('rules/', rules_view, name='rules'),
    path('set_selection/', set_selection_view, name='set_selection'),
    path('question_entry/<str:set_name>/<int:num_questions>/', question_entry_view, name='question_entry'),
    path('questions/<int:question_id>/', question_view, name='question_view'),
    path('result/', result_view, name='result_view'),
]
