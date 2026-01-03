from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        'donut_name',
        'formatted_toppings',
        'qty',
        'unit_price',
        'total_price',
    )
    fields = (
        'donut_name',
        'formatted_toppings',
        'qty',
        'unit_price',
        'total_price',
    )

    def formatted_toppings(self, obj):
        if not obj.toppings:
            return '-'
        
        labels = {
            'coating': 'Polewa',
            'sprinkle': 'Posypka',
            'topCoating': 'Dodatkowa polewa',
        }

        lines = []
        for key, data in obj.toppings.items():
            label = labels.get(key, key)
            lines.append(f'{label}: {data.get('name')}')
        return '\n'.join(lines)
    
    formatted_toppings.short_description = 'Dodatki'

    def has_add_permission(self, request, obj):
        return False
    
    def has_change_permission(self, request, obj):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'email',
        'phone',
        'total_price',
        'status'
    )

    list_filter = ('status', 'created_at')
    search_fields = ('id', 'email', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total_price')

    inlines = [OrderItemInline]
