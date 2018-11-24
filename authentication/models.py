from django.db import models
import uuid
import datetime


class UserModel(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=4096)
    dateOfBirth = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.dateOfBirth.year - (
                    (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day))


class UserSessionToken(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def create_token(self):
        self.session_token = uuid.uuid4()
