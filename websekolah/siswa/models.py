from django.db import models

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    umur = models.IntegerField()
    tgl_lahir = models.DateField()
    nilai_akhir = models.IntegerField(default=0)

    def __str__(self):
        return self.nama