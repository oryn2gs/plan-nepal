from django.db import models
import uuid

# Create your models here.

def ts_image_fs(instance, filename):
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

    def __str__(self):
        return f"{self.username} from {self.city}, {self.country}"
    


