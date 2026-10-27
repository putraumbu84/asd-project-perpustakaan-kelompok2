"""
buku.py - Modul data buku (Tahap 1: Array & Struct)

Seluruh koleksi buku disimpan dalam sebuah list (Array) yang setiap
elemennya adalah dictionary (Struct) dengan 6 atribut wajib:
kode_buku, judul, pengarang, genre, tahun_terbit, status.

Data hanya disimpan di memori, sehingga hilang saat program ditutup
(sesuai ketentuan Tahap 1).
"""

from datetime import date

# ---------------------------------------------------------------------
# Konstanta
# ---------------------------------------------------------------------
STATUS_TERSEDIA = "Tersedia"
STATUS_DIPINJAM = "Dipinjam"
KATA_BATAL = "batal"      # hanya berlaku di F1 (Tambah Buku)
LEBAR_KOLOM_MAKS = 30     # judul/pengarang yang lebih panjang dipotong

# Array of Struct: list berisi dict buku
koleksi_buku = []


# ---------------------------------------------------------------------
# Fungsi bantu (dipakai oleh banyak fitur)
# ---------------------------------------------------------------------
def buat_buku(kode_buku, judul, pengarang, genre, tahun_terbit):
    """Membuat satu struct buku. Status awal selalu 'Tersedia'."""
    return {
        "kode_buku": kode_buku,
        "judul": judul,
        "pengarang": pengarang,
        "genre": genre,
        "tahun_terbit": tahun_terbit,
        "status": STATUS_TERSEDIA,
    }


def cari_indeks_by_kode(kode):
    """
    Linear search: mengembalikan indeks buku dengan kode yang sama persis
    (huruf besar/kecil dibedakan), atau -1 jika tidak ada.
    """
    for indeks, buku in enumerate(koleksi_buku):
        if buku["kode_buku"] == kode:
            return indeks
    return -1


def kode_sudah_ada(kode):
    """
    Cek duplikat kode untuk F1. Huruf besar/kecil diabaikan agar 'bk001'
    dan 'BK001' tidak dianggap dua buku yang berbeda.
    """
    for buku in koleksi_buku:
        if buku["kode_buku"].lower() == kode.lower():
            return True
    return False


def validasi_tahun(teks_tahun):
    """
    Memvalidasi tahun terbit.
    Mengembalikan (tahun_int, None) jika valid, atau (None, pesan_error).
    """
    if not (teks_tahun.isascii() and teks_tahun.isdigit()):
        return None, "Tahun terbit harus berupa angka bulat positif."
    tahun = int(teks_tahun)
    if tahun <= 0:
        return None, "Tahun terbit harus berupa angka bulat positif."
    tahun_sekarang = date.today().year
    if tahun > tahun_sekarang:
        return None, ("Tahun terbit tidak boleh lebih besar dari tahun "
                      "sekarang (%d)." % tahun_sekarang)
    return tahun, None


def minta_input_wajib(label, boleh_batal=False):
    """
    Meminta input teks yang tidak boleh kosong. Jika kosong, tampilkan
    error dan minta lagi. Jika boleh_batal=True dan petugas mengetik
    'batal', mengembalikan None. Tanpa boleh_batal, kata 'batal' diperlakukan
    sebagai teks biasa (supaya judul/genre 'Batal' tetap bisa dicari).
    """
    while True:
        nilai = input("%s: " % label).strip()
        if boleh_batal and nilai.lower() == KATA_BATAL:
            return None
        if nilai == "":
            nama_isian = label.replace("Masukkan ", "", 1)
            nama_isian = nama_isian[0].upper() + nama_isian[1:]
            print("[GAGAL] %s tidak boleh kosong." % nama_isian)
            continue
        return nilai


def minta_konfirmasi(pertanyaan):
    """Meminta jawaban y/n. Mengembalikan True untuk 'y', False untuk 'n'."""
    while True:
        jawaban = input("%s (y/n): " % pertanyaan).strip().lower()
        if jawaban in ("y", "n"):
            return jawaban == "y"
        print("[GAGAL] Masukkan 'y' untuk ya atau 'n' untuk tidak.")


def potong_teks(teks, panjang_maks):
    """Memotong teks yang terlalu panjang agar tabel tetap rapi."""
    if len(teks) <= panjang_maks:
        return teks
    return teks[:panjang_maks - 3] + "..."


def hitung_ringkasan(daftar_buku):
    """Mengembalikan (total, jumlah_tersedia, jumlah_dipinjam)."""
    tersedia = 0
    dipinjam = 0
    for buku in daftar_buku:
        if buku["status"] == STATUS_TERSEDIA:
            tersedia += 1
        else:
            dipinjam += 1
    return len(daftar_buku), tersedia, dipinjam


def cetak_tabel(daftar_buku):
    """Mencetak daftar buku dalam bentuk tabel dengan lebar kolom dinamis."""
    judul_kolom = ["No", "Kode", "Judul", "Pengarang", "Genre",
                   "Tahun Terbit", "Status"]
    baris_data = []
    for nomor, buku in enumerate(daftar_buku, start=1):
        baris_data.append([
            str(nomor),
            buku["kode_buku"],
            potong_teks(buku["judul"], LEBAR_KOLOM_MAKS),
            potong_teks(buku["pengarang"], LEBAR_KOLOM_MAKS),
            potong_teks(buku["genre"], LEBAR_KOLOM_MAKS),
            str(buku["tahun_terbit"]),
            "[%s]" % buku["status"].upper(),
        ])

    # Lebar tiap kolom = teks terpanjang di kolom tersebut (termasuk header)
    lebar = []
    for i in range(len(judul_kolom)):
        terpanjang = len(judul_kolom[i])
        for baris in baris_data:
            terpanjang = max(terpanjang, len(baris[i]))
        lebar.append(terpanjang)

    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def format_baris(isi):
        sel = [isi[i].ljust(lebar[i]) for i in range(len(isi))]
        return "| " + " | ".join(sel) + " |"

    print(garis)
    print(format_baris(judul_kolom))
    print(garis)
    for baris in baris_data:
        print(format_baris(baris))
    print(garis)


def cetak_detail(buku):
    """Mencetak seluruh atribut satu buku secara vertikal."""
    print("  Kode Buku    : %s" % buku["kode_buku"])
    print("  Judul        : %s" % buku["judul"])
    print("  Pengarang    : %s" % buku["pengarang"])
    print("  Genre        : %s" % buku["genre"])
    print("  Tahun Terbit : %d" % buku["tahun_terbit"])
    print("  Status       : [%s]" % buku["status"].upper())


# ---------------------------------------------------------------------
# F1 - Tambah Buku Baru
# ---------------------------------------------------------------------
def minta_kode_baru():
    """Meminta kode buku yang belum dipakai. None jika dibatalkan."""
    while True:
        kode = minta_input_wajib("Kode Buku", boleh_batal=True)
        if kode is not None and kode_sudah_ada(kode):
            print("[GAGAL] Kode buku '%s' sudah digunakan. "
                  "Gunakan kode lain." % kode)
            continue
        return kode


def minta_teks(label):
    """Meminta satu isian teks wajib di F1. None jika dibatalkan."""
    return minta_input_wajib(label, boleh_batal=True)


def minta_tahun():
    """Meminta tahun terbit yang valid (int). None jika dibatalkan."""
    while True:
        teks = minta_input_wajib("Tahun Terbit", boleh_batal=True)
        if teks is None:
            return None
        tahun, pesan_error = validasi_tahun(teks)
        if pesan_error:
            print("[GAGAL] %s" % pesan_error)
            continue
        return tahun


def tambah_buku():
    """Menambah buku baru ke koleksi dengan validasi setiap atribut."""
    print("\n--- TAMBAH BUKU BARU ---")
    print("(ketik '%s' pada isian mana pun untuk membatalkan)" % KATA_BATAL)

    # Urutan isian: (nama field, fungsi yang meminta nilainya)
    langkah = [
        ("kode_buku", minta_kode_baru),
        ("judul", lambda: minta_teks("Judul")),
        ("pengarang", lambda: minta_teks("Pengarang")),
        ("genre", lambda: minta_teks("Genre")),
        ("tahun_terbit", minta_tahun),
    ]

    isian = {}
    for nama_field, minta in langkah:
        nilai = minta()
        if nilai is None:
            print("[INFO] Penambahan buku dibatalkan.")
            return
        isian[nama_field] = nilai

    koleksi_buku.append(buat_buku(**isian))
    print("[OK] Buku '%s' dengan kode %s berhasil ditambahkan ke koleksi."
          % (isian["judul"], isian["kode_buku"]))


# ---------------------------------------------------------------------
# F2 - Tampilkan Semua Buku
# ---------------------------------------------------------------------
def tampilkan_semua_buku():
    """Menampilkan seluruh koleksi dalam tabel beserta ringkasannya."""
    print("\n--- DAFTAR SEMUA BUKU ---")
    if len(koleksi_buku) == 0:
        print("[INFO] Belum ada buku dalam koleksi.")
        return

    cetak_tabel(koleksi_buku)
    total, tersedia, dipinjam = hitung_ringkasan(koleksi_buku)
    print("Total buku: %d | Tersedia: %d | Dipinjam: %d"
          % (total, tersedia, dipinjam))


# ---------------------------------------------------------------------
# F3 - Cari Buku
# ---------------------------------------------------------------------
def cari_buku():
    """Mencari buku berdasarkan kode (exact) atau judul (partial)."""
    print("\n--- CARI BUKU ---")
    print("Mode pencarian:")
    print("  1. Berdasarkan kode buku (harus persis sama)")
    print("  2. Berdasarkan judul (cukup sebagian kata)")
    mode = input("Pilih mode (1/2): ").strip()

    if mode == "1":
        cari_berdasarkan_kode()
    elif mode == "2":
        cari_berdasarkan_judul()
    else:
        print("[GAGAL] Mode pencarian tidak valid. Pilih 1 atau 2.")


def cari_berdasarkan_kode():
    """Pencarian exact match (huruf besar/kecil dibedakan), maksimal 1 hasil."""
    kata_kunci = minta_input_wajib("Masukkan kode buku")
    indeks = cari_indeks_by_kode(kata_kunci)
    if indeks == -1:
        print("[INFO] Buku dengan kode '%s' tidak ditemukan dalam koleksi."
              % kata_kunci)
        return
    print("[OK] Buku ditemukan (1 hasil):")
    cetak_detail(koleksi_buku[indeks])


def cari_berdasarkan_judul():
    """Pencarian partial match pada judul, tidak case sensitive."""
    kata_kunci = minta_input_wajib("Masukkan judul/kata kunci")
    hasil = []
    for buku in koleksi_buku:
        if kata_kunci.lower() in buku["judul"].lower():
            hasil.append(buku)
    if len(hasil) == 0:
        print("[INFO] Buku dengan judul '%s' tidak ditemukan dalam koleksi."
              % kata_kunci)
        return
    print("[OK] Ditemukan %d buku dengan judul mengandung '%s':"
          % (len(hasil), kata_kunci))
    cetak_tabel(hasil)


# ---------------------------------------------------------------------
# F4 - Update Status Buku
# ---------------------------------------------------------------------
def update_status_buku():
    """Toggle status Tersedia <-> Dipinjam setelah konfirmasi petugas."""
    print("\n--- UPDATE STATUS BUKU ---")
    kode = minta_input_wajib("Masukkan kode buku")

    indeks = cari_indeks_by_kode(kode)
    if indeks == -1:
        print("[GAGAL] Buku dengan kode '%s' tidak ditemukan dalam koleksi."
              % kode)
        return

    buku = koleksi_buku[indeks]
    print("Informasi buku:")
    print("  Judul     : %s" % buku["judul"])
    print("  Pengarang : %s" % buku["pengarang"])
    print("  Status    : [%s]" % buku["status"].upper())

    if buku["status"] == STATUS_TERSEDIA:
        status_baru = STATUS_DIPINJAM
        kata_kerja = "dipinjam"
    else:
        status_baru = STATUS_TERSEDIA
        kata_kerja = "dikembalikan"

    if not minta_konfirmasi("Ubah status menjadi %s?" % status_baru):
        print("[INFO] Perubahan status dibatalkan.")
        return

    status_lama = buku["status"]
    buku["status"] = status_baru
    print("[OK] Buku '%s' berhasil %s. Status diubah: %s menjadi %s."
          % (buku["judul"], kata_kerja, status_lama, status_baru))


# ---------------------------------------------------------------------
# F5 - Filter Buku Berdasarkan Genre
# ---------------------------------------------------------------------
def filter_buku_by_genre():
    """Menampilkan buku yang genre-nya mengandung kata kunci (partial)."""
    print("\n--- FILTER BUKU BERDASARKAN GENRE ---")
    genre = minta_input_wajib("Masukkan genre")

    hasil = []
    for buku in koleksi_buku:
        if genre.lower() in buku["genre"].lower():
            hasil.append(buku)

    if len(hasil) == 0:
        print("[INFO] Tidak ada buku dengan genre '%s' dalam koleksi." % genre)
        return

    print("Menampilkan buku genre: %s (%d buku ditemukan)."
          % (genre, len(hasil)))
    cetak_tabel(hasil)


# ---------------------------------------------------------------------
# F6 - Hapus Buku
# ---------------------------------------------------------------------
def hapus_buku():
    """Menghapus buku berdasarkan kode; buku Dipinjam tidak boleh dihapus."""
    print("\n--- HAPUS BUKU ---")
    kode = minta_input_wajib("Masukkan kode buku")

    indeks = cari_indeks_by_kode(kode)
    if indeks == -1:
        print("[GAGAL] Buku dengan kode '%s' tidak ditemukan dalam koleksi."
              % kode)
        return

    buku = koleksi_buku[indeks]

    # Cek status SEBELUM menampilkan konfirmasi
    if buku["status"] == STATUS_DIPINJAM:
        print("[GAGAL] Buku '%s' tidak dapat dihapus karena sedang dalam "
              "status Dipinjam. Pastikan buku dikembalikan terlebih dahulu "
              "sebelum dihapus dari koleksi." % buku["judul"])
        return

    print("Detail buku yang akan dihapus:")
    print("  Judul     : %s" % buku["judul"])
    print("  Pengarang : %s" % buku["pengarang"])
    print("  Genre     : %s" % buku["genre"])
    print("  Status    : [%s]" % buku["status"].upper())

    if not minta_konfirmasi("Yakin ingin menghapus buku ini?"):
        print("[INFO] Penghapusan dibatalkan.")
        return

    koleksi_buku.pop(indeks)
    print("[OK] Buku '%s' dengan kode %s berhasil dihapus dari koleksi."
          % (buku["judul"], buku["kode_buku"]))
