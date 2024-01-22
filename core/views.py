from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthForm
from django.contrib.auth import login, authenticate, logout


@login_required
def index(request):
    print(request.path)
    return render(request, "index.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core_index")

    if request.method == "GET":
        form = CustomUserCreationForm()

        return render(request, "register.html", {"form": form})
    else:
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core_index")
        else:
            errors = form.errors.values()
            return render(request, "register.html", {"form": form, "errors": errors})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core_index")

    if request.method == "GET":
        form = CustomAuthForm()
        return render(request, "login.html", {"form": form})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            form = CustomAuthForm()
            return render(
                request,
                "login.html",
                {"form": form, "error": "Nombre de usuario o contraseña incorrectas"},
            )

        login(request, user)
        return redirect("core_index")


def logout_view(request):
    logout(request)

    return redirect("core_login")
