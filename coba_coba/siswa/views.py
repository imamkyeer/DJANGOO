from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa


def index(request):
    data = Siswa.objects.all()
    return render(request, 'siswa/index.html', {'data': data})




def tambah(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        umur = request.POST['umur']
        tgl_lahir = request.POST['tgl_lahir']
        nilai_akhir = request.POST['nilai_akhir']

        Siswa.objects.create(
            nama=nama,
            umur=umur,
            tgl_lahir=tgl_lahir,
            nilai_akhir=nilai_akhir
        )

        return redirect('/')

    return render(request, 'siswa/tambah.html')


def edit(request, id):
    siswa = get_object_or_404(Siswa, id=id)

    if request.method == 'POST':
        siswa.nama = request.POST['nama']
        siswa.umur = request.POST['umur']
        siswa.tgl_lahir = request.POST['tgl_lahir']
        siswa.nilai_akhir = request.POST['nilai_akhir']
        siswa.save()

        return redirect('/')

    return render(request, 'siswa/edit.html', {'siswa': siswa})


def hapus(request, id):
    siswa = get_object_or_404(Siswa, id=id)
    siswa.delete()
    return redirect('/')