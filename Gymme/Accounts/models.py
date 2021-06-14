from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(verbose_name="phone number", unique=True)
    about = models.TextField(blank=True, null=True)
    homeState = models.CharField(max_length=120, blank=True, null=True)
    homeCountry = models.CharField(max_length=120, blank=True, null=True)
    workState = models.CharField(max_length=120, blank=True, null=True)
    workCountry = models.CharField(max_length=120, blank=True, null=True)
    work = models.CharField(max_length=120, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    coverPic = models.ImageField(upload_to='images/', null=True, blank=True)

    @property
    def userimage(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def coverImg(self):
        try:
            url = self.coverPic.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    trainer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(verbose_name="phone number", unique=True)
    about = models.TextField(blank=True, null=True)
    homeState = models.CharField(max_length=120, blank=True, null=True)
    homeCountry = models.CharField(max_length=120, blank=True, null=True)
    workState = models.CharField(max_length=120, blank=True, null=True)
    workCountry = models.CharField(max_length=120, blank=True, null=True)
    work = models.CharField(max_length=120, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    coverPic = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def userimage(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def coverImg(self):
        try:
            url = self.coverPic.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.trainer.username



