from .models import Recruit
import django.forms as forms
from .models import Event


# create a ModelForm
class CandidateCheckinForm(forms.Form):
    # specify the name of model to use

    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=50)
    desired_position = forms.ChoiceField(choices=())

    def __init__(self, event: Event, data, files):
        super().__init__(data=data, files=files)
        self.fields['desired_position'].choices = [(choice.pk, choice.name) for choice in event.positions.all()]

