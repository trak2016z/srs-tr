from django.shortcuts import render

from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
from django.utils import timezone

def index(request):
    '''alg = BCryptSHA256PasswordHasher()
    salt = alg.salt()
    print(salt)
    print(alg.encode('password', salt))'''
    return render(request, 'home.html')
