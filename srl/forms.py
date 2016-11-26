from django import forms


class SrlForm(forms.Form):
    url = forms.URLField(label='')
