from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=','):
    """Split a string by delimiter. Usage: {{ value|split:',' }}"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]


@register.filter(name='subtract')
def subtract(value, arg):
    """Subtract arg from value. Usage: {{ value|subtract:6 }}"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
