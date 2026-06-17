from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=150)
    pengarang = models.CharField(max_length=100) # Perbaikan typo 'penagrang'
    kategori = models.CharField(max_length=50)   # Perbaikan typo 'katagori'
    penerbit = models.CharField(max_length=100)
    tahun = models.IntegerField()
    isbn = models.CharField(max_length=50)
    rak = models.CharField(max_length=50)
    stok = models.IntegerField()                 # Perbaikan: hapus max_length=0
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.judul

# Tambahkan Model Peminjaman di bawah ini
class Peminjaman(models.Model):
    nama = models.CharField(max_length=100)      # Kolom p.nama yang dicari oleh SQL kamu
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tgl_pinjam = models.DateField()
    tgl_kembali = models.DateField()
    status = models.CharField(max_length=20, default='Dipinjam')

    def __str__(self):
        return f"{self.nama} meminjam {self.buku.judul}"