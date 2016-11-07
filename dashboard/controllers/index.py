from django.shortcuts import render

from app.utils.decorator import admin_required

@admin_required
def index_cont(request):
    return render(request, 'dashboard/index.html')
