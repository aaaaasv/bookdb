# Generated by Django 3.1.1 on 2021-03-21 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20210320_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating_sum',
        ),
        migrations.RemoveField(
            model_name='book',
            name='rating_voters_number',
        ),
    ]