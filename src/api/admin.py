from django.contrib import admin
from django.utils.html import format_html

from src.api.models import Parcel, PostOffice


class ParcelView(admin.ModelAdmin):
    list_display = ['pk', 'created_on']


admin.site.register(Parcel, ParcelView)
admin.site.register(PostOffice)
