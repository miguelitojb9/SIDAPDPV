# Generated by Django 4.2.5 on 2023-10-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0002_alter_user_municipality'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='noRad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
