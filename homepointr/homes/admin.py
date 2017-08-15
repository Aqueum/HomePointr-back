from django.contrib import admin

from .models import Bread


class BreadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bread, BreadAdmin)

admin.site.site_header = 'HomePointr admin'
