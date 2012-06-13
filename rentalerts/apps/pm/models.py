from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from rentalerts.apps.apartments.models import Apartment

class MessageManager(models.Manager):

    def parents(self):
        return self.filter(parent__isnull=True)

    def get_query_set(self):
        return super(MessageManager, self).get_query_set().select_related(
            'sender',
            'receiver',
            'apartment',
            'apartment__area',
            'apartment__area__city',
            'parent',
        )


class Message(models.Model):

    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
    apartment = models.ForeignKey(Apartment, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='replies',
    )


    created_on = models.DateTimeField(auto_now_add=True)

    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    objects = MessageManager()

    class Meta:
        ordering = ('-created_on',)

    def __unicode__(self):
        return unicode(self.sender)

    def is_parent(self):
        return self.parent is None

    @permalink
    def get_reply_url(self):
        return ('pm:reply', [str(self.id)])

    @permalink
    def get_absolute_url(self):
        return ('pm:detail', [str(self.id)])
