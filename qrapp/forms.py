from django import forms

from qrapp.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("name",)
