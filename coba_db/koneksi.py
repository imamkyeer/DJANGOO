import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="sekolah_db",
    user="postgres",
    password="09876",
    port="5432"
)

cur = conn.cursor()

print("Koneksi berhasil!")