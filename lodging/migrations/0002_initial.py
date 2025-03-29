# Generated by Django 5.1.6 on 2025-03-29 20:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lodging', '0001_initial'),
        ('trips', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lodging',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.trip'),
        ),
        migrations.AddField(
            model_name='lodging',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
