from django.contrib import admin
from .models import ServerModel,ServerUseModel


# Register your models here.
class ServerAdmin(admin.ModelAdmin):
    list_display_links = ['name', 'addr']
    list_display = ['name', 'addr']


class ServerUseAdmin(admin.ModelAdmin):
    list_display_links = ['user','server']
    list_display = ['user','server']

admin.site.register(ServerModel,ServerAdmin)
admin.site.register(ServerUseModel,ServerUseAdmin)