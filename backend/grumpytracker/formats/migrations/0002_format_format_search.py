# Generated by Django 5.2.1 on 2025-06-29 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='format',
            name='format_search',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
