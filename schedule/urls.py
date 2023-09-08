from django.urls import include,path
from . import views

app_name = "schedule"

urlpatterns = [

        path("", views.index, name="index"),
        ]
