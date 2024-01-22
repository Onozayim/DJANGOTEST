from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateAssignmentForm
from .models import Assignment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# ASSINGMENTS VIEWS


def index(request):
    title = request.GET.get("titulo")

    if title:
        assignments = Assignment.objects.filter(user=request.user).filter(
            title__icontains=title
        )
    else:
        assignments = Assignment.objects.filter(user=request.user)

    paginator = Paginator(assignments, 5)
 
    try:
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "ass/index.html", {"page_obj": page_obj})
    except EmptyPage:
        return HttpResponse("ERROR")
    except PageNotAnInteger:
        return HttpResponse("ERROR")


def create(request):
    if request.method == "GET":
        form = CreateAssignmentForm(user=request.user)
        return render(request, "ass/create.html", {"form": form})
    else:
        form = CreateAssignmentForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            commit = form.save(commit=False)
            commit.user = request.user
            commit.save()

            return redirect("ass_index")
        else:
            return render(request, "ass/create.html", {"form": form})


def detail(request):
    return HttpResponse("HOLA")
