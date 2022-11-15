from django import template

register = template.Library()


@register.filter
def path_modifier(value):
    url_parts = value.split('/')
    return '/' + '/'.join(url_parts[2:])
