from django.contrib import admin

from testimonials.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["user", "created_on"]
    list_filter = ["created_on", "user"]

admin.site.register(Testimonial, TestimonialAdmin)