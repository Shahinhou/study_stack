from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.forms import ModelForm

# Create your views here.

class DateInput(forms.DateInput):
    input_type='date'

class assignmentForm(forms.Form):
    name = forms.CharField(label="Assignment name")
    due_date = forms.DateField(label="Due date", widget=DateInput())
    difficulty = forms.IntegerField(label="Difficulty (1-5)", validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        widgets = {
                'due_date': DateInput(),
                }


#class removeForm(forms.Form):

def today():
    year,month,day = str(datetime.datetime.now()).split()[0].split('-')
    return year,month,day


def index(request):
    
    year,month,day = today()
    try:
        stack = Stack.objects.get(user=request.user.id)

    except Stack.DoesNotExist:
        print('stackless')

        stack = Stack(user=request.user)
        stack.save()
        assignments = stack.assignments.all()
        
        return render(request, "daily_stack/index.html", {
            "stack":assignments,
            "form":assignmentForm(),
            'day': day,
            'month': month,
            'year': year,
                })
    
    if request.method=="POST" and "remove_btn" not in request.POST:

        form = assignmentForm(request.POST)

        

        if form.is_valid():
            name = request.POST.get('name')
            due_date = request.POST.get('due_date')
            difficulty = request.POST.get('difficulty')

            a = Assignment(name=name,due_date=due_date,difficulty=difficulty)
            a.save()

         
            # don't repeat code. re-structure later.

            stack.assignments.add(a)
            stack.save()

            assignments = stack.assignments.all()
            warning = {assignments[0]: assignments[0].days_away(year,month,day)}
            
            return render(request, "daily_stack/index.html", {
                "form": assignmentForm(),
                "stack":assignments,
                'day': day,
                'month': month,
                'year': year,
                'warning': warning,
                })
        
        elif request.method=="POST" and "remove_btn" in request.POST:
            pass
            # do something

        else:
            warning = {assignments[0]: assignments[0].days_away(year,month,day)}
            return render(request, "daily_stack/index.html", {
                "form": assignmentForm(),
                "stack":assignments,
                'day': day,
                'month': month,
                'year': year,
                'warning': warning,
                })
    
    assignments = stack.assignments.all()
    if len(assignments) == 0:
        return render(request, "daily_stack/index.html", {
            "stack":assignments,
            "form":assignmentForm(),
            'day': day,
            'month': month,
            'year': year,
                })

    assignments = (stack.list_assignments())
    warning = {assignments[0]: assignments[0].days_away(year,month,day)}

   
    return render(request, "daily_stack/index.html", {
        "form": assignmentForm(),
        "stack":assignments,
        'day': day,
        'month': month,
        'year': year,
        'warning': warning,
        })

def assignment(request, assignment_id):

    year,month,day = today()

    assignment = Assignment.objects.get(pk=assignment_id)
    stack = Stack.objects.get(user=request.user.id)

    total = assignment.days_away(year,month,day)

    if request.method=="POST":
        print("posting")
        stack.remove_assignment(assignment)
        return redirect("daily_stack:index")

    
    return render(request, "daily_stack/assignment.html",{
        "assignment":assignment,
        'day': day,
        'month': month,
        'year': year,
        'days_away':total,
        })


