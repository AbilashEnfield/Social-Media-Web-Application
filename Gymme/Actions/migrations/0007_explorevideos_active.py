# Generated by Django 3.2 on 2021-05-15 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Actions', '0006_alter_explorevideos_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='explorevideos',
            name='Active',
            field=models.BooleanField(default=True),
        ),
    ]
