from django.db import models

class Prediksi(models.Model):
    idprediksi = models.AutoField(primary_key=True)
    prediksiradiasi = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    prediksitanggal = models.DateField(unique=True)

    class Meta:
        db_table = 'prediksi'


class Radiasi(models.Model):
    idradiasi = models.AutoField(primary_key=True)
    tanggal = models.DateField(unique=True)
    radiasi = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'radiasi'