# Generated by Django 4.1.3 on 2024-05-31 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_membership_membershipclaim'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('None', 'None'), ('GS', 'General Secretary'), ('President', 'President')], default='None', max_length=25),
        ),
    ]