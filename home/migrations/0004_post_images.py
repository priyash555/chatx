# Generated by Django 2.2.3 on 2019-08-08 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ImageField(blank=True, upload_to='postimages'),
        ),
    ]
