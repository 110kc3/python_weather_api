# Generated by Django 3.1.3 on 2020-11-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollution', '0005_custom_station_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]