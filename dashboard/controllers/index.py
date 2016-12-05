from django.shortcuts import render

from app.models import User, Room, Reservation
from app.utils.decorator import admin_required
import app.consts


@admin_required
def index_cont(request):
    return render(request, 'dashboard/index.html', {
        "reservations_waiting_count": Reservation.objects.filter(status=app.consts.RESERVATION_STATUS_WAITING).count(),
        "rooms_count": Room.objects.count(),
        "users_count": User.objects.count()
    })
