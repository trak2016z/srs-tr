from django.shortcuts import render

from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
from django.utils import timezone

def index(request):
    return render(request, 'home.html')
