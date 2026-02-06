from django import template

register = template.Library()

@register.filter
def get_field_display(obj, field_name):
    method_name = f'get_{field_name}_display'
    if hasattr(obj, method_name):
        return getattr(obj, method_name)()
    return getattr(obj, field_name)

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)