from django.shortcuts import render

from app import consts
from app.models import Room, Supervisor_Room, Reservation
from app.utils.decorator import supervisor_required
from app.utils.pagination import Pagination


@supervisor_required
def index_cont(request):
    sr = Supervisor_Room.objects.filter(user=request.user)
    lst = []
    for s in sr:
        lst.append(s.room.id)
    return render(request, 'dashboard/guard/index.html', {
        "rooms_count": sr.count(),
        "reservations_waiting_count": Reservation.objects.filter(room__in=lst, status=consts.RESERVATION_STATUS_WAITING).count()
    })


@supervisor_required
def rooms_cont(request, page=1):
    pagination = Pagination()
    pagination.url = "dashboard.guard.rooms.page"
    pagination.page = int(page)
    pagination.perPage = 20
    pagination.count = Supervisor_Room.objects.filter(user=request.user).count()
    sr_list_id = []
    for sr in Supervisor_Room.objects.filter(user=request.user):
        sr_list_id.append(sr.room.id)
    rooms = Room.objects.filter(id__in=sr_list_id).order_by('name')[pagination.ifrom:pagination.ito] # change
    return render(request, 'dashboard/guard/rooms.html', {
        "rooms": rooms,
        "pagination": pagination
    })
