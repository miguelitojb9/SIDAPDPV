# Generated by Django 4.2.5 on 2023-10-09 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200)),
                ('municipio', models.CharField(max_length=100)),
                ('procesado', models.BooleanField(default=False)),
                ('enTramite', models.BooleanField(default=False)),
                ('departamento_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demandas', to='customUser.departamento')),
                ('recurrente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_tramite', models.CharField(choices=[('queja', 'Queja'), ('demanda', 'Demanda'), ('solicitud', 'Solicitud')], max_length=10)),
                ('aprobado', models.BooleanField(default=False)),
                ('departamento_asignado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customUser.departamento')),
                ('usuario_responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200)),
                ('municipio', models.CharField(max_length=100)),
                ('procesado', models.BooleanField(default=False)),
                ('enTramite', models.BooleanField(default=False)),
                ('departamento_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes', to='customUser.departamento')),
                ('recurrente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Queja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200)),
                ('municipio', models.CharField(choices=[('arroyo_naranjo', 'Arroyo Naranjo'), ('boyeros', 'Boyeros'), ('centro_habana', 'Centro Habana'), ('cerro', 'Cerro'), ('cotorro', 'Cotorro'), ('diez_de_octubre', 'Diez de Octubre'), ('guanabacoa', 'Guanabacoa'), ('habana_del_este', 'Habana del Este'), ('habana_vieja', 'Habana Vieja'), ('la_lisa', 'La Lisa'), ('mantilla', 'Mantilla'), ('marianao', 'Marianao'), ('playa', 'Playa'), ('plaza', 'Plaza de la Revolución'), ('regla', 'Regla'), ('san_miguel_del_padron', 'San Miguel del Padrón')], max_length=100)),
                ('descripcion', models.TextField(blank=True, max_length=100, null=True)),
                ('procesado', models.BooleanField(default=False)),
                ('enTramite', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('departamento_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quejas', to='customUser.departamento')),
                ('organismo_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='solicitudes', to='customUser.organismo')),
                ('recurrente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('demanda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.demanda')),
                ('queja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.queja')),
                ('solicitud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.solicitud')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='documentos/')),
                ('demanda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.demanda')),
                ('queja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.queja')),
                ('solicitud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='siapdpv.solicitud')),
            ],
        ),
    ]
