# Generated by Django 4.1.4 on 2023-04-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0006_alter_publicaciones_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntuacion',
            name='valoracion',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]