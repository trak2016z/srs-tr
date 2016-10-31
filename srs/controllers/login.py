# -*- coding: utf-8 -*-
from django.shortcuts import render


def sign_in_cont(request):
    invalid = False
    not_active = False
    activated = request.session.get('activated-account', False)
    if activated:
        del request.session['activated-account']
    changed_password = request.session.get('changed_password', False)
    if changed_password:
        del request.session['changed_password']
    return render(request, 'sign_in.html', {
        "invalid": invalid,
        "not_active": not_active,
        "activated": activated,
        "changed_password": changed_password
    })

