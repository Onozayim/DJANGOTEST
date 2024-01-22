from django.urls import path
from . import views

urlpatterns = [
    path("<int:assId>", views.index, name="tasks_index"),
    path("create/<int:assId>", views.createTask, name="tasks_create")
]
