# Generated by Django 3.1.1 on 2021-03-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_auto_20210321_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(null=True, to='books.Genre'),
        ),
    ]