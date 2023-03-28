from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(cake,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==cake.id:
            return True
    return False    

@register.filter(name='cart_quantity')
def cart_quantity(cake,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==cake.id:
            return cart.get(id)
    return 0   

@register.filter(name='price_total')
def price_total(cake,cart):
    return cake.price * cart_quantity(cake,cart)

@register.filter(name='total_cart_price')
def total_cart_price(cakes,cart):
    sum=0;
    for p in cakes:
        sum += price_total(p,cart)
    return sum

@register.filter(name='multiply')
def multiply(number,number1):
    return number*number1