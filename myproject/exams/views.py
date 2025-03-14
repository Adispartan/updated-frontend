from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Question
from .forms import QuestionForm
import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rules')  # Redirect to the rules page
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def rules_view(request):
    return render(request, 'rules.html')

def set_selection_view(request):
    if request.method == 'POST':
        set_name = request.POST['set_name']
        num_questions = int(request.POST['num_questions'])
        return redirect('question_entry', set_name=set_name, num_questions=num_questions)
    return render(request, 'set_selection.html')

def question_entry_view(request, set_name, num_questions):
    if request.method == 'POST':
        for i in range(num_questions):
            question_text = request.POST[f'question_{i}']
            option1 = request.POST[f'option1_{i}']
            option2 = request.POST[f'option2_{i}']
            option3 = request.POST[f'option3_{i}']
            option4 = request.POST[f'option4_{i}']
            correct_option = int(request.POST[f'correct_option_{i}'])
            Question.objects.create(
                set_name=set_name,
                question_text=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_option=correct_option
            )
        return redirect('set_selection')
    return render(request, 'question_entry.html', {'set_name': set_name, 'num_questions': num_questions})

def question_view(request, question_id=1):
    questions = list(Question.objects.all())
    total_questions = len(questions)
    if question_id > total_questions or question_id < 1:
        return redirect('question_view', question_id=1)

    # Initialize timer
    if 'start_time' not in request.session:
        request.session['start_time'] = str(datetime.datetime.now())
        request.session['end_time'] = str(datetime.datetime.now() + datetime.timedelta(hours=3))
        request.session.modified = True

    question = questions[question_id - 1]
    saved_answer = request.session.get('answers', {}).get(str(question_id))

    if request.method == 'POST':
        form = QuestionForm(request.POST, question=question)
        if form.is_valid():
            selected_option = form.cleaned_data.get('option')
            if 'answers' not in request.session:
                request.session['answers'] = {}
            if selected_option:
                request.session['answers'][str(question_id)] = selected_option
            else:
                request.session['answers'].pop(str(question_id), None)
            request.session.modified = True
        if 'next' in request.POST:
            return redirect('question_view', question_id=question_id + 1)
        elif 'previous' in request.POST:
            return redirect('question_view', question_id=question_id - 1)
        elif 'submit' in request.POST:
            return redirect('result_view')
        elif 'mark_as_review' in request.POST:
            if 'review' not in request.session:
                request.session['review'] = []
            request.session['review'].append(str(question_id))
            request.session.modified = True
            return redirect('question_view', question_id=question_id + 1)
    else:
        form = QuestionForm(question=question, initial={'option': saved_answer})

    return render(request, 'question.html', {
        'question': question,
        'question_id': question_id,
        'total_questions': total_questions,
        'form': form,
        'start_time': request.session['start_time'],
        'end_time': request.session['end_time'],
        'answers': request.session.get('answers', {}),
        'review': request.session.get('review', [])
    })

def result_view(request):
    score = 0
    answers = request.session.get('answers', {})
    for question in Question.objects.all():
        selected_option = answers.get(str(question.id))
        if selected_option:
            if int(selected_option) == question.correct_option:
                score += 4
            else:
                score -= 1
    return render(request, 'result.html', {'score': score})
# def question_view(request, question_id=1):
#     questions = list(Question.objects.all())
#     total_questions = len(questions)
#     if question_id > total_questions or question_id < 1:
#         return redirect('question_view', question_id=1)

#     # Initialize timer
#     if 'start_time' not in request.session:
#         request.session['start_time'] = str(datetime.datetime.now())
#         request.session['end_time'] = str(datetime.datetime.now() + datetime.timedelta(hours=3))
#         request.session.modified = True

#     question = questions[question_id - 1]
#     saved_answer = request.session.get('answers', {}).get(str(question_id))

#     if request.method == 'POST':
#         form = QuestionForm(request.POST, question=question)
#         if form.is_valid():
#             selected_option = form.cleaned_data['option']
#             if 'answers' not in request.session:
#                 request.session['answers'] = {}
#             request.session['answers'][str(question_id)] = selected_option
#             request.session.modified = True
#             if 'next' in request.POST:
#                 return redirect('question_view', question_id=question_id + 1)
#             elif 'previous' in request.POST:
#                 return redirect('question_view', question_id=question_id - 1)
#             elif 'submit' in request.POST:
#                 return redirect('result_view')
#             elif 'mark_as_review' in request.POST:
#                 if 'review' not in request.session:
#                     request.session['review'] = []
#                 request.session['review'].append(str(question_id))
#                 request.session.modified = True
#                 return redirect('question_view', question_id=question_id + 1)
#     else:
#         form = QuestionForm(question=question, initial={'option': saved_answer})

#     return render(request, 'question.html', {
#         'question': question,
#         'question_id': question_id,
#         'total_questions': total_questions,
#         'form': form,
#         'start_time': request.session['start_time'],
#         'end_time': request.session['end_time'],
#         'answers': request.session.get('answers', {}),
#         'review': request.session.get('review', [])
#     })
print('Hello World!')