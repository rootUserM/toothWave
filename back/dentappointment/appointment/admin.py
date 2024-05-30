from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Owner,ConsultingRoom, Appointment,Patient, Treatment, Service, Payment
from django.contrib.auth.admin import UserAdmin
admin.site.register(ConsultingRoom)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Treatment)
admin.site.register(Service)
admin.site.register(Payment)
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Owner, CustomUserAdmin)
