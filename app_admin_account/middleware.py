# app_admin_account/middleware.py
from django.shortcuts import redirect

class EmailVerifiedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return redirect('email_activation_sent')
        return self.get_response(request)
