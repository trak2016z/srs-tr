# -*- coding: utf-8 -*-
import os
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.http import Http404
from django.http import HttpResponse
from django.http import request
from django.urls import reverse

from srs.settings import CAPTCHA_LENGTH, BASE_DIR


def show_image(request, name):
    reload = request.GET.get('r', None) if True else False
    if reload:
        captcha = Captcha(request, name)
    hash = request.session.get('captcha_'+name, None)
    if hash is None:
        raise Http404("Captcha does not exist")
    response = HttpResponse(content_type="image/png")
    font_dir = os.path.join(BASE_DIR, "app", "fonts", "Cookie.ttf")
    font = ImageFont.truetype(font_dir, size=22, encoding="unic")
    im = Image.new("RGB", (30+CAPTCHA_LENGTH*25, 40), "#eceeef")
    draw = ImageDraw.Draw(im)
    for iy in range(0, 5):
        y = im.height / 10 + iy * im.height / 5
        draw.line((0, y, im.width, y), fill="#aaaaaa")
    for ix in range(0, 10):
        x = im.width / 20 + ix * im.width / 10
        draw.line((x, 0, x, im.height), fill="#aaaaaa")
    x = 15
    for c in hash:
        rx = random.randint(0, 10)
        ry = random.randint(5, 15)
        draw.text((x+rx, ry), c, font=font, fill="#000000")
        x += 25
    im.save(response, "PNG")
    return response

class Captcha:
    name = 'captcha'
    old_hash = ''
    hash = ''
    url = ''
    def __init__(self, request, name):
        self.name = name
        self.old_hash = request.session.get('captcha_'+self.name, '')
        self.hash = self.random_hash()
        request.session['captcha_'+self.name] = self.hash
        self.url = reverse('captcha', kwargs={'name': self.name})
    def __str__(self):
            return self.name
    def is_valid(self, hash):
        hash = hash.lower()
        return len(self.old_hash) > 0 and self.old_hash == hash
    def random_hash(self):
        rand = ''
        for i in range(1, CAPTCHA_LENGTH+1):
            rand += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
        return rand