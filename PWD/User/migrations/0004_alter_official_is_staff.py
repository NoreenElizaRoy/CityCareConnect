# Generated by Django 5.0.2 on 2024-03-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_rename_id_customuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='official',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
