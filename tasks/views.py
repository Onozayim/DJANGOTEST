from django.shortcuts import render, redirect
from django.http import HttpResponse
from assignments.models import Assignment
from .models import Task
from .forms import CreateTaskForm


def index(requet, assId):
    assignment = Assignment.objects.filter(id=assId, user_id=requet.user.id).first()

    if assignment is None:
        return HttpResponse("ASSIGNMENT NOT FOUND")

    tasks = Task.objects.filter(assignment=assignment.id, user_id=requet.user.id)

    for task in tasks:
        print(task)

    return render(requet, "tasks/index.html", {"assig": assignment, "tasks": tasks})


def createTask(request, assId):
    if request.method == "GET":
        form = CreateTaskForm()
        return render(request, "tasks/create.html", {"form": form})
    else:
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            assignment = Assignment.objects.filter(
                id=assId, user_id=request.user.id
            ).first()

            if assignment is None:
                return HttpResponse("ASSIGNMENT NOT FOUNjjD")

            commit = form.save(commit=False)
            commit.user = request.user
            commit.assignment = assignment
            commit.save()

            return redirect("tasks_index", assId=assId)
        else:
            return render(request, "tasks/create.html", {"form": form})
