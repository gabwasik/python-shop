from django.template.defaulttags import register


@register.filter
def multiply_quantity(price, quantity):
    return float(price) * int(quantity)
