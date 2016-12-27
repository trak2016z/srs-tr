from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def pag_extra(obj, page):
    dic = getattr(obj, 'args', {})
    dic.update({'page': page})
    return reverse(obj.url, kwargs=dic)+obj.url_add
