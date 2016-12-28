from django import template

register = template.Library()

@register.filter
def zero_prepend(value):
    s = str(value)
    l = 2
    if len(s) < l:
        return "0" * (l - len(s)) + s
    return s
