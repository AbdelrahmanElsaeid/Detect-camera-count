# Generated by Django 5.0.6 on 2024-07-07 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_alter_video_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camerastatus',
            name='title',
        ),
    ]