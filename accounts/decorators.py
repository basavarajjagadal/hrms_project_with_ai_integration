from django.shortcuts import redirect


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role == "admin":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper


def hr_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role == "hr":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper


def employee_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role == "employee":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper