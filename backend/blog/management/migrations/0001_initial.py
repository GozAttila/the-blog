# Generated by Django 5.1.1 on 2024-10-17 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('name_change', 'Name Change'), ('email_change', 'Email Change')], max_length=20)),
                ('requested_name', models.CharField(blank=True, max_length=150, null=True)),
                ('requested_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('reason', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('changelog', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('handled_at', models.DateTimeField(blank=True, null=True)),
                ('handled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
