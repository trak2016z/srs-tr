from django.shortcuts import render

def index_cont(request):
    return render(request, 'dashboard/index.html')
