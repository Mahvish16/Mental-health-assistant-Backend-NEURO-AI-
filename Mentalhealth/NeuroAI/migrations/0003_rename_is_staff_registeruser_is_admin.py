# Generated by Django 5.1.4 on 2024-12-26 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NeuroAI', '0002_registeruser_groups_registeruser_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registeruser',
            old_name='is_staff',
            new_name='is_admin',
        ),
    ]