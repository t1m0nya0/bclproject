from django.urls import path
from .views import TicketListCreateView, TicketCheckView

urlpatterns = [
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/check/', TicketCheckView.as_view(), name='ticket-check'),
]
