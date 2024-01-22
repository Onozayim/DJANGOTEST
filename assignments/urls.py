from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ass_index"),
    path("create", views.create, name="ass_create")
]
