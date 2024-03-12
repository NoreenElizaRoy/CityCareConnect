# Generated by Django 5.0.2 on 2024-03-05 07:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('complaint_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('complaint_details', models.TextField(blank=True, max_length=500, null=True)),
                ('complaint_location', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pendinig'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')], default='Pending', max_length=100)),
                ('filled_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]