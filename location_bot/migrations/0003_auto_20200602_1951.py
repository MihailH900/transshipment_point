# Generated by Django 3.0.6 on 2020-06-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_bot', '0002_delete_vk_getter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vk_sender',
            name='location',
        ),
        migrations.AddField(
            model_name='vk_sender',
            name='meet_location_x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vk_sender',
            name='meet_location_y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
