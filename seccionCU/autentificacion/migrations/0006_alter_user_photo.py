# Generated by Django 4.1.4 on 2023-03-17 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autentificacion', '0005_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='autentificacion/gato.jpg', null=True, upload_to='autentificacion'),
        ),
    ]
