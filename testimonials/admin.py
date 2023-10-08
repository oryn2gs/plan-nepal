from django.contrib import admin

from testimonials.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "content"]

admin.site.register(Testimonial, TestimonialAdmin)