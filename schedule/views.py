from django.shortcuts import render
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json

from django.contrib.auth.models import User
from daily_stack.models import *
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your views here.

class courseNameForm(forms.Form):
    name = forms.CharField(label="Course Name: ")

def index(request):

    schedule ={}
    
    try:
        course = Course.objects.get(user=request.user.id)
    
    except Course.DoesNotExist:
        print('courseless')

        course = Course(user=request.user)
        course.save()
        # get name

        return render(request, 'schedule/index.html',{
            # set default course name to none, let html check for none.
            'course': course,
            'form': courseNameForm(),
            })
    
    if request.method=="POST" and 'reset_name' in request.POST:
        course.name = 'none'
        course.save()

    elif request.method=="POST" and 'offline' in request.POST:

        schedule = json.loads(course.offline_schedule)


    elif request.method=="POST":

        # get schedule
        if 'get_schedule_from_model' in request.POST:
            name = course.name
        else:
            name = request.POST['name']
        
        today = str(datetime.datetime.now()).split()[0]
        today = '2023-9-11' # comment this out when done testing.
        url = f"https://mytimetable.dcu.ie/timetables?date={today}&view=week&timetableTypeSelected=241e4d36-60e0-49f8-b27e-99416745d98d"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.get(url)

        search_bar = driver.find_elements(By.ID, "mat-input-0")[0]

        search_bar.clear()
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.RETURN)
        #print(driver.current_url)

        box = driver.find_elements(By.TAG_NAME, "mat-pseudo-checkbox")[0]
        print(box)
        box.click()
        print(driver.current_url)

        appointments = driver.find_elements(By.CLASS_NAME, "e-appointment")
        
        for a in appointments:
            #print(a)
            lesson,b = (a.get_attribute('aria-label')).split(maxsplit=1)
            #print(b)

            #p1 = 'Begin From '
            #c = re.sub(p1, '', b[0])

            day = b.split()[2]
            print(day)
            #print(lesson)
            p2 = r'\d*\d:\d\d:\d\d'
            begin, end = re.findall(p2, b)
            #print(begin, end)
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(f'{lesson} ({begin} - {end})')

        print(schedule)

        course.offline_schedule = json.dumps(schedule)

        course.name = name
        course.save()
 


    return render(request, 'schedule/index.html', {

        'course':course,
        'form':courseNameForm(),
        'schedule':schedule,
        })
    

    
