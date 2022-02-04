from django.forms import ModelForm
from src.application.models import Team


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'participants', 'is_active']
