from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as login_
from django.contrib.auth import logout as logout_
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    users_ = get_user_model().objects.order_by("-pk")
    context = {
        "users_": users_,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login_(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def update(request, pk):
    user = get_user_model().objects.get(id=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", user.id)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        "form": form,
        "user": user,
    }
    return render(request, "accounts/update.html", context)


@login_required
def logout(request):
    logout_(request)
    return redirect("accounts:index")
