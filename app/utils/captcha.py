# -*- coding: utf-8 -*-
import os
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.http import Http404
from django.http import HttpResponse
from django.urls import reverse

from app.settings import CAPTCHA_LENGTH, BASE_DIR


def show_image(request, name):
    reload = request.GET.get('r', None) if True else False
    if reload:
        captcha = Captcha(request, name)
    hash = request.session.get('captcha_'+name, None)
    if hash is None:
        raise Http404("Captcha does not exist.")
    response = HttpResponse(content_type="image/png")
    font_dir = os.path.join(BASE_DIR, "app", "fonts", "Dink.ttf")
    font = ImageFont.truetype(font_dir, size=28, encoding="unic")
    im = Image.new("RGB", (30+CAPTCHA_LENGTH*25, 40), "#eceeef")
    width = im.size[0]
    height = im.size[1]
    draw = ImageDraw.Draw(im)
    for iy in range(0, 5):
        y = height / 10 + iy * height / 5
        draw.line((0, y, width, y), fill="#aaaaaa")
    for ix in range(0, 10):
        x = width / 20 + ix * width / 10
        draw.line((x, 0, x, height), fill="#aaaaaa")
    x = 15
    for c in hash:
        rx = random.randint(1, 6)
        ry = random.randint(0, 10)
        draw.text((x+rx, ry), c, font=font, fill="#000000")
        x += 26
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