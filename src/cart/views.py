from django.shortcuts import render
from .cart import Cart
from shop.models import Donut, Coating, Sprinkle, TopCoating
from django.http import JsonResponse
import json


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart_summary.html', {'cart': cart})


def cart_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        donut_id = str(data.get('donut_id'))
        toppings = data.get('toppings') or {}

        cart = Cart(request)
        cart.add(
            donut_id=donut_id,
            toppings=toppings,
            qty=1
        )

        return JsonResponse({
            'status': 'ok',
            'cart': cart.cart,
            'cart_quantity': len(cart)
        })


def cart_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')

        cart = Cart(request)
        cart.remove(key)

        return JsonResponse({
            'status': 'ok',
            'cart_quantity': len(cart)
        })


def cart_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        key = data.get('key')
        qty = int(data.get('qty', 1))

        cart = Cart(request)

        if key in cart.cart:
            if qty > 0:
                cart.cart[key]['qty'] = qty
                cart.save()
            else:
                cart.remove(key)

        return JsonResponse({
            'status': 'ok',
            'cart_quantity': len(cart)
        })
