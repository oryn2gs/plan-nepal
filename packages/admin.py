from django.contrib import admin
from packages.models import (
    Destination,
    Type,
    Package,
    TourTimeline
    )

class TourTimelineInlines(admin.StackedInline):
    model = TourTimeline
    extra = 0

class PackageAdmin(admin.ModelAdmin):
    inlines = [TourTimelineInlines]
    exclude = ["slug"]
    list_display = ['name', 'destination', 'price', 'discount']
    list_filter = ['destination', 'type']

# class TourTimelineAdmin(admin.ModelAdmin):
#     list_display = ['tour_timeline', 'day', 'stop_name' ]

admin.site.register(Destination)
admin.site.register(Type)
admin.site.register(Package, PackageAdmin)
# admin.site.register(TourTimeline, TourTimelineAdmin)