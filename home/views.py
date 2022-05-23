from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate


def index(request):
    user = authenticate(username='tes', password='password')
    return render(request, 'home/index.html', context={
        'user': user,
    })
