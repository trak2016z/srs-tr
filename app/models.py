from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.contrib.auth.hashers import BCryptSHA256PasswordHasher

from srs import settings


class User(models.Model):

    REQUIRED_FIELDS = ('password', 'first_name', 'last_name',)
    USERNAME_FIELD = 'email'

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    role = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    is_anonymous = True # TODO
    is_authenticated = False # TODO

    def set_password(self, password):
        alg = BCryptSHA256PasswordHasher()
        self.password = alg.encode(password, alg.salt())

    def is_admin(self):
        return self.role >= 1

    def __str__(self):
        return self.first_name+' '+self.last_name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.TextField(null=True)
    description = models.TextField(null=True)
    seats_number = models.IntegerField(default=0) # liczba miejsc
    auto_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name+' '+self.last_name

class Supervisor_Room(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return 'user='+str(self.user)+', room'+str(self.room)

    class Meta:
        unique_together = ('user', 'room')


class User_ConfirmationHash(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=16)
    hash = models.CharField(max_length=32)

    class Meta:
        unique_together = ('type', 'hash')