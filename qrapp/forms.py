from django import forms

from qrapp.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("first_name", "last_name", "phone_number", "student_id", "university", "purchase_status", "dorm_stud")
