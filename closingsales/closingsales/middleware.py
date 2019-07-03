import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from notification.models import Notification
from products.models import Category, Subcategory

def split_array_equally(arr, number_of_element):
    return [arr[i:i+number_of_element] for i in range(len(arr))[::number_of_element]]

def get_loginrequired_urls():
    return tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.required = get_loginrequired_urls()
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        if request.user.is_authenticated:
            return None

        for url in self.exceptions:
            if url.match(request.path):
                return None


        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)
        return None

class NotificationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.required = get_loginrequired_urls()

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == 'POST':
            return None

        for url in self.required:
            if url.match(request.path):
                user = request.user
                notification = Notification.notifications.unseen(user)
                view_kwargs['notification'] = notification
        return view_func(request, *view_args, **view_kwargs)

class CategoryMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.exception_paths = ['/admin/', '/dashboard/', '/api/', '/accounts', '/media']

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        for path in self.exception_paths:
            if request.path.startswith(path):
                return None
        
        main_categories = Category.objects.all().prefetch_related('subcategories')
        top_categories  = main_categories[:5]
        view_kwargs['main_categories'] = split_array_equally(main_categories, 4) 
        view_kwargs['top_categories'] = top_categories
        
        return view_func(request, *view_args, **view_kwargs)

        


