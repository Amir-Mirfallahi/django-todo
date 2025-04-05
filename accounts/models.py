from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email, password and extra fields.
        """
        if not email:
            raise ValueError(_("ایمیل باید تنظیم شود."))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Super User with the given email, password and extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("سوپر ادمین باید دارای is_staff=True باشد."))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("سوپر ادمین باید دارای is_superuser=True باشد."))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    bio = models.TextField(blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    When User send `save` signal, automatically generate the profile ofr the created User
    """

    if created:
        Profile.objects.create(user=instance)
