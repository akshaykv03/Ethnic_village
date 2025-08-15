from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Stay)
admin.site.register(Booking)
admin.site.register(Feedback)