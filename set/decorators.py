from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def set_required(view_func):
    """
    Only allow users with role='set' to access a view.
    Others will be redirected to 'access_denied' page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, "Please log in first.")
            return redirect("login")

        if user.role != "set" and not user.is_superuser:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("access_denied")

        return view_func(request, *args, **kwargs)
    return wrapper
