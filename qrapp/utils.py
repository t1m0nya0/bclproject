import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailSendingError(Exception):
    pass


def send_email(receiver_email, subject, message, qr_code_path):
    sender_email = "tamirlan@1fit.app"
    sender_password = "erpnylkjkuzqqfoh"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Добавление текстового сообщения
    msg.attach(MIMEText(message, 'plain'))

    # Добавление QR-кода как вложения
    qr_image = open(qr_code_path, 'rb').read()
    image = MIMEImage(qr_image, name="qr_code.png")
    msg.attach(image)

    # Установка соединения с SMTP-сервером и отправка письма
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        raise EmailSendingError("Email could not be sent. Error: " + str(e))
