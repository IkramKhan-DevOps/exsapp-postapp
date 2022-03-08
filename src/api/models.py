import uuid

from django.db import models
from django_resized import ResizedImageField

from src.accounts.models import User


class Parcel(models.Model):
    SERVICE_TYPES_CHOICES = (
        ('urgent', 'urgent'),
        ('normal', 'normal'),
    )
    qr_image = ResizedImageField(
        upload_to='account/images/qrs/', null=True, blank=True, quality=75,
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    tracking_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    postal_charges = models.PositiveIntegerField(default=5)
    service_type = models.CharField(max_length=255, choices=SERVICE_TYPES_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    dispatchLocation = models.CharField(max_length=1000)
    postman = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='postman', null=True, blank=True)
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='receiver')
    details = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tracking_id


class PostOffice(models.Model):
    service_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    office_address = models.TextField()
    parcels = models.ManyToManyField(Parcel)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)
