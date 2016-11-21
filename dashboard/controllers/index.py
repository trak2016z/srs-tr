from django.shortcuts import render

from app.models import User, Room
from app.utils.decorator import admin_required

@admin_required
def index_cont(request):
    return render(request, 'dashboard/index.html', {
        "rooms_count": Room.objects.count(),
        "users_count": User.objects.count()
    })
