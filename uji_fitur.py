"""
uji_fitur.py - Pengujian otomatis sederhana untuk Tahap 1

Cara menjalankan:
    python uji_fitur.py

Fungsi input() diganti dengan jawaban terskrip sehingga seluruh alur menu
dapat diuji tanpa mengetik manual. Jika semua asersi lolos, program
mencetak "SEMUA PENGUJIAN LULUS".
"""

import builtins
import contextlib
import io

import buku
import main

DATA_AWAL = [
    ("BK001", "Algoritma dan Pemrograman", "Rinaldi Munir", "Teknologi", 2020),
    ("BK002", "Struktur Data dengan Python", "Budi Raharjo", "Teknologi", 2019),
    ("BK003", "Laskar Pelangi", "Andrea Hirata", "Fiksi", 2005),
    ("BK004", "Bumi", "Tere Liye", "Fiksi Ilmiah", 2014),
    ("BK005", "Sapiens", "Yuval Noah Harari", "Sejarah", 2017),
    ("BK006", "Pengantar Algoritma", "Thomas H. Cormen", "Teknologi", 2013),
    ("BK007", "Kosmos", "Carl Sagan", "Sains", 1980),
]


def siapkan_data(dipinjam=()):
    """Mengisi koleksi dengan data contoh; 'dipinjam' = daftar kode buku."""
    buku.koleksi_buku.clear()
    for data in DATA_AWAL:
        satu_buku = buku.buat_buku(*data)
        if satu_buku["kode_buku"] in dipinjam:
            satu_buku["status"] = buku.STATUS_DIPINJAM
        buku.koleksi_buku.append(satu_buku)


def jalankan(jawaban):
    """Menjalankan menu utama dengan input terskrip; mengembalikan output."""
    antrean = list(jawaban)
    keluaran = io.StringIO()
    input_asli = builtins.input
    builtins.input = lambda prompt="": antrean.pop(0)
    try:
        with contextlib.redirect_stdout(keluaran):
            main.jalankan_program()
    finally:
        builtins.input = input_asli
    assert not antrean, "Masih ada jawaban yang tidak terpakai: %r" % antrean
    return keluaran.getvalue()


def status_semua():
    return {b["kode_buku"]: b["status"] for b in buku.koleksi_buku}


def uji_tambah_buku():
    siapkan_data()
    # kode duplikat (beda huruf besar/kecil) ditolak, tahun tidak valid ditolak
    keluaran = jalankan(["1", "bk001", "BK008", "Judul Baru", "Penulis",
                         "Genre", "abc", "2035", "-5", "2000", "", "0"])
    assert "sudah digunakan" in keluaran
    assert keluaran.count("Tahun terbit") >= 3
    assert len(buku.koleksi_buku) == 8
    buku_baru = buku.koleksi_buku[-1]
    assert buku_baru["tahun_terbit"] == 2000
    assert buku_baru["status"] == "Tersedia"      # status otomatis


def uji_batal_di_tambah_buku():
    siapkan_data()
    keluaran = jalankan(["1", "BK008", "Judul", "batal", "", "0"])
    assert "Penambahan buku dibatalkan" in keluaran
    assert len(buku.koleksi_buku) == 7


def uji_tampil_semua():
    buku.koleksi_buku.clear()
    assert "Belum ada buku dalam koleksi." in jalankan(["2", "", "0"])
    siapkan_data(dipinjam=("BK003",))
    keluaran = jalankan(["2", "", "0"])
    assert "Total buku: 7 | Tersedia: 6 | Dipinjam: 1" in keluaran


def uji_cari_buku():
    siapkan_data()
    assert "Ditemukan 2 buku" in jalankan(["3", "2", "ALGORITMA", "", "0"])
    assert "tidak ditemukan" in jalankan(["3", "2", "matematika", "", "0"])
    assert "Buku ditemukan (1 hasil)" in jalankan(["3", "1", "BK004", "", "0"])
    assert "tidak ditemukan" in jalankan(["3", "1", "BK00", "", "0"])   # exact
    assert "tidak ditemukan" in jalankan(["3", "1", "bk004", "", "0"])  # case sensitive
    # kata 'batal' hanya membatalkan di F1; di F3 dianggap kata kunci biasa
    buku.koleksi_buku.append(buku.buat_buku("BK099", "Batal Sudah", "X", "Batal", 2000))
    assert "Ditemukan 1 buku" in jalankan(["3", "2", "batal", "", "0"])
    assert "(1 buku ditemukan)" in jalankan(["5", "batal", "", "0"])


def uji_update_status():
    siapkan_data(dipinjam=("BK003",))
    jalankan(["4", "BK002", "y", "", "4", "BK003", "y", "", "0"])
    assert status_semua()["BK002"] == "Dipinjam"
    assert status_semua()["BK003"] == "Tersedia"
    jalankan(["4", "BK001", "n", "", "0"])                # dibatalkan
    assert status_semua()["BK001"] == "Tersedia"
    assert "tidak ditemukan" in jalankan(["4", "ZZ", "", "0"])


def uji_filter_genre():
    siapkan_data()
    assert "(2 buku ditemukan)" in jalankan(["5", "FIKSI", "", "0"])
    assert "Tidak ada buku dengan genre" in jalankan(["5", "Horor", "", "0"])


def uji_hapus_buku():
    siapkan_data(dipinjam=("BK003",))
    keluaran = jalankan(["6", "BK003", "", "0"])
    assert "tidak dapat dihapus" in keluaran
    assert "Yakin ingin menghapus" not in keluaran   # cek status sebelum konfirmasi
    jalankan(["6", "BK007", "n", "", "0"])           # batal
    assert len(buku.koleksi_buku) == 7
    jalankan(["6", "BK005", "x", "y", "", "0"])      # 'x' diulang, 'y' hapus
    assert len(buku.koleksi_buku) == 6
    assert "BK005" not in status_semua()


def uji_menu_tidak_valid():
    siapkan_data()
    assert jalankan(["abc", "", "7", "0"]).count("Pilihan tidak valid") == 3

def uji_update_kode_persis():
    siapkan_data()
    assert "tidak ditemukan" in jalankan(["4", "bk002", "", "0"])
    assert status_semua()["BK002"] == "Tersedia"


def uji_validasi_tahun():
    assert buku.validasi_tahun("2000") == (2000, None)
    assert buku.validasi_tahun("abc")[0] is None
    assert buku.validasi_tahun("0")[0] is None
    assert buku.validasi_tahun("9999")[0] is None

if __name__ == "__main__":
    uji_tambah_buku()
    uji_batal_di_tambah_buku()
    uji_tampil_semua()
    uji_cari_buku()
    uji_update_status()
    uji_filter_genre()
    uji_hapus_buku()
    uji_menu_tidak_valid()
    uji_update_kode_persis()
    uji_validasi_tahun()
    print("SEMUA PENGUJIAN LULUS")
