# Generated by Django 3.2 on 2022-09-20 07:39

import api.v1.users.services
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('flf', models.CharField(max_length=150, verbose_name='Name')),
                ('role', models.CharField(choices=[('student', 'student'), ('sponsor', 'sponsor'), ('admin', 'admin')], max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('man', 'man'), ('woman', 'woman')], default='man', max_length=5)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=api.v1.users.services.upload_location_avatar, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']), api.v1.users.services.validate_size_image])),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
