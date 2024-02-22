from typing import ClassVar

from django import forms

from . import models


class OutputForm(forms.ModelForm):
    class Meta:
        model = models.ICSOutput
        fields: ClassVar = ["name", "inputs", "filter"]

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["inputs"].queryset = models.ICSInput.objects.filter(user=user)
