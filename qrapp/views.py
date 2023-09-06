from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Ticket
from .serializers import TicketSerializer
import qrcode
from io import BytesIO
from django.core.files import File
from rest_framework.response import Response

from .utils import send_email


class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        mail = self.request.data.get('mail', '')  # Извлечение адреса электронной почты из запроса
        ticket = serializer.save(mail=mail)  # Сохранение билета с указанным адресом электронной почты

        # Генерация QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://127.0.0.1:8000/tickets/{ticket.id}/check/")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Сохранение QR-кода как изображения
        buffer = BytesIO()
        img.save(buffer)
        ticket.qr_code.save(f'qr_code_{ticket.id}.png', File(buffer), save=True)

        receiver_email = mail  # Адрес получателя, указанный в запросе
        subject = "Ваш билет с QR-кодом"
        message = "Спасибо за покупку билета. Вот ваш QR-код для мероприятия."

        qr_code_path = ticket.qr_code.path  # Путь к QR-коду
        send_email(receiver_email, subject, message, qr_code_path)


class TicketCheckView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, pk):
        ticket = self.get_object()

        # Проверка, что билет оплачен
        if not ticket.purchase_status:
            return Response({"status": "invalid", "message": "Билет не оплачен"})

        # Проверка num_of_visits
        if ticket.num_of_visits > 0:
            return Response({"status": "invalid", "message": "Билет уже использован"})

        # Увеличение счетчика посещений
        ticket.num_of_visits += 1
        ticket.save()

        return Response({"status": "valid", "message": "Билет действителен"})
