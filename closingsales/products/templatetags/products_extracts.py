from django import template
from django.urls import resolve
from django.urls import reverse

register = template.Library()

@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter(name='contains')
def contains(text, contain):
    if isinstance(text, str):
        if contain in text:
            return True
    return False

@register.filter(name='dashboardtext')
def dashboardtext(text):
    if isinstance(text, str):
        words = text.split('/')
        if len(words) <= 3:
            return 'Home'
        else:
            return words[-2].title()
    return text

@register.filter(name='breadcrumb')
def breadcrumb(text):
    if isinstance(text, str):
        words = text.split('/')
        # import pdb; pdb.set_trace()
        last_world = words.pop()
        if not last_world:
            return '<li class="active">' + words[-1].title() + '</li>'
        else:
            words.append('')
            match = resolve("/".join(words))
            url = reverse(match.url_name)
            return '<li><a href="' + url + '">' + words[-2].title() + '</a></li><li class="active">' + last_world.title() + '</li>'
    return text
