# Generated by Django 4.2.5 on 2023-10-14 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siapdpv', '0006_tramite_conclusion_queja_tramite_nivel_solucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramite',
            name='tiene_respuesta',
            field=models.BooleanField(default=False),
        ),
    ]