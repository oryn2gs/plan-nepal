from subscriptions.models import Subscription
from django import forms

class SubscriptionsForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email"
            }
        )
    )

    class Meta:
        model = Subscription
        fields = ["email"]

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if Subscription.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email you\'ve provided is already in the subscription list."
            )
        
        return email

    

    