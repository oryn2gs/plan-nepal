from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
import uuid
from django.utils.text import slugify


class UserManager(BaseUserManager):

    def create_user(self, email:str, password:str=None) -> models.Model:

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email:str, password:str) -> models.Model:
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user


    def create_superuser(self, email:str, password:str) -> models.Model:
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    slug = models.SlugField(primary_key=True, unique=True, editable=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.email)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'slug': self.slug})

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin




def profile_image_fs(instance, _) -> str:
    return f"accounts/profile_image/{instance.id}.png"


class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender')
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_image_fs, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def get_fullname(self) -> str:
        if self.firstname and self.lastname:
            return f"{self.firstname} {self.lastname}"
        return None
    
    @property
    def get_profile_image(self) -> str:
        if self.profile_image:
            return self.profile_image.url
        return "/media/accounts/profile_image/profile_image_default.png"



