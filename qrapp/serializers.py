from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=None)
    qr_code = serializers.CharField(source='qrcode')
    class Meta:
        model = Ticket
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "student_id",
            "university",
            "purchase_status",
            "qr_code",
            "num_of_visits",
            "dorm_stud",
            "owner",
        )
