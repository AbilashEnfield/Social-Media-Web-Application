# Generated by Django 3.2 on 2021-06-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Actions', '0011_explorevideos_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatcontent',
            name='msg_type',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='chatcontent',
            name='upload_file',
            field=models.FileField(default='', null=True, upload_to='files'),
        ),
    ]
