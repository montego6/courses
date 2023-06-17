from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .forms import UserLoginForm


urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=UserLoginForm), name='login')
]