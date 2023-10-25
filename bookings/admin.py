from django.contrib import admin

from bookings.forms import InquiryAdminForm

from bookings.models import (
    Booking,
    Inquiry,
    InquiryAnswer
)


# class BookingAdmin(admin.ModelAdmin):
#     list_display = ['id']

admin.site.register(Booking)




class InquiryAnswerInline(admin.TabularInline):
    model = InquiryAnswer
    extra = 1
    fields = ('content',)


class InquiryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "inquiry_type", "inquiry_resolved"]
    list_filter = ["inquiry_type", "inquiry_resolved", "created_on"]
    InquiryAdminForm = InquiryAdminForm
    inlines = [InquiryAnswerInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print("user", request.user, request.user.slug)

        # !need to fix the reply for Inquiry
        if not obj.inquiry_resolved and form.cleaned_data.get('inquiry_answer_content'):
            InquiryAnswer.objects.create(
                inquiry=obj,
                user=request.user,
                content=form.cleaned_data['inquiry_answer_content']
            )

admin.site.register(Inquiry, InquiryAdmin)


class InquiryAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "inquiry", "user"]
    list_filter = ["user", "timestamp"]
admin.site.register(InquiryAnswer, InquiryAnswerAdmin)


