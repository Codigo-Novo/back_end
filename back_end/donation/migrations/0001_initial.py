# Generated by Django 5.1.3 on 2025-02-07 20:09

import django.db.models.deletion
import secrets
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=secrets.token_hex, max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('is_redeemed', models.BooleanField(default=False)),
                ('redeemed_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_donation_tokens', to=settings.AUTH_USER_MODEL)),
                ('redeemed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='redeemed_donation_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
