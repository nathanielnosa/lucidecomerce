from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    age= models.IntegerField()
    profile_pix = models.ImageField(max_length=255)

    def __str__(self):
        return self.fullname