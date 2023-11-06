from django.db import models
import uuid
import random
from django.conf import settings

from django.utils import timezone
from typing import Dict, Any, List

class TestimonialManager(models.Manager):
   

    def get_random_testimonial(self, length:int = 6) -> List[Dict[str, Any]]:
        """ Returns random six testimonial if the length of the queryset is larger than 6.

        Args:
            length (int, optional): _description_. Defaults to 6.

        Returns:
            List[Dict[str, Any]]: _description_
        """

        queryset = self.get_queryset()
        random_queryset = queryset
        if len(queryset) > length:
            random_queryset = random.sample(list(queryset), length)
        return random_queryset



class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="testimonials")
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = TestimonialManager()

    def __str__(self) -> str:
        return f"Testimonial from {self.user.email}"
    


