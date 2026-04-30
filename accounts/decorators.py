from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(expected_role):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user_role = getattr(getattr(request.user, "profile", None), "role", None)
            if user_role != expected_role:
                return redirect("role-dashboard")
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
