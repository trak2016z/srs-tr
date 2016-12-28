# coding=utf-8
import unittest

from django.http import HttpResponseRedirect
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from app.models import User


class SignUpTestCase(TestCase):

    invalid_email_message = 'Format adresu email jest nieprawidłowy.'

    def test_form_invalid_email(self):
        response = self.client.post(reverse('sign_up'), {
            "email": "andrzej",
        })
        self.assertContains(response, self.invalid_email_message)

    def test_form_valid_email(self):
        response = self.client.post(reverse('sign_up'), {
            "email": "andrzej@onet.pl",
        })
        self.assertNotContains(response, self.invalid_email_message)

    def test_save_form(self):
        response = self.client.get(reverse('sign_up'))
        session = self.client.session
        captcha = session['captcha_sign_up']
        email_field = "tragos@onet.eu"
        first_name_field = "Jan"
        last_name_field = "Kowalski"
        password_field = "tragos123"
        response = self.client.post(reverse('sign_up'), {
            "email": email_field,
            "first_name": first_name_field,
            "last_name": last_name_field,
            "password": password_field,
            "password2": password_field,
            "captcha": captcha
        })
        self.assertEqual(User.objects.filter(email=email_field).count(), 1)
        self.assertEqual(User.objects.filter(email=email_field)[0].first_name, first_name_field)
        self.assertEqual(User.objects.filter(email=email_field)[0].last_name, last_name_field)
        self.assertTrue(User.objects.filter(email=email_field)[0].check_password(password_field))
        self.assertFalse(User.objects.filter(email=email_field)[0].check_password(password_field+'x'))


class NotAllowedByGuestTestCase(TestCase):

    redirect_url = reverse('sign_in')

    def test_auth(self):
        self.assertIn(self.redirect_url, self.client.get(reverse('account.change_password'))['Location'])
        self.assertIn(self.redirect_url, self.client.get(reverse('account.change'))['Location'])
        self.assertIn(self.redirect_url, self.client.get(reverse('account.reservations'))['Location'])
        self.assertIn(self.redirect_url, self.client.get(reverse('dashboard.index'))['Location'])


def make_account(email, password, first_name, last_name):
    User.objects.filter(email=email).delete()
    u = User()
    u.email = email
    u.set_password(password)
    u.first_name = first_name
    u.last_name = last_name
    u.active = True
    return u.save()


class NotAllowedByNoAdminTestCase(TestCase):

    email_field = "tragos@onet.eu"
    password_field = "tragos123"
    sign_in_url = reverse("sign_in")

    def prepare(self):
        make_account(self.email_field, self.password_field, "Jan", "Kowalski")
        response = self.client.post(self.sign_in_url, {
            "email": self.email_field, "password": self.password_field
        })
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_auth(self):
        self.prepare()
        response = self.client.get(reverse('account.change'))
        self.assertNotIsInstance(response, HttpResponseRedirect) # user has access to change data
        response = self.client.get(reverse('dashboard.index'))
        self.assertEqual(response.status_code, 403)

