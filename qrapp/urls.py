from django.urls import path
from .views import create_ticket, generate_qr_code, TicketCheckView


urlpatterns = [
    path('create/', create_ticket, name='create-ticket'),
    path('generate_qr_code/<int:ticket_id>/', generate_qr_code, name='generate-qr-code'),
    path('tickets/<int:pk>/check/', TicketCheckView.as_view(), name='ticket-check'),
]
