# Generated by Django 4.1.4 on 2023-02-25 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autentificacion', '0002_alter_user_address_alter_user_birthdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
