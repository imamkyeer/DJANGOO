from flask import Flask, render_template, request, redirect
from koneksi import conn, cur

app = Flask(__name__)

# =========================
# TAMPILKAN DATA
# =========================

@app.route("/")
def index():

    cur.execute("""
        SELECT *
        FROM siswa
        ORDER BY id
    """)

    data = cur.fetchall()

    return render_template(
        "index.html",
        siswa=data
    )

# =========================
# TAMBAH DATA
# =========================

@app.route("/tambah", methods=["POST"])
def tambah():

    nama = request.form["nama"]
    umur = request.form["umur"]
    tgl_lahir = request.form["tgl_lahir"]
    nilai_akhir = request.form["nilai_akhir"]

    query = """
    INSERT INTO siswa (
        nama,
        umur,
        tgl_lahir,
        nilai_akhir
    )
    VALUES (%s, %s, %s, %s)
    """

    cur.execute(
        query,
        (
            nama,
            umur,
            tgl_lahir,
            nilai_akhir
        )
    )

    conn.commit()

    return redirect("/")

# =========================
# UPDATE DATA
# =========================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    nama = request.form["nama"]
    umur = request.form["umur"]
    tgl_lahir = request.form["tgl_lahir"]
    nilai_akhir = request.form["nilai_akhir"]

    query = """
    UPDATE siswa
    SET
        nama=%s,
        umur=%s,
        tgl_lahir=%s,
        nilai_akhir=%s
    WHERE id=%s
    """

    cur.execute(
        query,
        (
            nama,
            umur,
            tgl_lahir,
            nilai_akhir,
            id
        )
    )

    conn.commit()

    return redirect("/")

# =========================
# HAPUS DATA
# =========================

@app.route("/hapus/<int:id>")
def hapus(id):

    query = """
    DELETE FROM siswa
    WHERE id=%s
    """

    cur.execute(query, (id,))

    conn.commit()

    return redirect("/")

# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )