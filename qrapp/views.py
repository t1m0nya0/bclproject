from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import qrcode
from django.http import HttpResponse
from io import BytesIO

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from qrapp.forms import TicketForm
from qrapp.models import Ticket
from qrapp.serializers import TicketSerializer


@login_required
def generate_qr_code(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    # Создание QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"https://bclproject.up.railway.app/qrapp/tickets/{ticket.id}/check/")
    qr.make(fit=True)

    # Создание изображения QR-кода
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    # Возвращаем изображение в ответе
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            return redirect('generate-qr-code', ticket_id=ticket.id)
    else:
        form = TicketForm()

    return render(request, 'qrapp/create_ticket.html', {'form': form})


class TicketCheckView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk):
        ticket = self.get_object()
        # Проверка, что билет оплачен
        if not ticket.purchase_status:
            return Response({"message": "Билет не оплачен"})

        # Проверка num_of_visits
        if ticket.num_of_visits > 0:
            return Response({"message": "Билет уже использован"})

        # Увеличение счетчика посещений
        ticket.num_of_visits += 1
        ticket.save()
        ticket_data = model_to_dict(ticket)
        return Response({"message": "Билет действителен",
                         "ticket_info": ticket_data})
