from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm
from .tokens import account_activation_token

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            #login(request, user)
            return redirect('confirmation')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})



def confirmation(request):

    return render(request, 'confirmation.html')

