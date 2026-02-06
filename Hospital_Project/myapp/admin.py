from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(Doctor)

admin.site.register(Patient)

admin.site.register(Appointment)