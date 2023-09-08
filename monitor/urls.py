from django.urls import include,path
from . import views

app_name = "monitor"

urlpatterns = [

        path("", views.index, name="index"),
        path("edit/<str:name>", views.edit, name="edit"),

        ]
