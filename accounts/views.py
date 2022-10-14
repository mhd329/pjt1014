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
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def update(request, pk):
    me = request.user
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
        "me": me,  # 내가 보려는 정보가 다른 사람의 회원 정보이면 수정을 할 수 없게 하기위해 받아오는 변수, 지금 구현할 기능은 아니고 템플릿에도 포함되지 않음
    }
    return render(request, "accounts/update.html", context)
