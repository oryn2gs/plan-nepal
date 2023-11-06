from django.contrib import admin

from bookings.forms import InquiryAdminForm

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
    fields = ('content',)


class InquiryAdmin(admin.ModelAdmin):
    list_display = ["user", "inquiry_type", "replied_by", "inquiry_resolved"]
    list_filter = ["inquiry_type", "inquiry_resolved", "created_on"]
    inlines = [InquiryAnswerInline]

    #! Need to fix -- while creating a INquiryANswer --need to a assign user

    def replied_by(self, obj):
        """ Fetches user of InquiryAnswer related to Inquiry

        Args:
            obj (_type_): Inquiry obj

        Returns:
            _type_: InquiryAnswer user if any or none
        """
        return obj.answer.user



admin.site.register(Inquiry, InquiryAdmin)






