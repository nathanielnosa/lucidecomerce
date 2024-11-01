from django.core.mail import send_mail
from django.conf import settings

def send_welcome_message(user_email,user_name):
    subject = "Welcome to Lucid Ecommerce"
    message = f'Hello, {user_name}.\n\n Thanks for joining our community'
    from_email = settings.EMAIL_HOST_USER
    receiver = [user_email]
    send_mail(
    subject,
    message,
    from_email,
    receiver,
    fail_silently=False,
)