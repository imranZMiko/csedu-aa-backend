# Generated by Django 4.1.3 on 2024-01-04 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-created_at']},
        ),
    ]