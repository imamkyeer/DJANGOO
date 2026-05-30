from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.utils.html import escape

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            ORDER BY id DESC
        """)
        data_siswa = dictfetchall(cursor)

        #passing data

    search_text = "belanda"

    return render(request, 'list.html',
                {
                    'keyword': search_text,
                    'data': data_siswa
        })



def dictfetchone(cursor):
    """Mengubah satu hasil query menjadi dictionary."""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    
def dictfetchone(cursor):
    """Mengubah satu hasil query menjadi dictionary."""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row is None:
        return None

    return dict(zip(columns, row))


    return render(request, 'list.html')


def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM siswa
            WHERE id = %s
            """,
            [id]
        )
        siswa = dictfetchone(cursor)    

    return render(request, 'detail.html', {
        'siswa': siswa,
    })




def siswa_create(request):
    # cek request yg masuk, klo dia POST (submit)
    if request.method == 'POST':        
        # kumpulkan data dari request post
        nama = request.POST.get('nama', '').strip()
        umur = request.POST.get('umur', '').strip()

        # eksekusi query insert ke tabel siswa
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO siswa (nama, umur)
                VALUES (%s, %s)
                """,
                [nama, umur]
            )

        # klo berhasil maka redirect ke siswa list
        return redirect(request, 'list.html')

    # klo gk submit (GET)
    return render(request, 'form.html')



# EDIT DATA
# ========================
def siswa_edit(request, id):

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM siswa WHERE id=%s",
            [id]
        )

        row = cursor.fetchone()

    siswa = {
        'id': row[0],
        'nama': row[1],
        'umur': row[2],
        'tgl_lahir': row[3],
        'status_hadir': row[4],
        'nilai_akhir': row[5],
    }

    if request.method == 'POST':

        nama = request.POST.get('nama')
        umur = request.POST.get('umur')
        tgl_lahir = request.POST.get('tgl_lahir')
        status_hadir = request.POST.get('status_hadir')
        nilai_akhir = request.POST.get('nilai_akhir')

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE siswa
                SET
                    nama=%s,
                    umur=%s,
                    tgl_lahir=%s,
                    status_hadir=%s,
                    nilai_akhir=%s
                WHERE id=%s
                """,
                [
                    nama,
                    umur,
                    tgl_lahir,
                    status_hadir,
                    nilai_akhir,
                    id
                ]
            )

        return redirect('siswa_list')

    return render(request, 'edit.html', {
        'siswa': siswa
    })

# HAPUS DATA
def siswa_delete(request, id):

    # ambil data siswa
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM siswa WHERE id=%s",
            [id]
        )

        row = cursor.fetchone()

    siswa = {
        'id': row[0],
        'nama': row[1],
        'tgl_lahir': row[3],
        
    }

    # kalau tombol hapus ditekan
    if request.method == 'POST':

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM siswa WHERE id=%s",
                [id]
            )

        return redirect('siswa_list')

    return render(request, 'hapus.html', {'siswa': siswa})