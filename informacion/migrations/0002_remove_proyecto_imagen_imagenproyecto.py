# Generated by Django 5.0.3 on 2024-09-17 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informacion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='imagen',
        ),
        migrations.CreateModel(
            name='ImagenProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='proyectos/')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='informacion.proyecto')),
            ],
        ),
    ]
