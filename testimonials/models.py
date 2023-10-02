from django.db import models
import uuid
import random


class TestimonialManager(models.Manager):

    def get_random_testimonial(self, length:int = 6) -> list :
        queryset = self.get_queryset()
        random_six_queryset = random.sample(list(queryset), length)
        return random_six_queryset


def ts_image_fs(instance, filename:str):
    return f"testimonial_image/{instance.username}.png"


class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    user_image = models.ImageField(
        upload_to=ts_image_fs, default="testimonial/default.png"
        )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    objects = TestimonialManager()

    def __str__(self) -> str:
        return f"{self.username} from {self.city}, {self.country}"
    


