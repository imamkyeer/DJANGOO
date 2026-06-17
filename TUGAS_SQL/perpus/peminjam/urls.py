from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path(
        '',
        views.dashboard_view,
        name='dashboard'
    ),

    # Buku
    path(
        'buku/',
        views.daftar_buku,
        name='daftar_buku'
    ),
    path(
        'buku/detail/<int:id>/',
        views.detail_buku,
        name='detail_buku'
    ),
    path(
        'buku/tambah/',
        views.tambah_buku,
        name='tambah_buku'
    ),
    path(
        'buku/edit/<int:id>/',
        views.edit_buku,
        name='edit_buku'
    ),
    path(
        'buku/hapus/<int:id>/',
        views.hapus_buku,
        name='hapus_buku'
    ),

    # Peminjaman
    path(
        'peminjaman/',
        views.daftar_peminjaman,
        name='daftar_peminjaman'
    ),
    path(
        'peminjaman/tambah/',
        views.tambah_peminjaman,
        name='tambah_peminjaman'  # <-- DIUBAH DI SINI agar sesuai dengan template
    ),
    path(
        'peminjaman/kembali/<int:id>/',
        views.kembalikan_buku,
        name='kembalikan_buku'
    ),
    path(
        'peminjaman/hapus/<int:id>/',
        views.hapus_peminjaman,
        name='hapus_peminjaman'
    ),

    # User
    path(
        'user/',
        views.user_list,
        name='user_list'
    ),
    path(
        'user/detail/<int:id>/',
        views.detail_user,
        name='detail_user'
    ),
    path(
        'user/tambah/',
        views.tambah_user,
        name='tambah_user'
    ),
    path(
        'user/edit/<int:id>/',
        views.edit_user,
        name='edit_user'
    ),
    path(
        'user/hapus/<int:id>/',
        views.hapus_user,
        name='hapus_user'
    ),
]