# Generated by Django 2.1.5 on 2021-08-04 13:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0009_auto_20210804_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 21, 3, 24, 237569)),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 21, 3, 24, 237569)),
        ),
    ]