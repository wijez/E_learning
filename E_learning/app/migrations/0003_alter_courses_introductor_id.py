# Generated by Django 5.1.2 on 2024-10-22 07:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_enrollments_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='introductor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
