# Generated by Django 5.0.6 on 2024-07-03 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song_cover_image_song_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
