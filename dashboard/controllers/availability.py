# coding=utf-8
import datetime

import re
from dateutil.parser import parse
from django.shortcuts import render, get_object_or_404, redirect

from app.models import Room, Availability_Room
from app.utils.date import dayw_name
from app.utils.decorator import supervisor_required, supervisor_room_required


@supervisor_room_required
def room_cont(request, id, month, year):
    room = get_object_or_404(Room, pk=id)
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    av_list = Availability_Room.objects.filter(room__id=room.id).order_by('day_of_week', 'since', '-until', 'hour_from', '-hour_to')
    for a in av_list:
        a.dow = dayw_name(a.day_of_week)
    return render(request, 'dashboard/availability/room.html', {
        "room": room,
        "month": month,
        "year": year,
        "av_list": av_list,
        "message": message
    })


@supervisor_required
def room_delete_cont(request, id, month, year, aid):
    room = get_object_or_404(Room, pk=id)
    av = get_object_or_404(Availability_Room, pk=aid)
    av.delete()
    request.session['message'] = 'Wpis został usunięty.'
    return redirect('dashboard.availability.room', id=id, month=month, year=year)


@supervisor_room_required
def room_add_cont(request, id, month, year):
    room = get_object_or_404(Room, pk=id)
    dow_list = []
    for i in range(1, 8):
        dow_list.append({ "key": i, "value": dayw_name(i) })
    dow = []
    today = datetime.date.today()
    since = today.isoformat()
    until = ""
    hour_from = "00:00"
    hour_to = "23:59"
    errors = []
    if request.method == 'POST':
        errors = []
        dowX = request.POST.getlist('day_of_week[]')
        dow = []
        for i in dowX:
            dow.append(int(i))
        if len(dow) == 0:
            errors.append('Nie wybrano przynajmniej jednego dnia tygodnia.')
        since = request.POST.get('since', '')
        since_day = None
        if len(since) == 0:
            errors.append('Nie podano daty rozpoczęcia.')
        else:
            since_day = parse(since)
        until = request.POST.get('until', '')
        until_day = None
        if len(until) == 0:
            errors.append('Nie podano daty zakończenia.')
        else:
            until_day = parse(until)
        if since_day is not None and until_day is not None and since_day > until_day:
            errors.append('Zły zakres daty obowiązywania.')
        hour_from = request.POST.get('hour_from', '')
        if len(hour_from) == 0:
            errors.append('Nie podano godziny rozpoczęcia.')
        elif not re.match(r"(^[0-9]{2}:[0-9]{2}$)", hour_from):
            errors.append('Nieprawidłowy format godziny rozpoczęcia.')
        hour_to = request.POST.get('hour_to', '')
        if len(hour_to) == 0:
            errors.append('Nie podano godziny zakończenia.')
        elif not re.match(r"(^[0-9]{2}:[0-9]{2}$)", hour_to):
            errors.append('Nieprawidłowy format godziny rozpoczęcia.')
        if len(errors) == 0 and hour_from > hour_to:
            errors.append('Zły zakres godzinowy.')
        if len(errors) == 0:
            for day_of_week in dow:
                ar = Availability_Room()
                ar.room = room
                ar.day_of_week = day_of_week
                ar.since = since_day
                ar.until = until_day
                ar.hour_from = hour_from
                ar.hour_to = hour_to
                ar.save()
            request.session['message'] = 'Utworzono wpis o dostępności sali.'
            return redirect('dashboard.availability.room', id=room.id, month=month, year=year)
    return render(request, 'dashboard/availability/room_add.html', {
        "room": room,
        "month": month,
        "year": year,
        "dow": dow,
        "dow_list": dow_list,
        "since": since,
        "until": until,
        "hour_from": hour_from,
        "hour_to": hour_to,
        "errors": errors
    })