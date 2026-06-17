# Generated manually for SQLite

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- 1. Tabel siswa
                CREATE TABLE IF NOT EXISTS siswa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    kelas TEXT NOT NULL,
                    nis TEXT NOT NULL UNIQUE,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    status TEXT
                );

                -- 2. Tabel buku dengan CHECK ala SQLite
                CREATE TABLE IF NOT EXISTS buku (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul TEXT NOT NULL,
                    pengarang TEXT NOT NULL,
                    kategori TEXT NOT NULL CHECK (kategori IN ('Novel', 'Sejarah', 'Pendidikan')),
                    penerbit TEXT,
                    tahun_terbit INTEGER,
                    rak TEXT NOT NULL CHECK (rak IN ('Rak A-01', 'Rak A-02', 'Rak A-03', 'Rak A-04', 'Rak A-05')),
                    stok INTEGER NOT NULL DEFAULT 0,
                    deskripsi TEXT
                );

                -- 3. Tabel peminjaman dengan FOREIGN KEY ala SQLite
                CREATE TABLE IF NOT EXISTS peminjaman (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    siswa_id INTEGER NOT NULL,
                    buku_id INTEGER NOT NULL,
                    tanggal_pinjam DATE NOT NULL DEFAULT CURRENT_DATE,
                    jatuh_tempo DATE NOT NULL,
                    keperluan TEXT,
                    status TEXT NOT NULL DEFAULT 'Dipinjam' CHECK (status IN ('Dipinjam', 'Dikembalikan', 'Terlambat')),
                    nama_peminjam TEXT,
                    petugas TEXT,
                    catatan TEXT,
                    FOREIGN KEY (siswa_id) REFERENCES siswa(id) ON DELETE CASCADE,
                    FOREIGN KEY (buku_id) REFERENCES buku(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_peminjaman_siswa_id ON peminjaman (siswa_id);
                CREATE INDEX IF NOT EXISTS idx_peminjaman_buku_id ON peminjaman (buku_id);
                CREATE INDEX IF NOT EXISTS idx_peminjaman_status ON peminjaman (status);
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS peminjaman;
                DROP TABLE IF EXISTS buku;
                DROP TABLE IF EXISTS siswa;
            """,
        ),
    ]