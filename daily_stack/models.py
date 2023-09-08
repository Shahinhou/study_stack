from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

def key(a):

    x,y,z = a.date_to_int()
    return int(x+y+z)

class Assignment(models.Model):

    due_date = models.DateField(auto_now=False,auto_now_add=False)
    assigned_date = models.DateField(auto_now_add=True)
    difficulty = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    name = models.CharField(max_length=100, default="essay")

    def date_to_int(self):
        return str(self.due_date).split('-')

    def days_away(self,year,month,day):
        
        # breaks don't repeat rule, but is faster time complexity than "if" checking for every loop.
        d = {1: 31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        d_leap = {1: 31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        
        if int(year) % 4 == 0:
            selected = d_leap
        else:
            selected = d
        
        # c pointers would've been useful here.

        xyear, xmonth, xday = self.date_to_int()

        print(f'{xyear} - {year}, {xmonth} - {month}, {xday} - {day}')

        total = int(xday) - int(day)

        i = int(month)
        while i < int(xmonth):
            total += selected[i]
            print(total)

        total += 365 * (int(xyear) - int(year))

        print(f'days away: {total}')
        return total

    def __str__(self):
        return self.name

class Question(models.Model):

    title = models.CharField(max_length=100,default="Mathematics")
    content = models.TextField(max_length=1000,default="none")
    date = models.DateField(auto_now_add=True)
    answer =models.TextField(max_length=1000,default="none")


    def __str__(self):
        return str(self.title)


class Stack(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    assignments = models.ManyToManyField(Assignment)
    questions = models.ManyToManyField(Question)
    monitor = models.TextField(max_length=1000,default="none")

    def remove_assignment(self, a):
        self.assignments.remove(a)
    
    def remove_question(self, q):
        self.questions.remove(q)

    def list_assignments(self):
        assignments = sorted(self.assignments.all(),key=key)
        return assignments



class Course(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    name = models.CharField(max_length=100, default="none")
    timetable = models.TextField(max_length=1000, default="course list goes here")
    offline_schedule = models.TextField(max_length=100000, default='json here')

    def __str__(self):
        return str(self.name)
