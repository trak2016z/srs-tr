# -*- coding: utf-8 -*-
import os
import re

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import User, User_ConfirmationHash
from app.utils.captcha import Captcha
from app.utils.hash import generate_unique_hash
from app.utils.sender import send_email
from srs import settings
from srs.settings import BASE_DIR


def forgotten_password_cont(request):
    sended = request.session.get('sended-email', False)
    if sended:
        del request.session['sended-email']
    errors = []
    captcha = Captcha(request, "forgotten_password")
    if request.method == 'POST':
        email = request.POST.get('email')
        captcha_value = request.POST.get('captcha')
        if len(email) == 0:
            errors.append('Nie podano adresu email.')
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            errors.append('Format adresu email jest nieprawidłowy.')
        elif User.objects.filter(email=email).count() == 0:
            errors.append('Nie istnieje konto z takim adresem email.')
        if len(captcha_value) == 0:
            errors.append('Nie podano kodu.')
        elif not captcha.is_valid(captcha_value):
            errors.append('Podany kod jest nieprawidłowy.')
        if len(errors) == 0:
            file = open(os.path.join(BASE_DIR, 'app', 'utils', 'email-forms', 'reset-password.txt'), 'r')
            hash = generate_unique_hash('reset-password')
            message = file.read().decode('utf8')
            domain_url = ''.join(['http://', get_current_site(request).domain])
            active_url = reverse('reset_password', kwargs={'hash': hash})
            message = message.replace('URL_SITE', settings.SITE_TITLE)
            message = message.replace('URL_CONFIRMATION', domain_url + active_url)
            u = User.objects.filter(email=email).get()
            uch = None
            try:
                uch = User_ConfirmationHash.objects.filter(user=u,type='reset-password').get()
            except ObjectDoesNotExist:
                uch = User_ConfirmationHash()
                uch.user = u
                uch.type = 'reset-password'
            uch.hash = hash
            uch.save()
            send_email(u.email, 'Resetowanie hasła', message)
            request.session['sended-email'] = True
            return redirect('forgotten_password')
    return render(request, 'forgotten_password.html', {
        "captcha_url": captcha.url,
        "captcha_max": settings.CAPTCHA_LENGTH,
        "sended": sended,
        "errors": errors
    })