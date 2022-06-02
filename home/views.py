from django.shortcuts import render
from utils.messages import notice


def index(request):
    return render(request, 'home/index.html')
