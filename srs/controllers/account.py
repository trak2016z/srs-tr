# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.models import User


@login_required
def change(request):
    update_errors = []
    update_success = request.session.get('update_success', False)
    if update_success:
        del request.session['update_success']
    user = User.objects.filter(id=request.user.id).get()
    first_name = user.first_name
    last_name = user.last_name
    if request.method == 'POST' and request.POST.get('update'):
        first_name = request.POST.get('first_name')
        if len(first_name) == 0:
            update_errors.append('Nie podano imienia.')
        elif len(first_name) < 3:
            update_errors.append('Za krótkie imie.')
        last_name = request.POST.get('last_name')
        if len(last_name) == 0:
            update_errors.append('Nie podano nazwiska.')
        elif len(last_name) < 3:
            update_errors.append('Za krótkie nazwisko.')
        if len(update_errors) == 0:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            request.session['update_success'] = True
            return redirect('account.change')
    return render(request, 'account/change.html', {
        "first_name": first_name,
        "last_name": last_name,
        "update_errors": update_errors,
        "update_success": update_success,
    })


@login_required
def change_password(request):
    cp_errors = []
    cp_success = request.session.get('cp_success', False)
    if cp_success:
        del request.session['cp_success']
    if request.method == 'POST' and request.POST.get('change-password'):
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')
            user = User.objects.filter(id=request.user.id).get()
            if user.check_password(password):
                if len(new_password) == 0:
                    cp_errors.append('Nie podano nowego hasła.')
                elif len(new_password) < 6:
                    cp_errors.append('Za krótkie nowe hasło. Przynajmniej 6 znaków.')
                elif new_password != new_password2:
                    cp_errors.append('Podane hasła nie są identyczne.')
            else:
                cp_errors.append('Podano nieprawidłowe obecne hasło.')
            if len(cp_errors) == 0:
                user.set_password(new_password)
                user.save()
                request.session['cp_success'] = True
                return redirect('account.change_password')
    return render(request, 'account/change_password.html', {
        "cp_errors": cp_errors,
        "cp_success": cp_success
    })
