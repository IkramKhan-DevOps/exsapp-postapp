from io import StringIO

import qrcode as qrcode
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.forms import TextInput
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView)
from core.settings import LINUX

from core.settings import BASE_DIR
from src.api.models import Parcel, PostOffice

User = get_user_model()

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]

"""  INIT ------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(View):

    def get(self, request):
        return redirect('admins:parcel-search')


""" ------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'admins/user_list.html'


""" ------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class ParcelListView(ListView):
    queryset = Parcel.objects.all()
    template_name = 'admins/parcel_list.html'


class ParcelForm(forms.ModelForm):
    sender = forms.CharField(widget=TextInput(attrs={'type': 'number'}))
    receiver = forms.CharField(widget=TextInput(attrs={'type': 'number'}))
    postal_code = forms.CharField(widget=TextInput(attrs={'type': 'number'}))

    class Meta:
        model = Parcel
        fields = [
            'postal_charges', 'service_type', 'dispatchLocation', 'details'
        ]


@method_decorator(admin_decorators, name='dispatch')
class SearchIDView(View):

    def get(self, request):
        context = {}
        if request.GET.get('search'):
            search = request.GET.get('search')
            parcel = Parcel.objects.filter(tracking_id=search)
            if parcel:
                context['parcel'] = parcel.first()
            else:
                messages.error(request, "Requested tracking ID Doesn't available")
        return render(request, 'admins/search_id.html', context=context)


def get_qr_image(string):
    data = string
    img = qrcode.make(data)
    if not LINUX:
        img.save(f'{BASE_DIR}\\media\\{string}-QR.png')
    else:
        img.save(f'{BASE_DIR}/media/{string}-QR.png')
    return f'{string}-QR.png'


@method_decorator(admin_decorators, name='dispatch')
class TestView(View):

    def get(self, request):
        context = {
            'form': ParcelForm()
        }
        return render(request, 'admins/test.html', context=context)

    def post(self, request):
        form = ParcelForm(data=request.POST)
        if form.is_valid():
            form.instance.customer = User.objects.get(username=form.cleaned_data['sender'])
            form.instance.source_service_manager = request.user
            receiver = User.objects.get(username=form.cleaned_data['receiver'])
            form.instance.receiver = receiver
            users = User.objects.filter(
                postal_code=form.cleaned_data['postal_code']
            )
            if users:
                form.instance.destination_city = users[0]
            parcel = form.save()
            string = str(parcel.tracking_id)
            new_parcel = Parcel.objects.get(tracking_id=string)
            image = get_qr_image(string)
            new_parcel.qr_image = image
            x = User.objects.filter(postal_code=form.cleaned_data['postal_code'])
            new_parcel.destination_service_manager = x[0] if User.objects.get(postal_code=form.cleaned_data['postal_code']) else None
            new_parcel.save()
            send_email.send_email(new_parcel.customer, "Your Parcel is is on the Way thanks for using PakEPost")
            send_email.send_email(new_parcel.receiver, "Your Parcel is is on the Way thanks for using PakEPost")
            return redirect('admins:parcel')
        return render(request, 'admins/test.html', {'form': form})


@method_decorator(admin_decorators, name='dispatch')
class UserExistsJSON(View):

    def get(self, request, username):
        flag = False
        user = User.objects.filter(cnic=username, is_superuser=False)
        if user:
            flag = True

        response = {
            'flag': flag,
        }
        return JsonResponse(data=response, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class CityExistsJSON(View):

    def get(self, request, city):
        flag = False
        user = User.objects.filter(postal_code=city, is_superuser=True)
        if user:
            flag = True

        response = {
            'flag': flag,
        }
        return JsonResponse(data=response, safe=False)


from . import send_email


@method_decorator(admin_decorators, name='dispatch')
class AddUserView(View):

    def post(self, request):

        phone = request.POST.get('phone')
        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')

        if phone and name and cnic and address:
            if not email:
                email = f"{cnic}@gmail.com"

            try:
                user = User.objects.create_user(
                    username=cnic, cnic=cnic, email=email, address=address, password=f'default@password',
                    is_active=True, is_customer=True, first_name=name, city=city
                )
                send_email.send_email(user, 'Your account has been created with above information')
                messages.success(request, f"New user {user.first_name} created successfully")
            except IntegrityError:
                messages.error(request, "Username email and cnic must be unique")
        else:
            messages.error(request, "Please fill out all the fields to create new user")

        return redirect('admins:add-parcel')


@method_decorator(admin_decorators, name='dispatch')
class AddSuperUserView(View):

    def get(self, request):
        return render(request, template_name='admins/super_user_form.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')

        if email and name and city:
            try:
                user = User.objects.create_user(
                    username=email, email=email, password=f'default@password',
                    is_active=True, is_customer=False, first_name=name, is_superuser=True, city=city
                )
                user.save()
                send_email.send_email(user, 'Your account has been created with above information')
                messages.success(request, f"New admin user {user.first_name} created successfully")
                return redirect('admins:user')
            except IntegrityError:
                messages.error(request, "Username already exists")
        else:
            messages.error(request, "Please fill out all the fields to create new user")

        return redirect('admins:add-super-user')


@method_decorator(admin_decorators, name='dispatch')
class AddPostmanUserView(View):

    def get(self, request):
        return render(request, template_name='admins/add_postman.html')

    def post(self, request):
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        if phone and name and cnic and address:
            if not email:
                email = f"{cnic}@gmail.com"

            try:
                user = User.objects.create_user(
                    username=cnic, cnic=cnic, email=email, address=address, password='default@password',
                    phone_number=phone,
                    is_active=True, is_customer=False, first_name=name, is_postman=True, postal_code=postal_code
                )
                user.save()
                send_email.send_email(user, 'Your account has been created with above information')
                messages.success(request, f"New postman {user.first_name} created successfully")
                return redirect('admins:user')
            except IntegrityError:
                messages.error(request, "Username email and cnic must be unique")
        else:
            messages.error(request, "Please fill out all the fields to create new user")

        return redirect('admins:user')


@method_decorator(admin_decorators, name='dispatch')
class ReceivedParcel(View):

    def get(self, request, pk):
        parcel = None

        # PARCEL EXISTS
        try:
            parcel = Parcel.objects.get(pk=pk)
        except Parcel.DoesNotExist:
            messages.error(request, "Requested Parcel doesn't exists")
            return redirect('admins:parcel')

        if parcel.destination_service_manager == request.user:
            parcel.status = 'dsm'
            parcel.save()
            messages.success(request, "Parcel mark as received successfully")
        else:
            messages.error(request, "You are not registered Destination manager")

        return redirect('admins:parcel')
