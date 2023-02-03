from django.core.mail import send_mail
from django.conf import settings


class Email:

    def __init__(self,to,subject='',message='') -> None:
        self.to=to
        self.subject=subject
        self.message=message

    def send(self):
        return send_mail(recipient_list=self.to,subject=self.subject,message=self.message,from_email=settings.EMAIL_HOST_USER)
