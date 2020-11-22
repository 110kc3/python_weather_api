# Generated by Django 3.1.3 on 2020-11-22 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pollution', '0002_auto_20201122_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cities', to='auth.user'),
        ),
    ]
