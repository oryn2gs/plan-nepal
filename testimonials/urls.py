
from django.urls import path
from testimonials.views import create_testimonial


urlpatterns = [
    path('create/', create_testimonial, name="create-testimonial"),
]
