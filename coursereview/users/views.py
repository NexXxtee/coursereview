from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from coursereview import settings
from django.urls import reverse, reverse_lazy


def user_logout(request):
    """Logout view"""
    logout(request)
    return redirect('users:login')


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    
    def form_valid(self, form):
    # Указал явно, так как Джанго ругается на бекенд аутентификации без него 
        """Process valid form data."""
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'


    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    

