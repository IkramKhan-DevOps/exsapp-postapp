from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, ListView


class HomeView(View):

    def get(self, request):
        return redirect('account_login')