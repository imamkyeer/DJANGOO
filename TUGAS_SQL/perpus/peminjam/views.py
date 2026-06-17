from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from datetime import date, timedelta

# ==========================
# HELPER
# ==========================

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(zip(columns, row))


# ==========================
# DASHBOARD
# ==========================

def dashboard_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM buku")
        total_judul = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(stok),0) FROM buku")
        total_buku = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM peminjaman
            WHERE status='Dipinjam'
        """)
        total_dipinjam = cursor.fetchone()[0]

    return render(
        request,
        "dashboard.html",
        {
            "total_judul": total_judul,
            "total_buku": total_buku,
            "total_dipinjam": total_dipinjam
        }
    )


# ==========================
# BUKU
# ==========================

def daftar_buku(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM buku
            ORDER BY id DESC
        """)
        buku_list = dictfetchall(cursor)

    return render(
        request,
        "daftar_buku.html",
        {
            "buku_list": buku_list
        }
    )


def detail_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM buku
            WHERE id=%s
        """, [id])
        buku = dictfetchone(cursor)

    return render(
        request,
        "detail_buku.html",
        {
            "buku": buku
        }
    )


def tambah_buku(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO buku
                (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            [
                request.POST.get("judul"),
                request.POST.get("pengarang"),
                request.POST.get("kategori"),
                request.POST.get("penerbit"),
                request.POST.get("tahun_terbit"),
                request.POST.get("rak"),
                request.POST.get("stok"),
                request.POST.get("deskripsi")
            ])
        return redirect("daftar_buku")

    return render(request, "tambah_buku.html")


def edit_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku WHERE id=%s", [id])
        buku = dictfetchone(cursor)

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE buku
                SET judul=%s, pengarang=%s, kategori=%s, penerbit=%s, tahun_terbit=%s, rak=%s, stok=%s, deskripsi=%s
                WHERE id=%s
            """,
            [
                request.POST.get("judul"),
                request.POST.get("pengarang"),
                request.POST.get("kategori"),
                request.POST.get("penerbit"),
                request.POST.get("tahun_terbit"),
                request.POST.get("rak"),
                request.POST.get("stok"),
                request.POST.get("deskripsi"),
                id
            ])
        return redirect("daftar_buku")

    return render(request, "edit_buku.html", {"buku": buku})


def hapus_buku(request, id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM buku WHERE id=%s", [id])
    return redirect("daftar_buku")


# =====================================================
# PEMINJAMAN
# =====================================================

def daftar_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                p.id,
                s.nama AS nama_peminjam,
                s.kelas,
                b.judul,
                p.tanggal_pinjam,
                p.jatuh_tempo,
                p.keperluan,
                p.petugas,
                p.status
            FROM peminjaman p
            JOIN siswa s ON p.siswa_id = s.id
            JOIN buku b ON p.buku_id = b.id
            ORDER BY p.id DESC
        """)
        data = dictfetchall(cursor)

    return render(request, "daftar_peminjaman.html", {"data": data})


def tambah_peminjaman(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, judul, stok FROM buku WHERE stok > 0 ORDER BY judul")
        buku_list = dictfetchall(cursor)

        # Mengambil semua siswa tanpa filter status agar nama lain tidak hilang
        cursor.execute("""
            SELECT id, nama, kelas 
            FROM siswa 
            ORDER BY nama
        """)
        users = dictfetchall(cursor)

    if request.method == "POST":
        siswa_id = request.POST.get("siswa_id")
        buku_id = request.POST.get("buku_id")
        jumlah_pinjam = int(request.POST.get("jumlah_pinjam", 1))
        keperluan = request.POST.get("keperluan")
        catatan = request.POST.get("catatan")
        petugas = request.POST.get("petugas", "Imam")

        tanggal_pinjam = date.today().strftime('%Y-%m-%d')
        jatuh_tempo = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

        with connection.cursor() as cursor:
            cursor.execute("SELECT nama FROM siswa WHERE id = %s", [siswa_id])
            siswa = dictfetchone(cursor)

            if not siswa:
                return HttpResponse("Data siswa tidak ditemukan.")

            cursor.execute("SELECT stok FROM buku WHERE id = %s", [buku_id])
            buku_skrg = dictfetchone(cursor)

            if buku_skrg and buku_skrg['stok'] >= jumlah_pinjam:
                cursor.execute("""
                    INSERT INTO peminjaman
                    (siswa_id, nama_peminjam, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, petugas, catatan, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Dipinjam')
                """, [
                    siswa_id,
                    siswa["nama"],
                    buku_id,
                    tanggal_pinjam,
                    jatuh_tempo,
                    keperluan,
                    petugas,
                    catatan
                ])

                cursor.execute("""
                    UPDATE buku
                    SET stok = stok - %s
                    WHERE id = %s
                """, [jumlah_pinjam, buku_id])

                return redirect("daftar_peminjaman")
            else:
                return HttpResponse("Gagal menyimpan! Jumlah pinjam melebihi sisa stok buku saat ini.")

    return render(
        request,
        "tambah_peminjam.html",
        {
            "buku_list": buku_list,
            "users": users,
            "petugas_aktif": "Imam"
        }
    )


def kembalikan_buku(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT buku_id
            FROM peminjaman
            WHERE id=%s
        """, [id])
        data = dictfetchone(cursor)

        if data:
            cursor.execute("""
                UPDATE peminjaman
                SET status='Dikembalikan'
                WHERE id=%s
            """, [id])

            cursor.execute("""
                UPDATE buku
                SET stok = stok + 1
                WHERE id=%s
            """, [data['buku_id']])

    return redirect('daftar_peminjaman')


def hapus_peminjaman(request, id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM peminjaman WHERE id=%s", [id])
        return redirect('daftar_peminjaman')
    return render(request, 'hapus_peminjaman.html')


# =====================================================
# USER / SISWA
# =====================================================

def user_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, status
            FROM siswa
            ORDER BY id DESC
        """)
        users = dictfetchall(cursor)
    return render(request, "user.html", {"users": users})


def detail_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, kelas, nis, status
            FROM siswa
            WHERE id=%s
        """, [id])
        siswa = dictfetchone(cursor)

        if siswa is None:
            return HttpResponse("Data siswa tidak ditemukan")

        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE siswa_id=%s", [id])
        total_peminjaman = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE siswa_id=%s AND status='Dipinjam'", [id])
        peminjaman_aktif = cursor.fetchone()[0]

    # Menggunakan key 'user' agar sinkron dengan file html Anda
    return render(
        request,
        "detail_user.html",
        {
            "user": siswa,
            "total_peminjaman": total_peminjaman,
            "peminjaman_aktif": peminjaman_aktif
        }
    )


def tambah_user(request):
    if request.method == "POST":
        nama = request.POST["nama"]
        kelas = request.POST["kelas"]
        nis = request.POST["nis"]
        status = request.POST["status"]

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM siswa WHERE nis = %s", [nis])
            if cursor.fetchone():
                return render(request, "tambah_user.html", {"error": "NIS sudah terdaftar!"})

            cursor.execute("""
                INSERT INTO siswa (nama, kelas, nis, status)
                VALUES (%s, %s, %s, %s)
            """, [nama, kelas, nis, status])

        return redirect("user_list")
    return render(request, "tambah_user.html")


def edit_user(request, id):
    if request.method == "POST":
        nama = request.POST.get("nama")
        kelas = request.POST.get("kelas")
        nis = request.POST.get("nis")
        status = request.POST.get("status")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE siswa
                SET nama=%s, kelas=%s, nis=%s, status=%s
                WHERE id=%s
            """, [nama, kelas, nis, status, id])
        return redirect("user_list")

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa WHERE id=%s", [id])
        user = dictfetchone(cursor)

    return render(request, "edit_user.html", {"user": user})


def hapus_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM siswa WHERE id=%s", [id])
    return redirect("user_list")