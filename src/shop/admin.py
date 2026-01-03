from django.contrib import admin
from .models import CustomUser, Donut, Coating, Sprinkle, TopCoating


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined', 'is_active')
    ordering = ('-date_joined',)
    search_fields = ('email', 'last_name')
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Donut)
class DonutAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ('name',)
    search_fields = ('name',)
    

@admin.register(Coating)
class CoatingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Sprinkle)
class SprinkleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(TopCoating)
class TopCoatingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ('name',)
    search_fields = ('name',)