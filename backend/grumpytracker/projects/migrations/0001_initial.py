# Generated by Django 5.2.1 on 2025-07-01 23:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cameras', '0003_camera_sensor_size'),
        ('formats', '0002_format_format_search'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True)),
                ('project_type', models.CharField(choices=[('feature', 'Feature'), ('episodic', 'Episodic')], default='feature', max_length=10)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('poster_path', models.CharField(blank=True, max_length=200)),
                ('release_date', models.DateField(blank=True)),
                ('adult', models.BooleanField(default=False)),
                ('tmdb_id', models.IntegerField(blank=True, null=True)),
                ('tmdb_original_name', models.CharField(blank=True, max_length=100)),
                ('genres', models.JSONField(blank=True, default=list)),
                ('rating', models.JSONField(blank=True, default=list)),
                ('cameras', models.ManyToManyField(blank=True, related_name='used_in_projects', to='cameras.camera')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFormat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('fmt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formats.format')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'unique_together': {('project', 'fmt')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='formats',
            field=models.ManyToManyField(blank=True, related_name='used_in_projects', through='projects.ProjectFormat', to='formats.format'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('up', 'upVote'), ('down', 'downVote')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fmt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formats.format')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('project', 'fmt', 'user')},
            },
        ),
    ]
