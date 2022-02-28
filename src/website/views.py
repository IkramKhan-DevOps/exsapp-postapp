from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'website/home.html'
