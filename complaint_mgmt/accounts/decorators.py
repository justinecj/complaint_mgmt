from functools import wraps
from django.shortcuts import redirect

# def admin_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.role != 'ADMIN':
#             return redirect('login')
#         return view_func(request, *args, **kwargs)
#     return wrapper

# def employee_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.role != 'EMPLOYEE':
#             return redirect('login')
#         return view_func(request, *args, **kwargs)
#     return wrapper



def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return redirect('dashboard') 
        return view_func(request, *args, **kwargs)
    return wrapper

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'EMPLOYEE':
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

