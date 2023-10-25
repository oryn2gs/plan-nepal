from django import forms
from bookings.models import Inquiry

class InquiryAdminForm(forms.ModelForm):
    inquiry_answer_content = forms.CharField(
        required=False,
        label='Inquiry Answer',
        widget=forms.Textarea(attrs={'rows': 3}),
    )
    class Meta:
        model = Inquiry
        fields = '__all__'

