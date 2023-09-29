from testimonials.models import Testimonial
from django.forms import ModelForm

class TestimonialForm(ModelForm):
    class Meta:
        model = Testimonial
        fields = ['username', 'content', 'user_image', 'city', 'country']