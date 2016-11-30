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
    redirect_p = ''
    next = request.GET.get('next', '')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_p = request.POST.get('redirect')
        invalid = True
        try:
            user = User.objects.filter(email=email).get()
            if user.check_password(password):
                invalid = False
                not_active = True
                if user.active:
                    user_auth = authenticate(username=email, password=password)
                    if user_auth is not None:
                        login(request, user_auth)
                        redirect_to = redirect_p if redirect_p else 'home'
                        return redirect(redirect_to)
        except User.DoesNotExist:
            pass
    return render(request, 'sign_in.html', {
        "invalid": invalid,
        "not_active": not_active,
        "activated": activated,
        "changed_password": changed_password,
        "next": next,
        "redirect": redirect_p or next
    })


def sign_out_cont(request):
    logout(request)
    return redirect('home')