from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UserRegistration(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    # reverse_lazy is used to delay the reverse lookup until the view is called.
    # reverse_lazy is used in class based views and object, reverse is used in function based views and string.
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        customer = form.save()
        messages.success(self.request, 'Account Created Successfully!')
        login(self.request, customer)
        # here we use super() to call the parent class method form_valid() and pass the form as an argument. that means form_valid calls itself recursively.
        return super().form_valid(form)


class UserLogin(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
class UserLogout(LogoutView):
    template_name = ''

    def get_success_url(self):
        logout(self.request)
        return reverse_lazy('login')