from django.shortcuts import redirect
from django.http import HttpResponse
from .views import *


def allowed_roles(allowed_role=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = str(request.user.groups.get())

            if group in allowed_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')

        return wrapper

    return decorator


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

