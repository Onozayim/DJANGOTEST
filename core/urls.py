from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="core_index"),
    path("register/", views.register_view, name="core_register"),
    path("login/", views.login_view, name="core_login"),
    path("logout/", views.logout_view, name="core_logout")
]
