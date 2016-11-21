# _*_ coding:utf-8 _*_
import re
from django.shortcuts import render, redirect, get_object_or_404

from app.models import User, Room, Supervisor_Room
from app.utils.decorator import admin_required
from app.utils.pagination import Pagination


@admin_required
def index_cont(request, page=1):
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    pagination = Pagination()
    pagination.url = "dashboard.rooms.page"
    pagination.page = int(page)
    pagination.perPage = 20
    pagination.count = Room.objects.count()
    rooms = Room.objects.order_by('name')[pagination.ifrom:pagination.ito]
    return render(request, 'dashboard/rooms/index.html', {
        "rooms": rooms,
        "pagination": pagination,
        "message": message
    })


@admin_required
def add_edit_cont(request, id=None):
    room = Room()
    if id is not None:
        room = get_object_or_404(Room, pk=id)
    mode = "edytuj" if id is not None else "dodaj"
    mode2 = "zapisz zmiany" if id is not None else "dodaj"
    errors = []
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    if request.method == 'POST':
        room.name = request.POST.get('name')
        if len(room.name) == 0:
            errors.append('Nie podano nazwy.')
        room.city = request.POST.get('city')
        if len(room.city) == 0:
            errors.append('Nie podano miasta.')
        room.address = request.POST.get('address')
        room.description = request.POST.get('description')
        room.seats_number = request.POST.get('seats_number')
        if len(room.seats_number) > 0:
            if not re.match(r"(^[0-9]+$)", room.seats_number):
                errors.append('Nieprawidłowy format liczby miejsc.')
        room.auto_accepted = True if request.POST.get('auto_accepted') else False
        if len(errors) == 0:
            room.save()
            if id is not None:
                request.session['message'] = 'Zapisano zmiany.'
                return redirect('dashboard.rooms.edit', id=id)
            else:
                request.session['message'] = 'Sala została dodana'
                return redirect('dashboard.rooms')
    return render(request, 'dashboard/rooms/add_edit.html', {
        "room": room,
        "mode": mode,
        "mode2": mode2,
        "url": request.build_absolute_uri(),
        "message": message,
        "errors": errors
    })


@admin_required
def delete_cont(request, id):
    try:
        room = Room.objects.get(id=id)
        room.delete()
        request.session['message'] = 'Sala została usunięta.'
    except Room.DoesNotExist:
        pass
    return redirect('dashboard.rooms')


@admin_required
def supervisors_cont(request, id):
    room = get_object_or_404(Room, pk=id)
    supervisors = Supervisor_Room.objects.filter(room=room).order_by('user__last_name').order_by('user__first_name')
    users_canAdd = []
    users_v = User.objects.filter(role=0).order_by('last_name').order_by('first_name')
    for u in users_v:
        if Supervisor_Room.objects.filter(room=room, user=u).count() == 0:
            users_canAdd.append(u)
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            uid_obj = User.objects.get(pk=uid)
            if uid_obj in users_canAdd:
                svr = Supervisor_Room()
                svr.user = uid_obj
                svr.room = room
                svr.save()
                request.session['message'] = 'Dodano opiekuna dla tej sali.'
                return redirect('dashboard.rooms.supervisors', id=room.id)
        except User.DoesNotExist:
            pass
    return render(request, 'dashboard/rooms/supervisors.html', {
        "room": room,
        "supervisors": supervisors,
        "users_canAdd": users_canAdd,
        "message": message
    })


@admin_required
def supervisors_delete_cont(request, id, uid):
    try:
        room = Room.objects.get(id=id)
        try:
            user = User.objects.get(id=uid)
            svr = Supervisor_Room.objects.filter(room=room, user=user)
            if len(svr) > 0:
                svr[0].delete()
                request.session['message'] = 'Odebrano prawa opiekuna dla tej sali.'
        except User.DoesNotExist:
            pass
    except Room.DoesNotExist:
        pass
    return redirect('dashboard.rooms.supervisors', id=id)