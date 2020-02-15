from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.views.generic import View, UpdateView
from .forms import MyUserCreationForm, GroupChoiceForm
from .tokens import account_activation_token

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_group = form.cleaned_data.get('sign_up_as')
            if user_group == 'developer':
                developers = Group.objects.get(name='Developer')
                user.groups.add(developers)
            elif user_group == 'player':
                players = Group.objects.get(name='Player')
                user.groups.add(players)
            else:
                raise FieldError()
            current_site = get_current_site(request)
            subject = 'Activate Your GameX-Account'
            message = render_to_string('../templates/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return redirect('login')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):

    if request.method == 'GET':
        try:
            #uidb64 = request.GET.get('uidb64', '')
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('../../../../')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')


def group_choice(request):

    if request.method == 'POST':
        user_group = request.POST.get('sign_up_as')
        request.session['group'] = user_group
        return redirect(reverse('social:complete'))
    else:
        form = GroupChoiceForm()
    return render(request, 'registration/group_choice.html', {'form': form})


def logout(request):
    auth_logout(request)
    return render(request, 'registration/logout.html')
