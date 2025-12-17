from django.contrib import admin
from .models import CustomUser, Donut, Coating, Sprinkle, TopCoating

admin.site.register(CustomUser)
admin.site.register(Donut)
admin.site.register(Coating)
admin.site.register(Sprinkle)
admin.site.register(TopCoating)