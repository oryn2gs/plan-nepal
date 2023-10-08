from django.db import models
import uuid
import random
from django.conf import settings

from django.utils import timezone


class TestimonialManager(models.Manager):

    def get_random_testimonial(self, length:int = 6) -> list :
        queryset = self.get_queryset()
        random_six_queryset = random.sample(list(queryset), length)
        return random_six_queryset



class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="testimonials")
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)


    objects = TestimonialManager()

    def __str__(self) -> str:
        return f"Testimonial from {self.user.email}"
    


