from .forms import SignUpForm
from utils.messages import notice
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from re import match
from datetime import date, timedelta, datetime


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
        form_valid = form.is_valid()  # form.is_valid must be run to get form.cleaned_data
        username = form.cleaned_data.get('username')
        birth_date = form.cleaned_data.get('birth_date')
        valid_birth_date = date.today() - timedelta(weeks=676)
        if not match(r"^[A-Z][\w_]+$", str(username)):
            notice(request, "danger", "Username must start with a capital letter and be alphanumeric.")
        elif birth_date is None:
            notice(request, "danger", "Invalid input.")
        elif not (birth_date < valid_birth_date):
            notice(request, "danger", "You must be at least 13 years old.")
        elif form_valid:
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('user:profile'))
    # Load registration page
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})


def profile(request, username=None):
    if username is None:  # If the user has navigated to '/profile/'
        if request.user.is_authenticated:  # If the user is looking at their own profile
            profile_user = request.user
            is_current_user = True
        else:
            return HttpResponseRedirect(reverse('user:login'))
    else:  # If the user has navigated to '/profile/USERNAME'
        profile_user = get_object_or_404(User, username=username)
        is_current_user = False

    return render(request, 'user/profile.html', context={
        'profile': profile_user,
        'is_current_user': is_current_user,
    })


def edit_profile(request):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        notice(request, "danger", "You must be logged in to edit your profile!")
        return HttpResponseRedirect(reverse('user:login'))
    return render(request, 'user/edit_profile.html', context={
        'user': current_user,
    })
