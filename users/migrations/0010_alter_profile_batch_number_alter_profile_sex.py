# Generated by Django 4.1.3 on 2023-04-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_phone_number_profile_registration_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='batch_number',
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
            preserve_default=False,
        ),
    ]