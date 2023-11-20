from django import forms
from bookings.models import (
    Booking
    )
from django.contrib.auth import get_user_model
User = get_user_model()


class BookingForm(forms.ModelForm):

    kids = forms.IntegerField(
        required=False,
        initial=0,
        help_text="Age below 12 yrs old",
        min_value=0,
    )

    arrival_date = forms.DateField(
        widget=forms.DateInput(
                attrs={
                'type': 'date',
                'class': 'w-full grow'
            }
            
        ),
    )
    arrival_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    airport_pickup = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "sr-only peer"
            }
        ),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3, 'cols': 30, 'placeholder': "If you have any messages"
                }
            ),
    )


    class Meta:
        model = Booking
        fields = "__all__"
        exclude = [
            "user", "package",  "total_price", "bookings_fullfilled", "payments_done"
            ]
        

   
