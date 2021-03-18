# Generated by Django 3.0.5 on 2021-03-18 01:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='reg_date',
            field=models.DateField(default=datetime.datetime(2021, 3, 18, 1, 30, 12, 757852, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='stockitemlist',
            name='stock_item_code',
            field=models.CharField(max_length=200),
        ),
    ]