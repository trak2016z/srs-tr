# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from app.models import User


def sign_in_cont(request):
    invalid = False
    not_active = False
    activated = request.session.get('activated-account', False)
    if activated:
        del request.session['activated-account']
    changed_password = request.session.get('changed_password', False)
    if changed_password:
        del request.session['changed_password']
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        invalid = True
        user = User.objects.filter(email=email).get()
        if user is not None:
            if user.check_password(password):
                invalid = False
                not_active = True
                if user.active:
                    user_auth = authenticate(username=email, password=password)
                    if user_auth is not None:
                        login(request, user_auth)
                        return redirect('home')
    return render(request, 'sign_in.html', {
        "invalid": invalid,
        "not_active": not_active,
        "activated": activated,
        "changed_password": changed_password
    })


def sign_out_cont(request):
    logout(request)
    return redirect('home')