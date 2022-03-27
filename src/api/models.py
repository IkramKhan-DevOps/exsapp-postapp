import uuid

from django.db import models
from django_resized import ResizedImageField
from src.accounts.models import User


class Parcel(models.Model):
    STATUS_CHOICES = (
        ('cus', 'Customer'),
        ('ssm', 'Source Service Manager'),
        ('dsm', 'Destination Service Manager'),
        ('pos', 'Postman'),
    )
    SERVICE_TYPES_CHOICES = (
        ('urgent', 'urgent'),
        ('normal', 'normal'),
    )
    qr_image = ResizedImageField(
        upload_to='account/images/qrs/', null=True, blank=True, quality=75,
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    tracking_id = models.CharField(max_length=100, blank=True, unique=True, default=(str(uuid.uuid4())[:8]))
    postal_charges = models.PositiveIntegerField(default=5)
    service_type = models.CharField(max_length=255, choices=SERVICE_TYPES_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    dispatchLocation = models.CharField(max_length=1000)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sent_by', null=True,
                                 blank=True)
    source_service_manager = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='source_manager',
                                               null=True, blank=True)
    destination_service_manager = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                                                    related_name='destination_manager', null=True, blank=True)
    receiver = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='receiver', null=True,
                                 blank=True)
    postman = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='postman', null=True,
                                blank=True)
    details = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=3, default='ssm')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tracking_id


class PostOffice(models.Model):
    office_address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)
