from django.contrib.auth.models import User
from django.db import models
from django.forms import forms


# Create your models here.

class TimespamtedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # permet de dire à chaque fois qu'il y'a modif
    updated_at = models.DateTimeField(auto_now=True)  # permet de modifier apres création

    class Meta:
        abstract = True


class Book(TimespamtedModel):
     title = models.CharField(max_length=100)
     author = models.CharField(max_length=42)
     contain = models.TextField(null=True)
     # categorie = models.ForeignKey('Categorie')
     thumb = models.ImageField(upload_to='profile_pics', blank=True, default="default.png")
     pdf = models.FileField(upload_to='pdf/', null=True, blank=True)

     def __str__(self):
          return self.title


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    birth_date = models.DateField()

    def __str__(self):
      return self.user.username
