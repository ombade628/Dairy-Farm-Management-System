from django import template

register = template.Library()

@register.simple_tag(name="multiply")
def multiply(qty, unit_price, *args, **kwargs):
    """
    Multiply quantity by unit price.
    
    Usage:
        {% multiply qty unit_price %}
    
    Args:
        qty: The quantity value
        unit_price: The unit price value
    
    Returns:
        The product of qty and unit_price
    """
    try:
        return float(qty) * float(unit_price)
    except (TypeError, ValueError):
        return 0

@register.simple_tag(name="subtotal")
def subtotal(price, quantity, *args, **kwargs):
    """
    Calculate subtotal with proper type handling.
    
    Usage:
        {% subtotal price quantity %}
    """
    try:
        return float(price) * float(quantity)
    except (TypeError, ValueError):
        return 0

@register.filter(name="multiply_filter")
def multiply_filter(value, arg):
    """
    Filter to multiply a value by an argument.
    
    Usage:
        {{ qty|multiply_filter:unit_price }}
    """
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0

@register.simple_tag(name="add_vat")
def add_vat(price, vat_percentage=13):
    """
    Add VAT to a price.
    
    Usage:
        {% add_vat price 13 %}
    """
    try:
        return float(price) * (1 + float(vat_percentage) / 100)
    except (TypeError, ValueError):
        return 0

@register.simple_tag(name="format_currency")
def format_currency(value, currency_symbol="₹"):
    """
    Format a value as currency.
    
    Usage:
        {% format_currency value "₹" %}
    """
    try:
        return f"{currency_symbol}{float(value):.2f}"
    except (TypeError, ValueError):
        return f"{currency_symbol}0.00"