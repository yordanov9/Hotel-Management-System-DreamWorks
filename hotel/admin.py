from django.contrib import admin

# Register your models here.
from hotel.models import Room, Booking, UserProfile

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(UserProfile)