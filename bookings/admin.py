from django.contrib import admin

from bookings.models import (
    Booking,
    Inquiry,
    InquiryAnswer
)

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'arrival_date', 'airport_pickup', 'bookings_fullfilled', 'payments_done']
    list_filter = ['bookings_fullfilled', 'package']
    readonly_fields = ['total_price']
    raw_id_fields = ["package"]

admin.site.register(Booking, BookingAdmin)


class InquiryAnswerInline(admin.StackedInline):
    model = InquiryAnswer
    extra = 1
    raw_id_fields = ["user"]


class InquiryAdmin(admin.ModelAdmin):
    list_display = ["user", "inquiry_type", "replied_by", "inquiry_resolved"]
    list_filter = ["inquiry_type", "inquiry_resolved", "created_on"]
    inlines = [InquiryAnswerInline]


    def replied_by(self, obj):
        """ Fetches user of InquiryAnswer related to Inquiry

        Args:
            obj (_type_): Inquiry obj

        Returns:
            _type_: InquiryAnswer user if any or none
        """
        return obj.answer.user
    
    def get_formsets_with_inlines(self, request, obj=None):
        # Include the InquiryAnswerInline formset only if an Inquiry object is being edited
        if obj:
            return super().get_formsets_with_inlines(request, obj)
        else:
            return []


admin.site.register(Inquiry, InquiryAdmin)





