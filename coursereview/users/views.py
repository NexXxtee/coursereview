from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginUserForm

def user_logout(request):
    """Logout view"""
    logout(request)
    return redirect('users:login')


class LoginUser(LoginView):
    """Login view"""
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return self.request.GET.get('next', '/')