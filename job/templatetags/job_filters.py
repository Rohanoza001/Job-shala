from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key)

@register.filter
def split(value, arg):
    """Split a string by the given argument"""
    return value.split(arg)

@register.filter
def strip(value):
    """Strip whitespace from a string"""
    return value.strip()

@register.filter
def line_clamp(value, arg):
    """Limit text to specified number of lines"""
    lines = value.split('\n')
    if len(lines) <= int(arg):
        return value
    return '\n'.join(lines[:int(arg)]) + '...' 