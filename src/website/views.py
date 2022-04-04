from django.views.generic import TemplateView

from src.api.models import Parcel


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            parcel = Parcel.objects.filter(tracking_id=search)
            if parcel:
                context['parcel'] = parcel.first()
        return context
