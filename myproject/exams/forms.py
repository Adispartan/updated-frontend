from django import forms
from .models import Question

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['option'] = forms.ChoiceField(
            label=question.question_text,  # Use the question text as the label
            choices=[
                (1, question.option1),
                (2, question.option2),
                (3, question.option3),
                (4, question.option4)
            ],
            widget=forms.RadioSelect()
        )