from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.controllers import ajax
from dashboard.controllers import calendar
from dashboard.controllers import guard
from dashboard.controllers import index
from dashboard.controllers import pendings
from dashboard.controllers import rooms
from dashboard.controllers import users

urlpatterns = [
    url(r'^rooms/add$', rooms.add_edit_cont, name='dashboard.rooms.add'),
    url(r'^rooms/supervisors/(?P<id>[0-9]+)/delete/(?P<uid>[0-9]+)$', rooms.supervisors_delete_cont, name='dashboard.rooms.supervisors.delete'),
    url(r'^rooms/supervisors/(?P<id>[0-9]+)$', rooms.supervisors_cont, name='dashboard.rooms.supervisors'),
    url(r'^rooms/edit/(?P<id>[0-9]+)$', rooms.add_edit_cont, name='dashboard.rooms.edit'),
    url(r'^rooms/delete/(?P<id>[0-9]+)$', rooms.delete_cont, name='dashboard.rooms.delete'),
    url(r'^rooms/page,(?P<page>[0-9]+)$', rooms.index_cont, name='dashboard.rooms.page'),
    url(r'^rooms', rooms.index_cont, name='dashboard.rooms'),

    url(r'^users$', users.index_cont, name='dashboard.users'),
    url(r'^users/page,(?P<page>[0-9]+)$', users.index_cont, name='dashboard.users.page'),

    url(r'^calendar/room/(?P<id>[0-9]+)/date,(?P<month>[0-9]+),(?P<year>[0-9]+)', calendar.room_cont, name='dashboard.calendar.room.date'),
    url(r'^calendar/room/(?P<id>[0-9]+)', calendar.room_cont, name='dashboard.calendar.room'),
    url(r'^calendar', calendar.index_cont, name='dashboard.calendar'),

    url(r'^pendings/reject/(?P<id>[0-9]+)', pendings.reject_cont, name='dashboard.pendings.reject'),
    url(r'^pendings/accept/(?P<id>[0-9]+)', pendings.accept_cont, name='dashboard.pendings.accept'),
    url(r'^pendings', pendings.index_cont, name='dashboard.pendings'),

    url(r'^guard/rooms/page,(?P<page>[0-9]+)$', guard.rooms_cont, name='dashboard.guard.rooms.page'),
    url(r'^guard/rooms$', guard.rooms_cont, name='dashboard.guard.rooms'),
    url(r'^guard$', guard.index_cont, name='dashboard.guard'),

    url(r'^ajax/dashboard_rooms.json', ajax.rooms_search, name='ajax.dashboard.rooms'),
    url(r'^ajax/calendar/day/(?P<day>[0-9]+)-(?P<month>[0-9]+)-(?P<year>[0-9]+)', ajax.calendar_day, name='ajax.calendar.day'),

    url(r'^$', index.index_cont, name='dashboard.index'),
]
