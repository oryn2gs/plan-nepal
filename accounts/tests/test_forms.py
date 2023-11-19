from django.test import TestCase
from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm,
    PasswordResetForm,
    RequestResetPasswordForm
    )
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailFormFieldTestCase(TestCase):

    def setUp(self) -> None:
        self.form_class = RequestResetPasswordForm
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password = "password"
        )

    def test_field_valid(self) -> None:
        data = {
            "email": "testuser@email.com"
        }

        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        
    
    def test_field_invalid_user_does_not_exists(self) -> None:
        data = {
            "email": "wronguser@email.com"
        }
        form = self.form_class(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEquals(
            "User with that email does not exists!",
            form.errors["email"][0])



class UserRegistrationFormTestCase(TestCase):

    def setUp(self) -> None:
        self.form_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }

    def test_signup_form_valid(self) -> None:
        form = UserRegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_invalid_email_already_exists(self) -> None:
        User.objects.create_user(
            email='test@example.com', 
            password='existingpassword',
        )

        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("User with that email already exists!", form.errors["email"])

    def test_signup_form_invalid_password_mismatch(self) -> None:
        self.form_data['password'] = 'securepassword123'
        self.form_data['confirm_password'] = 'differentpassword'

        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("Password and confirm password must match", form.errors['confirm_password'])



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

    def test_login_form_invalid_email_does_not_exists(self) -> None:
        self.form_data['email'] = "wrong@email.com"
        
        form = UserLoginForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("User with that email does not exists!", form.errors["email"])
    
    def test_login_form_invalid_password_no_match(self) -> None:
        self.form_data['password'] = "wrongpassword"
        
        form = UserLoginForm(data=self.form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("Please enter a valid password", form.errors["password"])
        


class RequestResetPasswordFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password = "password",
        )


    def test_request_reset_password_form_valid(self) -> None:
        form_data = {
            "email": "testuser@email.com"
        }
        form = RequestResetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_request_reset_password_form_invalid(self) -> None:
        form_data = {
            "email": "wrongemail@email.com"
        }

        form = RequestResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("User with that email does not exists!", form.errors["email"])


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