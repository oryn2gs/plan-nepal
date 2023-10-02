from django.contrib import admin

from testimonials.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["username", "city", "country"]

admin.site.register(Testimonial, TestimonialAdmin)