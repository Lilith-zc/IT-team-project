# Generated by Django 2.1.5 on 2021-08-04 10:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_auto_20210804_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 18, 27, 27, 997879)),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 18, 27, 27, 997879)),
        ),
    ]
