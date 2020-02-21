from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
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
from social_django.utils import load_strategy
from .forms import MyUserCreationForm, GroupChoiceForm
from .tokens import account_activation_token

# Sign Up View
def register(request):
    # If POSTing i.e. creating a new user
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            # Get user, but don't set active before email validation
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Get the group of the user
            user_group = form.cleaned_data.get('sign_up_as')
            if user_group == 'developer':
                developers = Group.objects.get(name='Developer')
                user.groups.add(developers)
            elif user_group == 'player':
                players = Group.objects.get(name='Player')
                user.groups.add(players)
            else:
                raise FieldError()
            # Send email to user (to console) with a link to activation, then redirect with success-message
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
    # If GETting, render a User creation form
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Activate User View. Gets called when user follows the link provided in the validation email. Activates the profile
def activate(request, uidb64, token):

    # Methos should always be GET
    if request.method == 'GET':
        # Try getting the user based on the id
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        
        # If user is found and the token is correct, activate the account and log in
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account has been verified.'))
            return redirect('../../../../')
        
        # If user not found or bad token, redirect back to register 
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')

# Group Choice View. Gets called when users are registered trough Facebook in order to choose User-group.
def group_choice(request):

    # If POSTing, pass the choice to session variables. 
    if request.method == 'POST':
        form = GroupChoiceForm(request.POST)
        if form.is_valid():
            user_group = form.cleaned_data.get('sign_up_as')
            request.session['group'] = user_group
            # Redirect to complete registration according to social-auth pipeline.
            return redirect('/../../social-auth/complete/facebook')
    # If GETting render a GroupChoiceForm.
    else:
        form = GroupChoiceForm()
    return render(request, 'registration/group_choice.html', {'form': form})

# Logout View. Logs user out and redirects to login with message.
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, ('You were succesfully logged out.'))
    return redirect('../login')
