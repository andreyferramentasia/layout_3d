from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm

# Create your views here.


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    pass

class UserRegisterView(CreateView):
    template_name = 'accounts/user_form_register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
