from django.db import models
from django.conf import settings


class Order(models.Model):
    class Status(models.IntegerChoices):
        NEW = 1, 'Nowe'
        IN_PROGRESS = 2, 'W realizacji'
        DONE = 3, 'Zrealizowane'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='orders', verbose_name='użytkownik')
    first_name = models.CharField(max_length=100, verbose_name='imię')
    last_name = models.CharField(max_length=100, verbose_name='nazwisko')
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='numer telefonu')
    street_address = models.CharField(max_length=100, verbose_name='ulica') 
    postal_code = models.CharField(max_length=6, verbose_name='kod pocztowy')
    city = models.CharField(max_length=100, verbose_name='miasto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='kwota łączna')
    status = models.IntegerField(choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f'Zamówienie #{self.id}'

    class Meta:
        verbose_name = 'Zamówienie'
        verbose_name_plural = 'Zamówienia'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='zamówienie')
    donut_name = models.CharField(max_length=100, verbose_name='nazwa donuta')
    toppings = models.JSONField(blank=True, null=True, verbose_name='dodatki')
    qty = models.PositiveIntegerField(default=1, verbose_name='ilość')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='cena za sztukę')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='cena łączna')

    def __str__(self):
        return f'{self.donut_name} x{self.qty}'

    class Meta:
        verbose_name = 'Pozycja zamówienia'
        verbose_name_plural = 'Pozycje zamówienia'
