# Generated by Django 4.0.4 on 2022-04-19 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0002_remove_show_album_name_remove_show_artist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='new_field',
            field=models.BooleanField(default=True),
        ),
    ]
