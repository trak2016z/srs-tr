from __future__ import unicode_literals

from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone

import app.consts
from app.utils.date import date_format_short


class User(models.Model):

    REQUIRED_FIELDS = ('password', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    role = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    objects = UserManager()

    def set_password(self, password):
        alg = BCryptSHA256PasswordHasher()
        self.password = alg.encode(password, alg.salt())

    def check_password(self, password):
        alg = BCryptSHA256PasswordHasher()
        return alg.verify(password, self.password)

    @property
    def is_anonymous(self):
        return self.id is None

    @property
    def is_authenticated(self):
        return self.id is not None

    @property
    def is_staff(self):
        return self.is_authenticated and self.role >= 1

    def full_name(self):
        return self.first_name + ' ' + self.last_name if self.is_authenticated else None

    def __str__(self):
        return self.full_name()

    @property
    def is_any_supervisor(self):
        return Supervisor_Room.objects.filter(user=self).count() > 0


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.TextField(null=True)
    description = models.TextField(null=True)
    seats_number = models.IntegerField(default=0) # liczba miejsc
    auto_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def place(self):
        return self.city + (', '+self.address if self.address else '')

    def supervisiors(self):
        return Supervisor_Room.objects.filter(room=self)

    def supervisiors_count(self):
        return Supervisor_Room.objects.filter(room=self).count()

    def is_supervisor(self, user):
        return Supervisor_Room.objects.filter(room=self, user=user).count() > 0


class Supervisor_Room(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return 'user='+str(self.user)+', room='+str(self.room)

    class Meta:
        unique_together = ('user', 'room')


class User_ConfirmationHash(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=16)
    hash = models.CharField(max_length=32)

    class Meta:
        unique_together = ('type', 'hash')


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    request_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(default='0', max_length=1)
    considered_date = models.DateTimeField(null=True)
    considered_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='considered')

    @property
    def is_accepted(self):
        return self.status == app.consts.RESERVATION_STATUS_ACCEPTED

    @property
    def is_rejected(self):
        return self.status == app.consts.RESERVATION_STATUS_REJECTED

    @property
    def is_waiting(self):
        return self.status == app.consts.RESERVATION_STATUS_WAITING

    @property
    def is_cancelled(self):
        return self.status == app.consts.RESERVATION_STATUS_CANCELLED

    @property
    def date_from_format(self):
        return date_format_short(self.date_from)

    @property
    def date_to_format(self):
        return date_format_short(self.date_to)

