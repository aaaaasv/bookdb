# Generated by Django 3.0.2 on 2020-02-11 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name']},
        ),
    ]