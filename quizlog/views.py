from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from daily_stack.models import *

# Create your views here.

class questionForm(forms.Form):

    title = forms.CharField(max_length=100, label="Name of subject pertaining to question\n")

    content = forms.CharField(widget=forms.Textarea, label="Question:\n")
    answer = forms.CharField(widget=forms.Textarea, label="Answer:\n")


def index(request):
    
    errors = []
    try:
        stack = Stack.objects.get(user=request.user.id)

    except Stack.DoesNotExist:
        print('stackless')

        stack = Stack(user=request.user)
        stack.save()

    # view comments or add comments.

    if request.method=='POST':

        form = questionForm(request.POST)

        if form.is_valid():
            content = request.POST['content']
            title = request.POST['title']
            answer = request.POST['answer']
            question = Question(title=title, content=content, answer=answer)
            question.save()

            stack.questions.add(question)
            stack.save()

    questions = stack.questions.all()

    return render(request, 'quizlog/index.html', {

        'questions': questions,
        'errors':errors,
        'form': questionForm(),
        })

def quiz(request):
    try:
        stack = Stack.objects.get(user=request.user.id)

    except Stack.DoesNotExist:
        print('stackless')

        stack = Stack(user=request.user.id)

    # view comments or add comments.

    if request.method=='POST' and 'remove' in request.POST:
        qid = request.POST['remove']
        #print(qid)
        q = Question.objects.get(pk=qid)
        print(q.title)
        stack.remove_question(q)
        #stack.remove_question(request.POST['remove'])

    questions = stack.questions.all()
    return render(request, 'quizlog/quiz.html', {
        'questions':questions,
        })

