# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from app.models import User, Reservation, Room
import app.consts
from app.utils.pagination import Pagination


@login_required
def change(request):
    update_errors = []
    update_success = request.session.get('update_success', False)
    if update_success:
        del request.session['update_success']
    user = User.objects.filter(id=request.user.id).get()
    first_name = user.first_name
    last_name = user.last_name
    if request.method == 'POST' and request.POST.get('update'):
        first_name = request.POST.get('first_name', '')
        if len(first_name) == 0:
            update_errors.append('Nie podano imienia.')
        elif len(first_name) < 3:
            update_errors.append('Za krótkie imie.')
        last_name = request.POST.get('last_name', '')
        if len(last_name) == 0:
            update_errors.append('Nie podano nazwiska.')
        elif len(last_name) < 3:
            update_errors.append('Za krótkie nazwisko.')
        if len(update_errors) == 0:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            request.session['update_success'] = True
            return redirect('account.change')
    return render(request, 'account/change.html', {
        "first_name": first_name,
        "last_name": last_name,
        "update_errors": update_errors,
        "update_success": update_success,
    })


@login_required
def change_password(request):
    cp_errors = []
    cp_success = request.session.get('cp_success', False)
    if cp_success:
        del request.session['cp_success']
    if request.method == 'POST' and request.POST.get('change-password'):
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')
            user = User.objects.filter(id=request.user.id).get()
            if user.check_password(password):
                if len(new_password) == 0:
                    cp_errors.append('Nie podano nowego hasła.')
                elif len(new_password) < 6:
                    cp_errors.append('Za krótkie nowe hasło. Przynajmniej 6 znaków.')
                elif new_password != new_password2:
                    cp_errors.append('Podane hasła nie są identyczne.')
            else:
                cp_errors.append('Podano nieprawidłowe obecne hasło.')
            if len(cp_errors) == 0:
                user.set_password(new_password)
                user.save()
                request.session['cp_success'] = True
                return redirect('account.change_password')
    return render(request, 'account/change_password.html', {
        "cp_errors": cp_errors,
        "cp_success": cp_success
    })


@login_required
def reservations(request):
    res = Reservation.objects.filter(user=request.user).exclude(status=app.consts.RESERVATION_STATUS_CANCELLED).order_by('date_from')
    rooms = []
    if len(res) > 0:
        for r in res:
            if r.room not in rooms:
                rooms.append(r.room)
    for r in rooms:
        r.accepted = Reservation.objects.filter(room=r, user=request.user, status=app.consts.RESERVATION_STATUS_ACCEPTED, date_to__gt=timezone.now()).order_by('date_from')[:3]
        r.waiting = Reservation.objects.filter(room=r, user=request.user, status=app.consts.RESERVATION_STATUS_WAITING).order_by('date_from')[:3]
    return render(request, 'account/reservations.html', {
        'rooms': rooms
    })


@login_required
def reservations_room(request, room_id, page=1):
    room = get_object_or_404(Room, pk=room_id)
    message = request.session.get('message', False)
    if message:
        del request.session['message']
    pagination = Pagination()
    pagination.url = "account.reservations.room.page"
    pagination.args = {'room_id': room_id}
    pagination.page = int(page)
    pagination.perPage = 20
    pagination.count = Reservation.objects.filter(room__id=room_id, user=request.user).count()
    history = Reservation.objects.filter(room__id=room_id, user=request.user).order_by('-request_date')[pagination.ifrom:pagination.ito]
    for h in history:
        h.can_reject = h.date_from > timezone.now() and (h.is_accepted or h.is_waiting)
    return render(request, 'account/reservations_room.html', {
        'room': room,
        'history': history,
        'pagination': pagination,
        'message': message
    })


@login_required
def reservations_room_delete(request, room_id, id):
    room = get_object_or_404(Room, pk=room_id)
    reservation = get_object_or_404(Reservation, pk=id)
    if reservation.user != request.user or reservation.is_cancelled or reservation.is_rejected:
        raise Http404
    reservation.status = app.consts.RESERVATION_STATUS_CANCELLED
    reservation.save()
    request.session['message'] = 'Wybrana rezerwacja została wycofana.'
    return redirect('account.reservations.room', room_id=room_id)
