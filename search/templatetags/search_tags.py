from django import template

register = template.Library()


@register.inclusion_tag('partials/user.html')
def show_user(user):
    return {'user': user}
