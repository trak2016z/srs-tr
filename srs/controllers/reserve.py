# coding=utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from app.consts import RESERVATION_STATUS_ACCEPTED, RESERVATION_STATUS_WAITING
from app.models import Room, Reservation
from app.settings import RES_HOUR_START, RES_HOUR_END
from app.utils.availability import availability_hours_by_date, availability_inrange, availability_inrange2
from app.utils.date import month_name, dayw_name

@login_required
def reserve_post(request, id, day, month, year):
    room = get_object_or_404(Room, pk=id)
    errors = []
    from_hour = request.POST.get('from_hour', '')
    from_minute = request.POST.get('from_minute', '')
    date_from = None
    if len(from_hour) == 0 or len(from_minute) == 0:
        errors.append('Nie podano godziny rozpoczecia.')
    else:
        date_from = timezone.make_aware(datetime.datetime(day=int(day), month=int(month), year=int(year), hour=int(from_hour), minute=int(from_minute)), timezone.get_current_timezone())
    to_hour = request.POST.get('to_hour', '')
    to_minute = request.POST.get('to_minute', '')
    date_to = None
    if len(to_hour) == 0 or len(to_minute) == 0:
        errors.append('Nie podano godziny zakończenia.')
    else:
        date_to = timezone.make_aware(datetime.datetime(day=int(day), month=int(month), year=int(year), hour=int(to_hour), minute=int(to_minute)), timezone.get_current_timezone())
    if date_from is not None and date_to is not None and date_from >= date_to:
        errors.append('Nieprawidłowy zakres godzinowy.')
    if len(errors) == 0:
        tab_hours = availability_hours_by_date(id, int(day), int(month), int(year))
        if not availability_inrange2(tab_hours, date_from.hour, date_from.minute, date_to.hour, date_to.minute):
            errors.append('W tych godzinach sala nie jest dostępna.')
        else:
            dat = date_from
            while dat < date_to:
                how = Reservation.objects.filter(room__id=id, status=RESERVATION_STATUS_ACCEPTED, date_from__lte=dat, date_to__gt=dat).count()
                if how > 0:
                    errors.append('W tych godzinach sala jest już zajęta.')
                    break
                dat += datetime.timedelta(minutes=+15)
    event_name = request.POST.get('event_name', '')
    if len(event_name) == 0:
        errors.append('Nie podano nazwy wydarzenia.')
    elif len(event_name) < 5:
        errors.append('Za krótka nazwa wydarzenia.')
    status = -1
    if len(errors) == 0:
        res = Reservation()
        res.room = room
        res.user = request.user
        res.event_name = event_name
        res.request_date = timezone.now()
        res.date_from = date_from
        res.date_to = date_to
        res.status = RESERVATION_STATUS_ACCEPTED if room.auto_accepted else RESERVATION_STATUS_WAITING
        res.save()
        status = res.status
    return JsonResponse({
        "status": status,
        "errors": errors
    })


def reserve_cont(request, id, day, month, year, hour, minute):
    day = int(day)
    month = int(month)
    year = int(year)
    hour = int(hour)
    minute = int(minute)
    dat = datetime.date(day=day, month=month, year=year)
    w_index = int(dat.strftime("%w"))
    w_index = w_index if w_index > 0 else 7
    room = get_object_or_404(Room, pk=id)
    hour2 = hour+2
    if hour2 > 23:
        hour2 = 23
    hour_range = range(RES_HOUR_START, RES_HOUR_END+1)
    minute_range = range(0, 60, 15)
    return render(request, 'reserve_room.html', {
        "room": room,
        "day": day,
        "month": month,
        "month_name": month_name(month),
        "dow": dayw_name(w_index),
        "year": year,
        "hour_range": hour_range,
        "minute_range": minute_range,
        "hour": hour,
        "hour2": hour2,
        "minute": minute
    })