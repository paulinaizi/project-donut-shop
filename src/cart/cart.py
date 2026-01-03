import json
from shop.models import Donut, Coating, Sprinkle, TopCoating


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})

    def _make_key(self, donut_id, toppings):
        if not toppings:
            return str(donut_id)

        toppings_key = json.dumps(toppings, sort_keys=True)
        return f"{donut_id}:{toppings_key}"

    def add(self, donut_id, toppings=None, qty=1):
        key = self._make_key(donut_id, toppings)

        if key in self.cart:
            self.cart[key]['qty'] += qty
        else:
            self.cart[key] = {
                'donut_id': donut_id,
                'toppings': toppings,
                'qty': qty
            }

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def _calc_price(self, donut, toppings):
        price = donut.price
        if donut.is_custom_base:
            for topping in toppings.values():
                price += topping.price
        return price

    def get_total_price(self):
        return sum(item['total_price'] for item in self)

    def __iter__(self):
        for key, item in self.cart.items():
            donut = Donut.objects.get(id=item['donut_id'])

            toppings = {}
            if item['toppings']:
                if item['toppings'].get('coating'):
                    toppings['coating'] = Coating.objects.get(id=item['toppings']['coating'])
                if item['toppings'].get('sprinkle'):
                    toppings['sprinkle'] = Sprinkle.objects.get(id=item['toppings']['sprinkle'])
                if item['toppings'].get('topCoating'):
                    toppings['topCoating'] = TopCoating.objects.get(id=item['toppings']['topCoating'])

            unit_price = self._calc_price(donut, toppings)

            yield {
                'key': key,
                'donut': donut,
                'toppings': toppings,
                'qty': item['qty'],
                'is_custom': donut.is_custom_base,
                'unit_price': unit_price,
                'total_price': unit_price * item['qty']
            }
