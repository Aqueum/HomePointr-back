from django.contrib import admin

from .models import Provider
from .models import PropertyType
from .models import Council
from .models import Support
from .models import Property
from .models import Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0
    inlines = [PhotoInline]


class ProviderAdmin(admin.ModelAdmin):
    inlines = [PropertyInline]
    list_display = ('property_name')
    search_fields = ['property_name']


admin.site.register(Provider, ProviderAdmin)
