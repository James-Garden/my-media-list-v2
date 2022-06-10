from django.shortcuts import redirect
from urllib.parse import urlencode


def redirect_next(url, url_next):
    return redirect(f"{url}?{urlencode({'next': url_next})}")
