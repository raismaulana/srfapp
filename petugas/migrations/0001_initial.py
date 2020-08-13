# Generated by Django 3.0.8 on 2020-08-11 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediksi',
            fields=[
                ('idprediksi', models.AutoField(primary_key=True, serialize=False)),
                ('prediksiradiasi', models.DecimalField(blank=True, decimal_places=2, max_digits=65, null=True)),
                ('prediksitanggal', models.DateField(unique=True)),
            ],
            options={
                'db_table': 'prediksi',
            },
        ),
        migrations.CreateModel(
            name='Radiasi',
            fields=[
                ('idradiasi', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal', models.DateField(unique=True)),
                ('radiasi', models.DecimalField(blank=True, decimal_places=2, max_digits=65, null=True)),
            ],
            options={
                'db_table': 'radiasi',
            },
        ),
    ]