from django.contrib import admin

from .models import Property
from .models import PropertyType
from .models import Provider
from .models import Council
from .models import Support


class PropertyAdmin(admin.ModelAdmin):
    pass


class PropertyTypeAdmin(admin.ModelAdmin):
    pass


class ProviderAdmin(admin.ModelAdmin):
    pass


class CouncilAdmin(admin.ModelAdmin):
    pass


class SupportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Council, CouncilAdmin)
admin.site.register(Support, SupportAdmin)

admin.site.site_header = 'HomePointr admin'
