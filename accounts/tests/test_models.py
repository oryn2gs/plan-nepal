from django.test import TestCase
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Profile

from django.contrib.auth import get_user_model
User = get_user_model()


class UserModelTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password="password"
        )

        self.user_data = {
            "email" : "test@email.com",
            "password" : "password" 
        }

    def test_str_method(self) -> None:
        self.assertEqual(str(self.user), self.user.email)

    def test_user_slug(self) -> None:
        self.assertEqual(self.user.slug, slugify(self.user.email))

    def test_absolute_url_methods(self) -> None:
        # add the urls
        pass

    def test_user_create_method(self) -> None:
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
    
    def test_create_staff_method(self) -> None:
        user = User.objects.create_staff(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_admin)
    
    def test_create_superuser_method(self) -> None:
        user = User.objects.create_superuser(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)


    
class ProfileModel(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email= "test@email.com",
            password = "password",
        )
        self.profile = self.user.profile
    
    def test_str_method(self) -> None:
        self.assertEqual(str(self.profile), self.user.email)
    
    def test_profile_created_related_to_user(self) -> None:
        self.assertIsNotNone(self.profile)
    
    def test_fullname_method(self) -> None:
        self.profile.firstname = "Jhon"
        self.profile.lastname = "Doe"
        self.profile.save()

        self.assertEqual(self.profile.get_fullname.lower(), "jhon doe")

    def test_profile_image_upload(self):
        image = SimpleUploadedFile(
            "test_image.png",
            content=b"file_content",
            content_type="image/png"
        )
        self.profile.profile_image = image
        self.profile.save()
        self.assertTrue(self.profile.profile_image.url.startswith('/media/accounts/profile_image/'))

    def tearDown(self):
        try:
            profile = self.user.profile
            if profile.profile_image:
                default_storage.delete(profile.profile_image.name)
        except Profile.DoesNotExist:
            pass




    

    

    


        
    