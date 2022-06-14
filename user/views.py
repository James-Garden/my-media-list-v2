from datetime import date, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from utils.shortcuts import redirect_next
from .forms import SignUpForm, EditProfileForm
from .models import User
from utils.messages import notice
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


class LoginForm(LoginView):
    template_name = 'user/login.html'
    next_page = 'user/profile.html'


def register(request):
    if request.user.is_authenticated:
        notice(request, 'warning', 'Already logged in.')
        return redirect(reverse('user:profile'))
    # When the user clicks 'submit'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            raw_password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('user:profile'))
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
            return redirect(reverse('user:login'))
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
        return redirect_next(reverse('user:login'), reverse('user:edit_profile'))

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            notice(request, "success", "Profile updated successfully")
            return redirect(reverse("user:edit_profile"))
    else:
        form = EditProfileForm(instance=current_user)
    return render(request, 'user/edit_profile.html', context={
        'form': form,
    })


def edit_account(request):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        return redirect_next(reverse('user:login'), reverse('user:edit_account'))

    if request.method == 'POST':
        if request.POST['form-type'] == 'password_form':
            password_form = PasswordChangeForm(current_user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                notice(request, "success", "Password updated successfully!")
                login(request, user)
                return redirect(reverse("user:edit_account"))
        elif request.POST['form-type'] == 'username_form':
            raise NotImplementedError

        elif request.POST['form-type'] == 'email_form':
            raise NotImplementedError
        else:
            notice(request, 'danger', 'Invalid form type!')
            password_form = PasswordChangeForm(current_user)
    else:
        password_form = PasswordChangeForm(current_user)

    return render(request, 'user/edit_account.html', context={
        'password_form': password_form,
    })


def delete_account(request):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        return redirect_next(reverse('user:login'), reverse('user:edit_account'))

    if request.method == 'GET':
        return redirect(reverse('user:login'))

    deletion_date = date.today() + timedelta(days=7)
    current_user.deletion_date = deletion_date
    current_user.marked_for_deletion = True
    current_user.save()
    print(current_user.marked_for_deletion)

    return render(request, 'user/deletion_confirmation.html', context={
        'deletion_date': deletion_date.strftime("%d %B %Y")
    })
