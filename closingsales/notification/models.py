from django.db import models

from account.models import User


class NotificationManager(models.Manager):

	def unseen(self, user):
		return super().get_queryset().filter(seen=False).filter(user=user)


class Notification(models.Model):
	APPROVED = 'APPROVED'
	REJECTED = 'REJECTED'
	CREATED  = 'CREATED'

	OPTIONS = (
		(APPROVED, 'APPROVED'),
		(REJECTED, 'REJECTED'),
		(CREATED, 'CREATED')
		)
	user 				= models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	notifcation_type 	= models.CharField(max_length=10, choices=OPTIONS, default=CREATED)
	message 			= models.CharField(max_length=254)
	seen 				= models.BooleanField(default=False)
	date_created 		= models.DateTimeField(auto_now_add=True)
	date_updated 		= models.DateTimeField(auto_now=True)

	notifications 		= NotificationManager()

	def __str__(self):
		return self.message

