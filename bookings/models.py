from django.db import models
from django.db.models import Q
from django.conf import settings

import uuid
from packages.models import Package


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="package_bookings")
    kids = models.PositiveIntegerField(
        default = 0,
        help_text="Age below 12 yrs old"
    )
    adults = models.PositiveIntegerField(
        default = 0,
        help_text="Age above 12 yrs old"
    )
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    airlines = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=50)
    airport_pickup = models.BooleanField(default=True)
    message = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(
        default=0, decimal_places=2, max_digits=10)
    bookings_fullfilled = models.BooleanField(default=False)
    payments_done = models.BooleanField(default=False)
    booked_on = models.DateTimeField(auto_now_add=True)

    # ! add payments when necessary

    def __str__(self) -> str:
        return f"Bookings made by {self.user.email} for {self.package.name}"
    
    def save(self, *args, **kwargs):
        if self.package:
            final_price_after_discount = self.package.get_final_price_after_discount

            self.total_price = round(final_price_after_discount * (self.kids + self.adults), 2)
        return super().save(*args, **kwargs)
        #Todos: change it based on pricing(for kids and adults)
        


class InquiryManager(models.Manager):

    def filter_inquiry_by_resolved_value(self, resolved:bool = False) -> models.QuerySet:
        queryset = self.get_queryset().filter(
            Q(inquiry_resolved=resolved) & Q(active=True)
            )
        #  * chain filter if necessary chain filter when
        return queryset
    

class Inquiry(models.Model):
    TYPE_CHOICES = [
        ('destination', 'Destination'),
        ('packages', 'Packages'),
        ('pricing', 'Pricing'),
        ('tickets', 'Tickets'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inquiries")
    inquiry_type = models.CharField(
        choices=TYPE_CHOICES,
        default="packages",
        max_length=25
    )
    question = models.CharField(max_length=500, null=False, blank=False)
    inquiry_resolved = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = InquiryManager()

    def __str__(self):
        return str(self.id)
    


class InquiryAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inquiry = models.OneToOneField(
        Inquiry, 
        on_delete=models.CASCADE,
        related_name="answer"
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.user:
            self.user = self.request.user
        return super().save(*args, **kwargs)














    
    

    


