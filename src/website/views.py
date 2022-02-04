from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'website/home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'website/policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'website/terms.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class Error404View(TemplateView):
    template_name = 'website/404.html'
