# Generated by Django 2.0.2 on 2018-05-30 21:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20180528_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='category',
            field=models.CharField(default='Any Category', max_length=200),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='difficulty',
            field=models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')], default='Easy', max_length=100),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2018, 6, 1, 9, 6, 18, 208078)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2018, 5, 31, 9, 6, 18, 208078)),
        ),
    ]
