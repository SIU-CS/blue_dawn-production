from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from templates.form import RegistrationForm
from login.tokens import accountActivation
from django.core.mail import EmailMessage

def login(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate you account'
            message = render_to_string('registration/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': accountActivation.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            return redirect('email_activation_sent')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


def email_activation_sent(request):
    return render(request, 'registration/email_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and accountActivation.check_token(user, token):
        user.is_active = True
        user.confirm.confirmation = True
        user.save()
        login(request)
        return redirect('activation_complete')
    else:
        return render(request, 'signup.html')


def activation_complete(request):
    return render(request, 'registration/activation_complete.html')
