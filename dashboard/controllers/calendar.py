# coding=utf-8
import datetime

import math

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from app import consts
from app.models import Room, Reservation, Supervisor_Room
from app.utils.availability import availability_by_date
from app.utils.date import month_name, w_first_day, month_days
from app.utils.decorator import admin_required, supervisor_required, supervisor_room_required


@supervisor_required
def index_cont(request):
    return render(request, 'dashboard/calendar/index.html')


@supervisor_room_required
def room_cont(request, id, month=None, year=None):
    room = get_object_or_404(Room, pk=id)
    today = datetime.datetime.today()
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    month = today.month if month is None else int(month)
    year = today.year if year is None else int(year)
    prev_year = year-1 if month <= 1 else year
    prev_month = month-1 if month > 1 else 12
    next_year = year+1 if month >= 12 else year
    next_month = month+1 if month < 12 else 1
    current_first_day_range = range(1, w_first_day(month, year))
    days = []
    md = month_days(month, year)
    for i in range(1, md+1):
        must_break = (len(current_first_day_range) + i) % 7 == 1
        count_waiting = Reservation.objects.filter(room=room, status=consts.RESERVATION_STATUS_WAITING, date_from__day=i, date_from__month=month, date_from__year=year).count()
        count_accepted = Reservation.objects.filter(room=room, status=consts.RESERVATION_STATUS_ACCEPTED, date_from__day=i, date_from__month=month, date_from__year=year).count()
        ava = availability_by_date(room.id, i, month, year)
        days.append({"nr": i, "must_break": must_break, "count_waiting": count_waiting, "count_accepted" : count_accepted, "availability": ava})
    how_end = int(math.ceil((len(current_first_day_range) + md) / 7.)) * 7 - md - len(current_first_day_range)
    can_day_current = today.day if year == today.year and month == today.month else None
    return render(request, 'dashboard/calendar/room.html', {
        "room": room,
        "year": year,
        "month": month,
        "month_str": month_name(month),
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "current_first_day_range": current_first_day_range,
        "days": days,
        "how_end_range": range(0, how_end),
        "can_day_current": can_day_current,
        "message": message
    })


@supervisor_room_required
def room_reject_cont(request, id, rid):
    room = get_object_or_404(Room, pk=id)
    res = get_object_or_404(Reservation, pk=rid)
    res.status = consts.RESERVATION_STATUS_REJECTED
    res.considered_date = datetime.datetime.now()
    res.considered_user = request.user
    if request.method == 'POST':
        res.reason = request.POST.get('reason', '')
    res.save()
    request.session['message'] = 'Rezerwacja została odrzucona.'
    return JsonResponse({
        "executed": True
    })


@supervisor_room_required
def room_accept_cont(request, id, rid):
    room = get_object_or_404(Room, pk=id)
    res = get_object_or_404(Reservation, pk=rid)
    res.status = consts.RESERVATION_STATUS_ACCEPTED
    res.considered_date = datetime.datetime.now()
    res.considered_user = request.user
    res.save()
    request.session['message'] = 'Rezerwacja została zaakceptowana.'
    return JsonResponse({
        "executed": True
    })