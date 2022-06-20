from django.utils.timezone import now


def user_online_status(request):
    if request.user.is_authenticated:
        request.user.last_online = now()
        request.user.save()
    return {}
