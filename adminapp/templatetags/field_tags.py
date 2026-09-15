import builtins
from django import template
register = template.Library()

@register.filter
def getattr(obj, arg):
    """动态获取对象属性"""
    if obj is None:
        return ''
    return builtins.getattr(obj, arg, '')
