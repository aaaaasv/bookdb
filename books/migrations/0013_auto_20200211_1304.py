# Generated by Django 3.0.2 on 2020-02-11 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_auto_20200211_1206'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set(),
        ),
    ]
