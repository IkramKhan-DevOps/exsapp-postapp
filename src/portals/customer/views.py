import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView
from django import forms
from django.contrib import messages

from core.settings import BASE_DIR
from src.api.models import Parcel

from src.accounts.decorators import customer_required
from src.api.models import Parcel

User = get_user_model()

customer_decorators = [login_required, customer_required]
customer_nocache_decorators = [login_required, customer_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(customer_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'customer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(customer_decorators, name='dispatch')
class UserListView(ListView):
    queryset = User.objects.all()
    template_name = 'customer/user_list.html'


@method_decorator(customer_decorators, name='dispatch')
class ParcelListView(ListView):
    queryset = Parcel.objects.all()
    template_name = 'customer/parcel_list.html'

    def get_queryset(self):
        return Parcel.objects.filter(sender=self.request.user)


class ParcelForm(forms.ModelForm):
    sender = forms.CharField()
    receiver = forms.CharField()

    class Meta:
        model = Parcel
        fields = [
            'postal_charges', 'service_type', 'dispatchLocation', 'details'
        ]


@method_decorator(customer_decorators, name='dispatch')
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
        return render(request, 'customer/search_id.html', context=context)


def get_qr_image(string):
    data = string
    img = qrcode.make(data)
    img.save(f'{BASE_DIR}\\media\\{string}-QR.png')
    return f'{string}-QR.png'


@method_decorator(customer_decorators, name='dispatch')
class TestView(View):

    def get(self, request):
        context = {
            'form': ParcelForm()
        }
        print('SEARCH PARCEL TABLE')
        return render(request, 'customer/test.html', context=context)

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
        return render(request, 'customer/test.html', {'form': form})


@method_decorator(customer_decorators, name='dispatch')
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
