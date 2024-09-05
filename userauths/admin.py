from django.contrib import admin
from userauths.models import User, ContactUs

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']
    
admin.site.register(User, AdminUser)
admin.site.register(ContactUs, ContactUsAdmin)