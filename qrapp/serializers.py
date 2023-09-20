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
            "university",
            "purchase_status",
            "price",
        )
