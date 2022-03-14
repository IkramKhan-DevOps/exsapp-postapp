from io import StringIO

import qrcode as qrcode
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView,
    ListView
)
from core.settings import LINUX

from core.settings import BASE_DIR
from src.api.models import Parcel

User = get_user_model()

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]

"""  INIT ------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'admins/user_list.html'


@method_decorator(admin_decorators, name='dispatch')
class ParcelListView(ListView):
    queryset = Parcel.objects.all()
    template_name = 'admins/parcel_list.html'


class ParcelForm(forms.ModelForm):
    sender = forms.CharField()
    receiver = forms.CharField()

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
            form.instance.sender = User.objects.get(username=form.cleaned_data['sender'])
            form.instance.receiver = User.objects.get(username=form.cleaned_data['receiver'])
            parcel = form.save()
            string = str(parcel.tracking_id)
            new_parcel = Parcel.objects.get(tracking_id=string)
            image = get_qr_image(string)
            new_parcel.qr_image = image
            new_parcel.save()
            return redirect('admins:parcel')
        return render(request, 'admins/test.html', {'form': form})


@method_decorator(admin_decorators, name='dispatch')
class UserExistsJSON(View):

    def get(self, request, username):
        flag = False
        user = User.objects.filter(username=username)
        if user:
            flag = True

        response = {
            'flag': flag,
        }
        return JsonResponse(data=response, safe=False)


class AddUserView(View):

    def post(self, request):
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if phone and name and cnic and email and address:
            try:
                user = User.objects.create_user(
                    username=cnic, cnic=cnic, email=email, address=address, password=f'default@{phone}',
                    is_active=True, is_customer=True, first_name=name
                )
                messages.success(request, f"New user {user.first_name} created successfully")
            except IntegrityError:
                messages.error(request, "Username email and cnic must be unique")
        else:
            messages.error(request, "Please fill out all the fields to create new user")

        return redirect('admins:add-parcel')
