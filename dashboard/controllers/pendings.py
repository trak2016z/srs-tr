# _*_ coding:utf-8 _*_
import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from app import consts
from app.models import Reservation, Supervisor_Room
from app.utils.decorator import admin_required, supervisor_required


@supervisor_required
def index_cont(request):
    message = request.session.get('message', '')
    if message:
        del request.session['message']
    if request.user.is_staff:
        lst = Reservation.objects.filter(status=consts.RESERVATION_STATUS_WAITING).order_by('-request_date')
    else:
        rooms_spr = []
        sr_lst = Supervisor_Room.objects.filter(user=request.user)
        for s in sr_lst:
            rooms_spr.append(s.room.id)
        lst = Reservation.objects.filter(room__in=rooms_spr, status=consts.RESERVATION_STATUS_WAITING).order_by('-request_date')
    return render(request, 'dashboard/pendings/index.html', {
        "message": message,
        "lst": lst
    })


@supervisor_required
def accept_cont(request, id):
    res = get_object_or_404(Reservation, pk=id)
    if not request.user.is_staff:
        if not res.room.is_supervisor(request.user):
            return HttpResponseForbidden()
    res.status = consts.RESERVATION_STATUS_ACCEPTED
    res.considered_date = datetime.datetime.now()
    res.considered_user = request.user
    res.save()
    request.session['message'] = 'Rezerwacja została zaakceptowana.'
    return redirect('dashboard.pendings')


@supervisor_required
def reject_cont(request, id):
    res = get_object_or_404(Reservation, pk=id)
    if not request.user.is_staff:
        if not res.room.is_supervisor(request.user):
            return HttpResponseForbidden()
    res.status = consts.RESERVATION_STATUS_REJECTED
    res.considered_date = datetime.datetime.now()
    res.considered_user = request.user
    if request.method == 'POST':
        res.reason = request.POST.get('reason')
    res.save()
    request.session['message'] = 'Rezerwacja została odrzucona.'
    return redirect('dashboard.pendings')