from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

login_view = auth_views.LoginView.as_view()

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout')
]