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
import sys
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils import timezone

from app import settings
from app.settings import BASE_DIR
from app.utils import captcha
from dashboard.controllers import ajax
from srs.controllers import account
from srs.controllers import home
from srs.controllers import reserve
from srs.controllers import rooms
from srs.controllers.forgotten_password import forgotten_password_cont, reset_password_cont
from srs.controllers.sign_in import sign_in_cont, sign_out_cont
from srs.controllers.sign_up import sign_up_cont, activate_account_cont

urlpatterns = [
    url(r'^$', home.index, name='home'),

    url(r'^captcha/(?P<name>[a-zA-Z0-9_-]+)$', captcha.show_image, name='captcha'),
    url(r'^sign_up', sign_up_cont, name='sign_up'),
    url(r'^activate_account/(?P<hash>[a-zA-Z0-9]+)$', activate_account_cont, name='activate_account'),
    url(r'^forgotten_password', forgotten_password_cont, name='forgotten_password'),
    url(r'^reset_password/(?P<hash>[a-zA-Z0-9]+)$', reset_password_cont, name='reset_password'),
    url(r'^sign_in', sign_in_cont, name='sign_in'),
    url(r'^sign_out', sign_out_cont, name='sign_out'),

    url(r'^account/change_password', account.change_password, name='account.change_password'),
    url(r'^account/change', account.change, name='account.change'),

    url(r'^account/reservations/delete/room,(?P<room_id>[0-9]+)/id,(?P<id>[0-9]+)', account.reservations_room_delete, name='account.reservations.room.delete'),
    url(r'^account/reservations/room,(?P<room_id>[0-9]+)/page,(?P<page>[0-9]+)', account.reservations_room, name='account.reservations.room.page'),
    url(r'^account/reservations/room,(?P<room_id>[0-9]+)', account.reservations_room, name='account.reservations.room'),
    url(r'^account/reservations', account.reservations, name='account.reservations'),

    url(r'^reserve-room/(?P<id>[0-9]+)/(?P<day>[0-9]+)-(?P<month>[0-9]+)-(?P<year>[0-9]+).json', reserve.reserve_post, name='reserve.room.post'),
    url(r'^reserve-room/(?P<id>[0-9]+)/(?P<day>[0-9]+)-(?P<month>[0-9]+)-(?P<year>[0-9]+)/(?P<hour>[0-9]+):(?P<minute>[0-9]+)', reserve.reserve_cont, name='reserve.room'),

    url(r'^rooms/(?P<id>[0-9]+)/day/(?P<day>[0-9]+)-(?P<month>[0-9]+)-(?P<year>[0-9]+)', rooms.one_day, name='rooms.one.day'),

    url(r'^rooms/(?P<id>[0-9]+)/day/(?P<day>[0-9]+)-(?P<month>[0-9]+)-(?P<year>[0-9]+)', rooms.one_day, name='rooms.one.day'),

    url(r'^rooms/(?P<id>[0-9]+)/m,(?P<month>[0-9]+)/y,(?P<year>[0-9]+)', rooms.one, name='rooms.one'),
    url(r'^rooms/(?P<id>[0-9]+)', rooms.one, name='rooms.one'),

    url(r'^rooms/p,(?P<page>[0-9]+)', rooms.search, name='rooms.search.page'),
    url(r'^rooms', rooms.search, name='rooms.search'),

    url(r'^dashboard/', include('dashboard.urls')),
    # url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


def handler403(request):
    response = render_to_response('errors/403.html')
    response.status_code = 403
    return response


def handler404(request):
    response = render_to_response('errors/404.html')
    response.status_code = 404
    return response


def handler500(request):
    typ, value, traceback = sys.exc_info()
    now = timezone.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H_%M_%S')
    f = open(BASE_DIR+'/app/logs/'+now_str+'.txt', 'w+')
    f.write('500 | Internal Server Error\n')
    f.write('Request: '+request.path+' ['+request.method+']\n')
    f.write('Date: '+now_str+'\n')
    f.write(str(typ)+'\n')
    f.write(str(value))
    response = render_to_response('errors/500.html')
    response.status_code = 500
    return response

