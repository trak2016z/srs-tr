import re
from datashape import json
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from app import consts
from app.models import Room, User, Reservation
from app.utils.decorator import admin_required


@admin_required
def rooms_search(request):
    phrase = request.GET.get('phrase', '')
    r_list = []
    for room in Room.objects.order_by('name'):
        if len(phrase) == 0 or re.match(r'(.*)'+phrase+'(.*)', room.name) or re.match(r'(.*)'+phrase+'(.*)', room.city):
            link = reverse('dashboard.calendar.room', kwargs={'id': room.id})
            r = {'id': room.id, 'name': room.name, 'city': room.city, 'seats': room.seats_number, 'link': link}
            r_list.append(r)
    return JsonResponse({
        'rooms': r_list,
        'phrase': phrase
    })


@admin_required
def calendar_day(request, day, month, year):
    # TODO
    return render(request, 'dashboard/calendar/day.html', {
        "day": day,
        "month": month,
        "year": year
    })