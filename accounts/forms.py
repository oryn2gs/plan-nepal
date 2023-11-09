from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, 
    UserCreationForm,
)
from django.utils.translation import gettext as _
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
class EmailField(forms.EmailField):
    """ Custom EmailField -- with a validation method which checks if the user already exists in the database.

    Args:
        forms (_type_): Django forms Charfield
    """ 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = forms.EmailInput(
            attrs={
            'placeholder': 'Email'
            })


    def clean(self, value: str) -> Any:
        email = super().clean(value)
        user_exists = User.objects.filter(email__iexact=email).first()
        if not user_exists:
            raise ValidationError("User with that email does not exists!")
        return email

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password"
            }
        )
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password"
            }
        )
        )
    
    class Meta: 
        model = User
        fields = ["email", "password", "confirm_password"]

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "User with that email already exists!",
                code="email_already_exists"
                )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError({
                "confirm_password":"Password and confirm password must match"
                }, code="password_no_match")

        return cleaned_data
    

class UserLoginForm(forms.Form):
    email = EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password"
            }
        )
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(email=self.cleaned_data.get("email"))
            if not user.check_password(password):
                raise forms.ValidationError(
                    "Please enter a valid password",
                    code="wrong_password"
                    )
        except User.DoesNotExist as e:
            None
        
        return password
    
    
    
class RequestResetPasswordForm(forms.Form):
    email = EmailField()



class PasswordResetForm(forms.Form):

    password = forms.CharField(
        help_text="A password must not be less than 8 character, must contain atleast one number, one uppercase, one lowercase and a special charater. ",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password"
            }
        ),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
            }
        )
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


