# Generated by Django 2.2.4 on 2020-02-05 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200205_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='institucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Institucion'),
        ),
    ]