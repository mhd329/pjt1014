from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as login_
from django.contrib.auth import logout as logout_
from django.contrib.auth.decorators import login_required


# Create your views here.
def users(request):
    users_ = get_user_model().objects.order_by("-pk")
    context = {
        "users_": users_,
    }
    return render(request, "accounts/users.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:users")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login_(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:users')
    else:
        form = AuthenticationForm()
    context = {'form' : form}
    return render(request, 'accounts/login.html', context)