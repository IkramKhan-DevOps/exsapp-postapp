import uuid

from django.db import models
from django_resized import ResizedImageField

"""
DJANGO DATABASE MODELS
"""


class User(models.Model):
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    cnic = models.CharField(max_length=13, null=True, blank=True,
                            help_text="13 digits cnic without -")
    address = models.TextField(max_length=30, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.00, blank=True, null=True)
    office = models.ForeignKey('api.PostOffice', null=True, blank=True, on_delete=models.SET_NULL)
    is_customer = models.BooleanField(default=True)
    is_postman = models.BooleanField(default=False)
    city = models.CharField(max_length=30, null=True, blank=True, default="Default")
    postal_code = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


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
    tracking_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
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

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tracking_id


class PostOffice(models.Model):
    office_address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    service_manager = models.OneToOneField('User', on_delete=models.CASCADE, related_name='service_manager', null=False,
                                           blank=False)
    postal_code = models.IntegerField(max_length=255)
    city = models.CharField(max_length=255)
    incoming_parcels = models.ForeignKey('Parcel', on_delete=models.CASCADE, related_name='incoming_parcels',
                                         null=False,
                                         blank=False)
    out_going_parcels = models.ForeignKey('Parcel', on_delete=models.CASCADE, related_name='out_going_parcels',
                                          null=False,
                                          blank=False)
    postmen = models.ForeignKey('User', on_delete=models.CASCADE, related_name='postmen', null=True,
                                blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)
