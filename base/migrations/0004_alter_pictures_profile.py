# Generated by Django 4.2.5 on 2023-09-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_users_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictures',
            name='profile',
            field=models.BooleanField(default=False),
        ),
    ]
