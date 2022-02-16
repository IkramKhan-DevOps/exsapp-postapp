from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField

"""
At the start please be careful to start migrations
--------------------------------------------------

STEP: 1 comment current_subscription [FIELD] in model [USER]
STEP: 1 py manage.py makemigrations account
STEP: 2 py manage.py migrate
Then do next ...

"""


class User(AbstractUser):
    TYPES_OF_USERS = (
        ("CUSTOMER", 'Customer'),
        ("MANAGER", 'Manager'),
        ("POSTMAN", 'Postman')
    )
    profile_image = ResizedImageField(
        upload_to='account/images/profiles/', null=True, blank=True, size=[100, 100], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    cnic = models.CharField(max_length=13, null=True, blank=True, help_text="13 digits cnic without -")
    address = models.TextField(max_length=30, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    type = models.CharField(max_length=20, default='CUSTOMER', choices=TYPES_OF_USERS)
    is_customer = models.BooleanField(default=True)
    is_postman = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)
