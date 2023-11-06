from typing import Any
from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, 
    UserCreationForm,
)
from accounts.models import Profile
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password is not None and password != confirm_password:
            self.add_error("confirm_password", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        return self.initial["password"]
    


# ---------Users forms------------------------


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
        )
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
        )
    
    class Meta: 
        model = User
        fields = ["email", "password", "confirm_password"]

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        
        user_exists = User.objects.filter(email__iexact=email).first()
        if user_exists:
            raise ValidationError("User with that email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password and confirm password must match")

        return cleaned_data

    

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
        )
    

    def clean(self) -> dict[str, Any]:
        from django.utils.translation import gettext as _
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        user = self._get_user(email)
        if not user:
            raise ValidationError(
                _("User with %(value)s does not exists."), 
                code="invalid email",
                params={"value": email}
            )
        
        password_match = user.check_password(password)
        if not password_match:
            raise ValidationError(
                _("The password that you provided is incorrect"),
                code="invalid password"
            )
        
        return cleaned_data
    
    def _get_user(self, email: str) -> User:
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        return user
    
    
    
class PasswordResetForm(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password and confirm password must match.")

        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
                attrs={
                'type': 'date',
                'class': 'w-full grow'
            }
            
        ),
    )
    
    class Meta:
        model = Profile 
        fields = "__all__"
        exclude = ["user"]

    
# ---Rendering none field errors in templates
# <form method="post">
#     {% csrf_token %}
#     {{ form.as_p }}

#     {% if form.errors %}
#         <ul>
#             {% for field, errors in form.errors.items %}
#                 {% if field == '__all__' %}
#                     {% for error in errors %}
#                         <li>
#                             {% if error.code == "invalid_value" %}
#                                 Invalid Value Error: {{ error.message }}
#                             {% endif %}
#                         </li>
#                     {% endfor %}
#                 {% endif %}
#             {% endfor %}
#         </ul>
#     {% endif %}

#     <input type="submit" value="Submit">
# </form>


