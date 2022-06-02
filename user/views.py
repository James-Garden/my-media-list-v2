from .forms import SignUpForm
from utils.messages import notice
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


class LoginForm(LoginView):
    template_name = 'user/login.html'
    next_page = 'user/profile.html'


def register(request):
    if request.user.is_authenticated:
        notice(request, 'warning', 'Already logged in.')
        return HttpResponseRedirect(reverse('user:profile'))
    # When the user clicks 'submit'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            pass
    # Load registration page
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})


def profile(request, username=None):
    if username is None:  # If the user has navigated to '/profile/'
        if request.user.is_authenticated:  # If the user is looking at their own profile
            profile_user = request.user

        else:
            return HttpResponseRedirect(reverse('user:login'))
    else:  # If the user has navigated to '/profile/USERNAME'
        profile_user = get_object_or_404(User, username=username)

    return render(request, 'user/profile.html', context={
        'profile': profile_user,
    })
