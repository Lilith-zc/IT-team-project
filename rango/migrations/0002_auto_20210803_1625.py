# Generated by Django 2.2.5 on 2021-08-03 08:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='rango.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 3, 16, 25, 51, 840462)),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 3, 16, 25, 51, 841462)),
        ),
    ]
