from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
from utils.messages import notice


def index(request):
    valid_types = ['all', 'books', 'films', 'tv', 'users']
    if 'type' not in request.GET or request.GET['type'] not in valid_types or 'query' not in request.GET:
        notice(request, 'warning', 'Unexpected search type or query.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    search_type = request.GET['type']
    query = request.GET['query']
    if search_type == 'all':
        raise NotImplementedError
    elif search_type == 'books':
        raise NotImplementedError
    elif search_type == 'films':
        raise NotImplementedError
    elif search_type == 'tv':
        raise NotImplementedError
    elif search_type == 'users':
        return user_search(request, query)

    return HttpResponse("search page")


def user_search(request, query: str) -> HttpResponse:
    users = User.objects.filter(username__icontains=query)[:10]
    return render(request, 'search/user_search.html', context={
        'query': query,
        'users': users,
        'current_user': request.user,
    })
