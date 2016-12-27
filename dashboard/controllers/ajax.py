import re
from datashape import json
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from app import consts
from app.models import Room, User, Reservation, Supervisor_Room
from app.utils.availability import availability_hours_by_date
from app.utils.decorator import admin_required, supervisor_required, supervisor_room_required


@supervisor_required
def rooms_search(request):
    rooms_list = []
    if request.user.is_staff:
        rooms_list = Room.objects.order_by('name')
    else:
        for sr in Supervisor_Room.objects.filter(user=request.user):
            rooms_list.append(sr.room)
    phrase = request.GET.get('phrase', '')
    r_list = []
    for room in rooms_list:
        if len(phrase) == 0 or re.match(r'(.*)'+phrase+'(.*)', room.name, flags=re.IGNORECASE) or re.match(r'(.*)'+phrase+'(.*)', room.city, flags=re.IGNORECASE):
            link = reverse('dashboard.calendar.room', kwargs={'id': room.id})
            r = {'id': room.id, 'name': room.name, 'city': room.city, 'seats': room.seats_number, 'link': link}
            r_list.append(r)
    return JsonResponse({
        'rooms': r_list,
        'phrase': phrase
    })


@supervisor_room_required
def calendar_day(request, id, day, month, year):
    room = get_object_or_404(Room, pk=id)
    day = int(day)
    month = int(month)
    year = int(year)
    reservations = Reservation.objects.filter(room=room, date_from__day=day, date_from__month=month, date_from__year=year)
    hours_str = []
    for h in availability_hours_by_date(id, day, month, year):
        (hfrom, hto) = h
        (bminute, bsecond) = hfrom
        bminute_str = str(bminute) if bminute > 9 else "0"+str(bminute)
        bsecond_str = str(bsecond) if bsecond > 9 else "0"+str(bsecond)
        (eminute, esecond) = hto
        eminute_str = str(eminute) if eminute > 9 else "0" + str(eminute)
        esecond_str = str(esecond) if esecond > 9 else "0" + str(esecond)
        hours_str.append({"hfrom": bminute_str+":"+bsecond_str, "hto": eminute_str+":"+esecond_str})
    return render(request, 'dashboard/calendar/day.html', {
        "room": room,
        "day": day,
        "month": month,
        "year": year,
        "reservations": reservations,
        "hours_str": hours_str,
    })