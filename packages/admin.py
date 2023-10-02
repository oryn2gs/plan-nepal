from django.contrib import admin
from packages.models import (
    Destination,
    Type,
    Package,
    TourTimeline
    )


class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'price', 'discount']
    prepopulated_fields = {'slug':('name',)}

class TourTimelineAdmin(admin.ModelAdmin):
    list_display = ['tour_timeline', 'day', 'stop_name' ]

admin.site.register(Destination)
admin.site.register(Type)
admin.site.register(Package, PackageAdmin)
admin.site.register(TourTimeline, TourTimelineAdmin)