"""srs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.controllers import index
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
    url(r'^$', index.index_cont, name='dashboard.index'),
]
