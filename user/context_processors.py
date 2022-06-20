from django.utils.timezone import now


def settings_nav_links(request):
    nav_links = {
        '/edit_profile': 'Profile',
        '/edit_account': 'Account',
    }
    return {'settings_nav_links': nav_links}


def user_online_status(request):
    if request.user.is_authenticated:
        request.user.last_online = now()
        request.user.save()
    return {}
