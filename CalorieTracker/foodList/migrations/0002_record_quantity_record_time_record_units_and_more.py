# Generated by Django 4.0.4 on 2022-05-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='quantity',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='record',
            name='units',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='record',
            name='weight',
            field=models.FloatField(default=None),
        ),
    ]
