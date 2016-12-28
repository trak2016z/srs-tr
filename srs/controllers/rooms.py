# -*- coding: utf-8 -*-
import re

import math
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from app import consts
from app.models import Room, Reservation, Availability_Room
from app.settings import RES_HOUR_START, RES_HOUR_END
from app.utils.availability import availability_by_date, availability_hours_by_date, availability_inrange
from app.utils.date import month_days, w_first_day, month_name, dayw_name, dayw_name_date
from app.utils.pagination import Pagination


def search(request, page=1):
    if request.method == 'POST':
        url_lst = []
        if request.POST.get('name', None):
            url_lst.append('name='+request.POST.get('name'))
        if request.POST.get('city', None):
            url_lst.append('city=' + request.POST.get('city'))
        mseats = request.POST.get('mseats', "0")
        if mseats and mseats != "0":
            url_lst.append('mseats=' + mseats)
        if request.POST.get('seats', None):
            url_lst.append('seats=' + request.POST.get('seats'))
        url_str = ""
        if len(url_lst) > 0:
            for u in url_lst:
                url_str = url_str + ("?" if len(url_str) == 0 else "&")
                url_str = url_str + u
        return HttpResponseRedirect(reverse('rooms.search')+url_str)
    rooms = Room.objects.all()
    name = request.GET.get('name', '')
    if len(name) > 0:
        rooms = rooms.filter(name__icontains=name)
    city = request.GET.get('city', '')
    if len(city) > 0:
        rooms = rooms.filter(city__icontains=city)
    seats = request.GET.get('seats', '')
    mseats = request.GET.get('mseats', '0')
    if len(seats) > 0 and re.match(r"(^[0-9]+$)", seats):
        if mseats == "1":
            rooms = rooms.filter(seats_number__lte=int(seats))
        else:
            rooms = rooms.filter(seats_number__gte=int(seats))
    pagination = Pagination()
    pagination.url = "rooms.search.page"
    tab = request.get_full_path().split("?")
    if len(tab) > 1:
        pagination.url_add = "?"+tab[1]
    pagination.page = int(page)
    pagination.perPage = 16
    pagination.count = rooms.count()
    rooms = rooms.order_by('name', 'city')[pagination.ifrom:pagination.ito]
    return render(request, 'rooms.html', {
        "rooms": rooms,
        "name": name,
        "city": city,
        "seats": seats,
        "mseats": mseats,
        "pagination": pagination
    })


def one(request, id, month=None, year=None):
    room = get_object_or_404(Room, pk=id)
    today = datetime.date.today()
    month = today.month if month is None else int(month)
    year = today.year if year is None else int(year)
    prev_year = year - 1 if month <= 1 else year
    prev_month = month - 1 if month > 1 else 12
    next_year = year + 1 if month >= 12 else year
    next_month = month + 1 if month < 12 else 1
    current_first_day_range = range(1, w_first_day(month, year))
    days = []
    md = month_days(month, year)
    for i in range(1, md + 1):
        must_break = (len(current_first_day_range) + i) % 7 == 1
        dow = (w_first_day(month, year) + i) % 7 - 1
        ava = None
        past = today > datetime.date(day=i, month=month, year=year)
        if not past:
            ava = availability_by_date(room.id, i, month, year)
        events = Reservation.objects.filter(room__id=id).order_by('date_from')
        days.append({"nr": i, "must_break": must_break, "past": past, "ava": ava, "dow":dayw_name(dow), "events":events})
    how_end = int(math.ceil((len(current_first_day_range) + md) / 7.)) * 7 - md - len(current_first_day_range)
    can_day_current = today.day if year == today.year and month == today.month else None
    return render(request, 'room_one.html', {
        "room": room,
        "month": month,
        "year": year,
        "month_str": month_name(month),
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "current_first_day_range": current_first_day_range,
        "days": days,
        "how_end_range": range(0, how_end),
        "can_day_current": can_day_current,
    })


def one_day(request, id, day, month, year):
    room = get_object_or_404(Room, pk=id)
    today = datetime.date.today()
    day = int(day)
    month = int(month)
    year = int(year)
    hours = []
    one_height = 30.0
    dat = datetime.date(year=year, month=month, day=day)
    next_dat = dat + datetime.timedelta(days=+1)
    prev_dat = dat + datetime.timedelta(days=-1)
    past_day = today > datetime.date(day=day, month=month, year=year)
    ava_tab = None
    if not past_day:
        ava_tab = availability_hours_by_date(id, day, month, year)
    for h in range(RES_HOUR_START, RES_HOUR_END+1):
        for m in range(0, 60, 30):
            ihour = "0"+str(h) if h < 10 else str(h)
            iminute = "0"+str(m) if m < 10 else str(m)
            sdat = timezone.make_aware(datetime.datetime(year=year, month=month, day=day, hour=h, minute=m), timezone.get_current_timezone())
            dw = int(sdat.strftime("%w"))
            dw = dw if dw > 0 else 7

            h_next = h if m < 30 else h+1
            m_next = m+30 if m < 30 else 0
            if h_next == 24:
                h_next = 23
                m_next = 59
            ihour_next = "0" + str(h_next) if h_next < 10 else str(h_next)
            iminute_next = "0" + str(m_next) if m_next < 10 else str(m_next)
            sdat_next = timezone.make_aware(datetime.datetime(year=year, month=month, day=day, hour=h_next, minute=m_next), timezone.get_current_timezone())
            reserv = Reservation.objects.filter(room__id=id, status=consts.RESERVATION_STATUS_ACCEPTED, date_from__gte=sdat, date_from__lt=sdat_next).order_by('-request_date')
            for r in reserv:
                hf = r.hour_from_format.split(":")
                hf_minute = int(hf[1]) - m
                r.hour_diff_top = int(hf_minute)
                r.hour_diff_height = int(r.seconds_diff / 60.0 / 30.0 * one_height)

            ava = availability_inrange(ava_tab, h, m)

            hours.append({"hour": h, "ihour": ihour, "minute": m, "iminute": iminute, "reserv": reserv, "ava": ava})
    return render(request, 'room_one_day.html', {
        "room": room,
        "day": day,
        "month": month,
        "month_str": month_name(month),
        "year": year,
        "hours": hours,
        "day_w": dayw_name_date(day, month, year),
        "next_dat": next_dat,
        "prev_dat": prev_dat,
        "past_day": past_day
    })
