# Generated by Django 5.1.4 on 2024-12-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuroAI', '0005_remove_registeruser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
