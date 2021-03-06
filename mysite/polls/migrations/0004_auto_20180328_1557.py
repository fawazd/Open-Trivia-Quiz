# Generated by Django 2.0.3 on 2018-03-28 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20180328_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogbreed',
            name='coat_length',
            field=models.CharField(choices=[('S', 'Short'), ('M', 'Medium'), ('L', 'Long')], default='MED', max_length=6),
        ),
        migrations.AlterField(
            model_name='dogbreed',
            name='drools',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='MED', max_length=6),
        ),
        migrations.AlterField(
            model_name='dogbreed',
            name='good_with_children',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='MED', max_length=6),
        ),
    ]
