from django import template
from django.urls import resolve
from django.urls import reverse
register = template.Library()


@register.filter(name='extract')
def extract(text):
    if isinstance(text, str):
        index = text.index('</p>')
        return text[:index+4]
    return text


@register.filter(name='imageurl')
def imageurl(arr):
    img = arr.first()
    return img.file.url