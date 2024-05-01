from django.contrib import admin
from .models import User, Admin, Client, Stylist


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'start_date', 'role',
                    'is_staff', 'is_active', )


admin.site.register(User, UserAdmin)


class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)


admin.site.register(Admin, AdminAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone_number', 'residency')


admin.site.register(Client, ClientAdmin)


class StylistAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'phone_number', 'residency', 'next_of_kin_name', 
                    'next_of_kin_phone', 'emergency_contact_name', 'emergency_contact_phone', 'location')


admin.site.register(Stylist, StylistAdmin)
