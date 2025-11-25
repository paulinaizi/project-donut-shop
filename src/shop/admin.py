from django.contrib import admin
from .models import CustomUser, Coating, Sprinkle, Donut

admin.site.register(CustomUser)
admin.site.register(Coating)
admin.site.register(Sprinkle)
admin.site.register(Donut)