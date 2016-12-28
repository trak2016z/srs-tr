# -*- coding: utf-8 -*-
import os
import re

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse

from app import settings
from app.models import User, User_ConfirmationHash
from app.settings import BASE_DIR
from app.utils.captcha import Captcha
from app.utils.hash import generate_unique_hash
from app.utils.sender import send_email


def sign_up_cont(request):
    created = request.session.get('created-account', False)
    if created:
        del request.session['created-account']
    errors = []
    captcha = Captcha(request, "sign_up")
    email = ''
    first_name = ''
    last_name = ''
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        if len(first_name) == 0:
            errors.append('Nie podano imienia.')
        elif len(first_name) < 3:
            errors.append('Za krótkie imie.')
        last_name = request.POST.get('last_name', '')
        if len(last_name) == 0:
            errors.append('Nie podano nazwiska.')
        elif len(last_name) < 3:
            errors.append('Za krótkie nazwisko.')
        email = request.POST.get('email', '')
        if len(email) == 0:
            errors.append('Nie podano adresu email.')
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            errors.append('Format adresu email jest nieprawidłowy.')
        elif User.objects.filter(email=email).count() > 0:
            errors.append('Istnieje konto z takim adresem email.')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if len(password) == 0:
            errors.append('Nie podano hasła.')
        elif len(password) < 6:
            errors.append('Za krótkie hasło. Przynajmniej 6 znaków.')
        elif password != password2:
            errors.append('Podane hasła nie są identyczne.')
        captcha_value = request.POST.get('captcha', '')
        if len(captcha_value) == 0:
            errors.append('Nie podano kodu.')
        elif not captcha.is_valid(captcha_value):
            errors.append('Podany kod jest nieprawidłowy.')
        if len(errors) == 0:
            u = User()
            u.email = email
            u.set_password(password)
            u.first_name = first_name
            u.last_name = last_name
            u.save()
            file = open(os.path.join(BASE_DIR, 'app', 'utils', 'email-forms', 'create-account.txt'), 'r')
            hash = generate_unique_hash('create-account')
            message = file.read().decode('utf8')
            domain_url = ''.join(['http://', get_current_site(request).domain])
            active_url = reverse('activate_account', kwargs={'hash': hash})
            message = message.replace('URL_CONFIRMATION', domain_url + active_url)
            uch = User_ConfirmationHash.objects.create(user=u, type='create-account', hash=hash)
            send_email(u.email, 'Aktywacja konta', message)
            request.session['created-account'] = True
            return redirect('sign_up')
    return render(request, 'sign_up.html', {
        'captcha_url': captcha.url,
        'captcha_max': settings.CAPTCHA_LENGTH,
        'created': created,
        'errors': errors,
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    })


def activate_account_cont(request, hash):
    uch = User_ConfirmationHash.objects.filter(type='create-account', hash=hash).get()
    if uch is not None:
        uch.user.active = True
        uch.user.save()
        uch.delete()
        request.session['activated-account'] = True
    return redirect('sign_in')