# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from app.models import User_ConfirmationHash


def reset_password_cont(request, hash):
    invalid_hash = False
    errors = []
    uch = None
    email = ''
    try:
        uch = User_ConfirmationHash.objects.filter(type='reset-password', hash=hash).get()
        email = uch.user.email
    except ObjectDoesNotExist:
        invalid_hash = True
    if uch is not None and request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) == 0:
            errors.append('Nie podano hasła.')
        elif len(password) < 6:
            errors.append('Za krótkie hasło. Przynajmniej 6 znaków.')
        elif password != password2:
            errors.append('Podane hasła nie są identyczne.')
        if len(errors) == 0:
            uch.user.set_password(password)
            uch.user.save()
            uch.delete()
            request.session['changed_password'] = True
            return redirect('sign_in')
    return render(request, 'reset_password.html', {
        "hash": hash,
        "invalid_hash": invalid_hash,
        "errors": errors,
        "email": email
    })