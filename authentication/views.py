from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import MyUserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_group = form.cleaned_data.get('sign_up_as')
            if user_group == 'developer':
                developers = Group.objects.get(name='Developer')
                user.groups.add(developers)
            elif user_group == 'player':
                developers = Group.objects.get(name='Player')
                user.groups.add(developers)
            else:
                raise FieldError()
                
            user_authenticated = authenticate(username=username, password=password)
            login(request, user_authenticated)
            return redirect('../../gameLibrary/')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form' : form})

def logout(request):
    auth.logout(request)
    return render(request, 'registration/logout.html')

