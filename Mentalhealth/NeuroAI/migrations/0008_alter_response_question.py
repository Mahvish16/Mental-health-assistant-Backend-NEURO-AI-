# Generated by Django 5.1.4 on 2025-01-15 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuroAI', '0007_disorder_remove_questions_condition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='NeuroAI.questions'),
        ),
    ]
