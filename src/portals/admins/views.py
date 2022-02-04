from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView,
    ListView, CreateView, UpdateView
)
from django.contrib.auth import get_user_model

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


class ParcelForm(forms.ModelForm):
    sender = forms.CharField()
    receiver = forms.CharField()

    class Meta:
        model = Parcel
        fields = [
            'postal_charges', 'service_type', 'dispatchLocation', 'details'
        ]


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
            form.save()
            messages.success(request, "Request added successfully.")
            return redirect('admins:add-parcel')
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