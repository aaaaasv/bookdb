# Generated by Django 3.0.2 on 2020-01-12 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20200111_1901'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-rating']},
        ),
        migrations.AddField(
            model_name='book',
            name='rating_sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='rating_voters_number',
            field=models.IntegerField(default=0),
        ),
    ]
