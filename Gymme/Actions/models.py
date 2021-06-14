from django.db import models
from django.contrib.auth.models import User
from Accounts.models import Trainer, People
from django import template
# from encrypted_model_fields.fields import EncryptedTextField
# from fernet_fields import EncryptedTextField


# Create your models here.
class ExploreVideos(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    discription = models.TextField(blank=True, null=True)
    thumb = models.ImageField(upload_to='images/', null=True, verbose_name='')
    video = models.FileField(upload_to='videos/', null=True, verbose_name='')
    likeCount = models.BigIntegerField(blank=True, null=True)
    CommentCount = models.BigIntegerField(blank=True, null=True)
    shareCount = models.BigIntegerField(blank=True, null=True)
    Active = models.BooleanField(default=True)

    @property
    def feedsvideos(self):
        try:
            url = self.video.url
        except:
            url = ''
        return url

    @property
    def tumbimg(self):
        try:
            url = self.thumb.url
        except:
            url = ''
        return url

    register = template.Library()

    @register.filter
    def shrink_num_likeCount(self):
        """
        Shrinks number rounding
        123456  > 123,5K
        123579  > 123,6K
        1234567 > 1,2M
        """
        value = str(self.likeCount)

        if value.isdigit():
            value_int = int(value)

            if value_int >= 1000000:
                value = "%.0f%s" % (value_int / 1000000.00, 'M')
            else:
                if value_int >= 1000:
                    value = "%.0f%s" % (value_int / 1000.0, 'k')
        return value

    @register.filter
    def shrink_num_CommentCount(self):
        """
        Shrinks number rounding
        123456  > 123,5K
        123579  > 123,6K
        1234567 > 1,2M
        """
        value = str(self.CommentCount)

        if value.isdigit():
            value_int = int(value)

            if value_int >= 1000000:
                value = "%.0f%s" % (value_int / 1000000.00, 'M')
            else:
                if value_int >= 1000:
                    value = "%.0f%s" % (value_int / 1000.0, 'k')
        return value

    @register.filter
    def shrink_num_shareCount(self):
        """
        Shrinks number rounding
        123456  > 123,5K
        123579  > 123,6K
        1234567 > 1,2M
        """
        value = str(self.shareCount)

        if value.isdigit():
            value_int = int(value)

            if value_int >= 1000000:
                value = "%.0f%s" % (value_int / 1000000.00, 'M')
            else:
                if value_int >= 1000:
                    value = "%.0f%s" % (value_int / 1000.0, 'k')
        return value

    def __str__(self):
        return self.title


class chatroom(models.Model):
    roomcode = models.TextField(blank=True, null=True)
    trainee = models.ForeignKey(People, on_delete=models.SET_NULL, blank=True, null=True)
    trainerChat = models.ForeignKey(Trainer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.roomcode


class chatContent(models.Model):
    chatRoom = models.ForeignKey(chatroom, on_delete=models.SET_NULL, blank=True, null=True)
    chatter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    chatContentText = models.TextField(blank=True, null=True)
    msg_type = models.CharField(max_length=15, null=True)
    upload_file = models.FileField(upload_to='files/', null=True, default='')

    @property
    def getfile(self):
        if self.msg_type == 'image' or self.msg_type == 'video' or self.msg_type == 'audio':
            url = self.upload_file.url
        else:
            url = ''
        return url

