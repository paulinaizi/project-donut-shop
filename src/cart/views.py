import json
from datetime import datetime, timezone
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import OrderItem
from .cart import Cart
from .forms import OrderForm


def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart_summary.html', {'total_price': cart.get_total_price()})


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


def checkout(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        return redirect('cart_summary')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.total_price = cart.get_total_price()
            order.created_at = datetime.now(timezone.utc)
            order.save()

            for item in cart:
                toppings_data = {}

                if 'coating' in item['toppings']:
                    toppings_data['coating'] = {
                        'name': item['toppings']['coating'].name,
                        'price': str(item['toppings']['coating'].price),
                    }

                if 'sprinkle' in item['toppings']:
                    toppings_data['sprinkle'] = {
                        'name': item['toppings']['sprinkle'].name,
                        'price': str(item['toppings']['sprinkle'].price),
                    }

                if 'topCoating' in item['toppings']:
                    toppings_data['topCoating'] = {
                        'name': item['toppings']['topCoating'].name,
                        'price': str(item['toppings']['topCoating'].price),
                    }

                OrderItem.objects.create(
                    order=order,
                    donut_name=item['donut'].name,
                    toppings=toppings_data or None,
                    qty=item['qty'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price'],
                )

            cart.clear()
            return redirect('order_success', order_id=order.id)

    else:
        if request.user.is_authenticated:
            form = OrderForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            })
        else:
            form = OrderForm()

    return render(
        request,
        'checkout.html',
        {
            'form': form,
            'total_price': cart.get_total_price(),
        }
    )


def order_success(request, order_id):
    return render(request, 'order_success.html', {'order_id': order_id})