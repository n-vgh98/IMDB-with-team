from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.cache import *


def login_user(request):
    if request.user.is_anonymous:
        if request.method == "GET":
            cache.set('next', request.GET.get('next', None))
            form = UserLoginForm()
            return render(request, 'users/registration/login.html', context={'form': form})
        elif request.method == "POST":
            user = authenticate(request, email=request.POST.get('email'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return HttpResponseRedirect(next_url)

                return redirect('movies_list')
            else:
                form = UserLoginForm()
                return render(request, 'users/registration/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('movies_list')


def signup(request):
    if request.user.is_anonymous:
        if request.method == "GET":
            signup_form = CustomUserCreationForm()
            return render(request, 'users/registration/sign_up.html',
                          context={'form': signup_form})
        elif request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(
                    request,
                    "User with this Email address already!!"
                )
                messages.success(
                    request,
                    "You're register successfully!"
                )
                return redirect('login')
            else:
                return redirect('signup')
