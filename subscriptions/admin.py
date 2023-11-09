from django.contrib import admin
from subscriptions.models import Subscription

class SubcriptionsAdmin(admin.ModelAdmin):
    list_display = ["email", "active", "created_on"]
    list_filter = ["active"]
    readonly_fields = ["id"]


admin.site.register(Subscription, SubcriptionsAdmin)
