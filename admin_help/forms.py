from django import forms
from django_ace import AceWidget


class AdminHelpAdminForm(forms.ModelForm):
    help = forms.CharField(widget=AceWidget(mode='markdown', width='80%', height='500px;', showprintmargin=False), required=False)