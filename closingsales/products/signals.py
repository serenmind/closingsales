from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.mail import send_mail
from .models import Advertisement


@receiver(post_save, sender=Advertisement)
def advertisement_created(sender, instance, created, **kwargs):
    if created:
        subject = 'New Advertisement added to the system'
        message = "Plase review the newly added advertisement"
        customer_email = instance.user.email
        send_mail(subject, message, customer_email, ['contact@closingshops.de'])

