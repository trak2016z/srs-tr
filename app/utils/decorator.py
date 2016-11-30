from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, resolve_url

from app import settings
from app.models import Room


def admin_required(function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def _wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            path = request.get_full_path()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
        elif request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrap


def supervisor_required(function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def _wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            path = request.get_full_path()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
        elif request.user.is_staff or request.user.is_any_supervisor:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrap


def supervisor_room_required(function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def _wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            path = request.get_full_path()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
        elif request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            id = kwargs.get('id', None)
            room = get_object_or_404(Room, pk=id)
            if room.is_supervisor(request.user):
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
    return _wrap
