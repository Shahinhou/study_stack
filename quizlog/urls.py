from django.urls import include,path
from . import views

app_name = "quizlog"

urlpatterns = [

        path("", views.index, name="index"),
        path("quiz", views.quiz, name="quiz"),
        ]
