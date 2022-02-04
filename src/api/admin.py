from django.contrib import admin
from django.utils.html import format_html

from src.api.models import Parcel, PostOffice

admin.site.register(Parcel)
admin.site.register(PostOffice)

