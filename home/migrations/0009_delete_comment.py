# Generated by Django 3.0.3 on 2020-04-12 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_group_groupmessage_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
