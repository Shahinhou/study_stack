from django.shortcuts import render,redirect
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json
from daily_stack.models import *
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your views here.

class monitorForm(forms.Form):

    name = forms.CharField(max_length=100, label="Name of module studied")
    hours = forms.FloatField(label="Hours spent (decimal)")

class editForm(forms.Form):

    sessions = forms.IntegerField(label="Sessions logged")
    hours = forms.FloatField(label="Hours spent (decimal)")


def index(request):

    try:
        stack = Stack.objects.get(user=request.user.id)
    
    except Stack.DoesNotExist:
        print('stackless')
        # get name

        return redirect('daily_stack:index')
    
    if stack.monitor == "none":
        stack.monitor = json.dumps({})
    monitor = json.loads(stack.monitor)

    if request.method == 'POST' and 'edit' in request.POST:
        print(request.POST)
        form = editForm(request.POST)

        if form.is_valid:
            name = request.POST['edit']
            sessions = request.POST['sessions']
            hours = request.POST['hours']
            monitor[name] = {'hours': hours, 'sessions': sessions}
            print(monitor)
    
    elif request.method == 'POST' and 'remove' in request.POST:
        name = request.POST['remove']
        del monitor[name]


    elif request.method == 'POST':
        print(request.POST)

        form = monitorForm(request.POST)

        if form.is_valid():

            name = request.POST['name']
            hours = request.POST['hours']

            if name not in monitor:
                monitor[name] = {'hours': 0, 'sessions': 0}

            monitor[name]['hours'] += float(hours)
            monitor[name]['sessions'] += 1

    stack.monitor = json.dumps(monitor)
    stack.save()

    print(monitor)

    return render(request, 'monitor/index.html', {

        'monitor':monitor,
        'form': monitorForm(),
        })


def edit(request, name):

    if request.method=="POST":
        print('error')

    return render(request, 'monitor/edit.html', {
        'form': editForm(),
        'name': name,
        })


