# Generated by Django 3.0.2 on 2020-01-10 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_picture',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
