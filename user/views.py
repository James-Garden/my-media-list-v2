from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from utils.shortcuts import redirect_next
from user.forms import SignUpForm, EditProfileForm, UsernameChangeForm, EmailChangeForm
from user.models import User, FriendRequest
from utils.messages import notice


NAV_LINKS = {
    '/edit_profile': 'Profile',
    '/edit_account': 'Account',
}


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
            if request.user.marked_for_deletion:
                notice(request, "warning",
                       f"Your account will be deleted on {request.user.deletion_date.strftime('%d %B %Y')}.")
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
        form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            notice(request, "success", "Profile updated successfully")
            return redirect(reverse("user:edit_profile"))
    else:
        form = EditProfileForm(instance=current_user)

    return render(request, 'user/edit_profile.html', context={
        'form': form,
        'settings_nav_links': NAV_LINKS,
        'path': request.path,
    })


def edit_account(request):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        return redirect_next(reverse('user:login'), reverse('user:edit_account'))

    password_form = PasswordChangeForm(current_user)
    username_form = UsernameChangeForm(instance=current_user)
    email_form = EmailChangeForm(instance=current_user)

    if request.method == 'POST':
        if request.POST['form-type'] == 'password_form':
            password_form = PasswordChangeForm(current_user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                notice(request, "success", "Password updated successfully!")
                login(request, user)
                return redirect(reverse("user:edit_account"))
        elif request.POST['form-type'] == 'username_form':
            username_form = UsernameChangeForm(request.POST, instance=current_user)
            if username_form.is_valid():
                user = username_form.save()
                notice(request, "success", "Username updated successfully!")
                login(request, user)
                return redirect(reverse("user:edit_account"))
        elif request.POST['form-type'] == 'email_form':
            email_form = EmailChangeForm(request.POST, instance=current_user)
            if email_form.is_valid():
                user = email_form.save()
                notice(request, "success", "Email updated successfully!")
                login(request, user)
                return redirect(reverse("user:edit_account"))
        else:
            notice(request, 'danger', 'Invalid form type!')

    return render(request, 'user/edit_account.html', context={
        'password_form': password_form,
        'username_form': username_form,
        'email_form': email_form,
        'marked_for_deletion': current_user.marked_for_deletion,
        'settings_nav_links': NAV_LINKS,
        'path': request.path,
    })


@login_required
def delete_account(request):
    current_user = request.user

    if request.method == 'GET':
        if current_user.marked_for_deletion:
            return render(request, 'user/deletion_confirmation.html', context={
                'deletion_date': current_user.deletion_date.strftime("%d %B %Y")
            })
        else:
            return redirect(reverse("user:edit_account"))

    if not current_user.marked_for_deletion:
        current_user.schedule_deletion()
    else:
        current_user.cancel_deletion()
        notice(request, "success", "Your account will no longer be deleted!")

    return redirect(reverse("user:delete_account"))


@login_required
def add_friend(request, username):
    return_url = redirect(request.META.get('HTTP_REFERER', '/'))
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        notice(request, "warning", "This user does not exist")
        return return_url
    if request.user.friends.filter(user=recipient).exists():
        notice(request, "info", "You are already friends with this user!")
        return return_url
    if request.user.send_friend_request(recipient):
        notice(request, "success", "Friend request sent!")
        return return_url
    else:
        notice(request, "warning", "You have already sent a friend request to this user!")
        return return_url


@login_required
def cancel_friend_request(request, username):
    return_url = redirect(request.META.get('HTTP_REFERER', '/'))
    try:
        f_request = FriendRequest.objects.get(from_user=request.user, to_user=User.objects.get(username=username))
        f_request.delete()
        notice(request, "success", "Friend request cancelled.")
    except FriendRequest.DoesNotExist:
        notice(request, "warning", "There is no existing friend request to this user!")
    except User.DoesNotExist:
        notice(request, "warning", "This user does not exist.")
    finally:
        return return_url


@login_required
def remove_friend(request, username):
    return_url = redirect(request.META.get('HTTP_REFERER', '/'))
    try:
        friend = request.user.friends.get(username=username)
        request.user.unfriend(friend)
        notice(request, "info", f"Removed {friend.username} from your friends list.")
    except User.DoesNotExist:
        notice(request, "warning", "You are not friends with this user.")
    return return_url


@login_required
def friend_requests(request):
    recv_requests = FriendRequest.objects.filter(to_user=request.user)
    send_requests = FriendRequest.objects.filter(from_user=request.user)
    return render(request, "user/friend_requests.html", context={

    })
