# Generated by Django 3.1.1 on 2021-03-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_auto_20200211_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='cover_picture',
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='default.png', upload_to='book_covers'),
        ),
    ]
