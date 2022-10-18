# Generated by Django 2.2.4 on 2020-02-05 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_materia_semestre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='lapso_academico',
            field=models.CharField(default=2017, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carrera',
            name='institucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Institucion'),
        ),
    ]
