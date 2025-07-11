# Generated by Django 5.2.1 on 2025-06-08 17:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cameras', '0001_initial'),
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_format', models.CharField(max_length=10)),
                ('image_aspect', models.CharField(blank=True, max_length=10)),
                ('format_name', models.CharField(blank=True, max_length=100)),
                ('sensor_width', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('sensor_height', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('image_width', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('image_height', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('is_anamorphic', models.BooleanField(default=False, help_text='Is this format anamorphic?')),
                ('anamorphic_squeeze', models.DecimalField(decimal_places=2, default=1.0, help_text='Lens anamorphic factor (2.0 is the most common but can me 1.8, 1.33, etc)', max_digits=4)),
                ('is_desqueezed', models.BooleanField(default=False, help_text='Has this footage already beed desqueezed in-camera?')),
                ('pixel_aspect', models.DecimalField(decimal_places=2, default=1.0, help_text='Pixel aspect', max_digits=4)),
                ('filmback_width_3de', models.DecimalField(blank=True, decimal_places=3, help_text='3DE filmback width in mm', max_digits=6, null=True)),
                ('filmback_height_3de', models.DecimalField(blank=True, decimal_places=3, help_text='3DE filmback height in mm', max_digits=6, null=True)),
                ('distortion_model_3de', models.CharField(blank=True, help_text='Recommended 3DE distortion for this format', max_length=50, null=True)),
                ('is_downsampled', models.BooleanField(default=False)),
                ('is_upscaled', models.BooleanField(default=False)),
                ('codec', models.CharField(blank=True, max_length=20)),
                ('raw_recording_available', models.BooleanField(default=True, help_text='Is the raw, unprocessed format available for recording?')),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('make_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('tracking_workflow', models.TextField(blank=True, help_text='Step-by-step instructions for setting up this format in tracking software', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formats', to='cameras.camera')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='formats', to='sources.source')),
            ],
            options={
                'unique_together': {('camera', 'image_format', 'image_aspect', 'format_name', 'is_anamorphic', 'codec', 'is_downsampled', 'pixel_aspect')},
            },
        ),
    ]
