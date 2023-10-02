from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.urls import reverse
import uuid

class Destination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name 
    

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.name
    

# ----------- Package Model ----------

class PackageManager(models.Manager):
    """ Package manager """

    def filter_by_destination(self, destination: str) -> models.QuerySet:
        queryset = self.get_queryset().filter(
            Q(destination__name__iexact=destination) & Q(active=True)
            )
        return queryset
    
    
    def filter_by_type(self, type_name: str) -> models.QuerySet:
        queryset = self.get_queryset().filter(
            Q(type__name__iexact=type_name) & Q(active=True)
            )
        return queryset
    

def package_fs(instance, filename: str) -> str:
    """ Image storage path for Package image"""
    return f"package_image/{instance.slug}.png"


class Package(models.Model):
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="package")
    type = models.ManyToManyField(Type, blank=True)
    name = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField()
    image = models.ImageField(upload_to=package_fs, default="package_image/default.png")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.PositiveIntegerField(blank=True, null=True)
    cost_information = models.TextField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = PackageManager()

    def __str__(self) -> str:
        return f"{self.destination.name} | {self.name}"
    
    def get_absolute_url(self):
        return reverse('package-detail', kwargs={'slug': self.slug})    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_final_price_after_discount(self):
        return self.price - self.discount
        


# --------------TourTimeline-------
class TourTimelineManager(models.Manager):

    def filter_instance_related_to_package(self, package_slug: str, ascending: bool =True) -> models.QuerySet:

        queryset = self.get_queryset().filter(tour_timeline__slug=package_slug)
        queryset = queryset.order_by("day") if ascending else  queryset.order_by("-day")
        
        return queryset


class TourTimeline(models.Model):
    """ Many-to-one relation to packages which stores packages related timeline information  """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tour_timeline = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="tour_timeline")
    stop_name = models.CharField(max_length=250)
    description = models.TextField()
    day = models.PositiveIntegerField(
        help_text="days count into the trip: int"
    )

    objects = TourTimelineManager()

    def __str__(self):
        return f"day:{self.day} at {self.stop_name}"
    

