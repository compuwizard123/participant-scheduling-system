from django import forms

from pss.main.models import Experiment

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment