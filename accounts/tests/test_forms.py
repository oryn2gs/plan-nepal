from django.test import TestCase
from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm,
    PasswordResetForm
    )
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationFormTestCase(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }


    def test_signup_form_valid(self) -> None:
        form = UserRegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid() , form.errors)

    def test_signup_form_invalid_email_already_exists(self) -> None:
        User.objects.create_user(
            email='test@example.com', 
            password='existingpassword',
        )

        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("User with that email already exists.", form.errors["email"])

    def test_signup_form_invalid_password_mismatch(self) -> None:
        self.form_data['password'] = 'securepassword123'
        self.form_data['confirm_password'] = 'differentpassword'

        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("Password and confirm password must match", form.errors['__all__'])



class UserLoginFormTestCase(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            'email': 'test@example.com',
            'password': 'securepassword123'
        }

        self.user = User.objects.create_user(**self.form_data)


    def test_login_form_valid(self) -> None:
        form = UserLoginForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)


    def test_login_form_invalid_incorrect_password(self) -> None:
        self.form_data["password"] = "wrongpassword"

        form = UserLoginForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("The password that you provided is incorrect", form.errors["__all__"])
    


    def test_login_form_invalid_email_does_not_exists(self) -> None:
        self.form_data['email'] = "wrong@email.com"
        
        form = UserLoginForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn(f"User with {self.form_data['email']} does not exists.", form.errors["__all__"])


class PasswordResetFormTestCase(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            'password': 'securepassword123',
            'confirm_password': 'securepassword123'
        }


    def test_reset_password_form_valid(self) -> None:
        form = PasswordResetForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_reset_password_form_invalid(self) -> None:
        self.form_data["confirm_password"] = "unmatchingpassword"

        form = PasswordResetForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("Password and confirm password must match.", form.errors["__all__"])