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
    return render(request, 'registration/login.html')

#New user registration
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save user user in the database, but the user won't be active 
            user = form.save(commit=False)
            # assign user's activation to not active
            user.is_active = False
            user.save()
            # to get current web page
            current_site = get_current_site(request)

            #sending email to user for activation
            # subject of the email
            # message get the text in "email_activation.html" and render it to string to send it to the user
            # args: current user, current page, token (token for unique url that sent to the user)
            subject = 'Activate you account'
            message = render_to_string('registration/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': accountActivation.make_token(user),
            })
            #get the current user email
            to_email = form.cleaned_data.get('email')

            #args: subject of the email, content of the email, and the user's email
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

#unique url for activation
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        #getting current user by id
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    #check the user and the toekn that sent to the user
    #if so, activate the user account in the database
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
