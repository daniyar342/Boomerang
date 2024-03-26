from config.celery import app
from django.core.mail import send_mail
from datetime import datetime


@app.task
def send_recall_to_owner(email_or_phone,text,client_name,product_name):

    subject = f"Отзыв"
    message = f"Добрый день\nу вас есть новый отзыв от клиента {client_name}\nна продукт {product_name}\n{text} {datetime.utcnow()}"
    sender_email = "tolomushev33@gmail.com"
    recipient_email = email_or_phone

    send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)