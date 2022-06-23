from django import template
from user.models import FriendRequest

register = template.Library()


@register.inclusion_tag('partials/user.html', takes_context=True)
def show_user(context, user):
    if user == context['current_user']:
        profile_type = 2
    elif user in context['current_user'].friends.all():
        profile_type = 1
    elif FriendRequest.objects.filter(from_user=context['current_user'], to_user=user):
        profile_type = 3
    else:
        profile_type = 0
    return {
        'user': user,
        'is_friend': profile_type,
    }
