from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Q

from authentication.models import *

class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qs = self.get_queryset().filter(qlookup).distinct()
        return qs

    def get_or_new(self, user, other_user):  # get_or_create
        username = user.email_address
        if username == other_user:
            return None, False
        qlookup1 = Q(first__email_address=username) & Q(second__email_address=other_user)
        qlookup2 = Q(first__email_address=other_user) & Q(second__email_address=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()

        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            user2 = UserModel.objects.filter(email_address=other_user).first()
            if user2 == None:
                return None, False
            if user != user2:
                obj = self.model(
                        first=user,
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(UserModel, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
