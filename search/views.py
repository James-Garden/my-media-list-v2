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
    results_per_page = 10
    if 'page' in request.GET:
        try:
            offset = (int(request.GET['page']) - 1) * results_per_page
            if offset < 0:
                raise ValueError
        except ValueError:
            notice(request, "warning", "Invalid page number. Showing first page of results.")
            offset = 0
    else:
        offset = 0
    users = User.objects.filter(username__icontains=query)[offset:offset+results_per_page]
    total_results = User.objects.filter(username__icontains=query).count()
    pages = int(total_results // results_per_page) + (total_results % results_per_page > 0)
    return render(request, 'search/user_search.html', context={
        'query': query,
        'users': users,
        'current_user': request.user,
        'page': offset // 10 + 1,
        'pages': range(1, pages+1),
        'total_pages': pages,
        'results_per_page': results_per_page,
        'type': 'users',
    })
