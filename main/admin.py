from django.contrib import admin
from main.models import Comuna, Region, Inmueble, UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Inmueble)