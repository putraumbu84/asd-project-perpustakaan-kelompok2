# Sistem Perpustakaan Mini (Tahap 1: Array & Struct)

Project Semester - Algoritma dan Struktur Data Sistem Informasi, FTI Unmer Malang | Semester 3 | Tahun Ajaran 2026/2027
Dosen Pengampu: Amadea Permana Sanusi, S.Tr.T., M.Tr.Kom

## 1. Nama & Anggota Kelompok

**Nama sistem:** Sistem Perpustakaan Mini (PerpusMini)
**Tema:** Tema 3 - Perpustakaan Mini
**Kelompok:** Kelompok 2

| No | Nama Lengkap | NIM | Username GitHub |
|----|--------------|-----|-----------------|
| 1 | Putra Umbu Tonga Wohangara | 25083000084 | putraumbu84 |
| 2 | Viggrius Dangkur | 25083000095 | vikidangkur-svg |
| 3 | Agustian Vianney Calado Jandu | 25083000018 | vigojandu73 |
| 4 | Marselus Salvano Tikung | 25083000042 | cellosalvano2007 |
| 5 | Justin Putra Oktavian Lou | 25083000082 | JustinPutra24 |

## 2. Deskripsi Sistem

Sistem Perpustakaan Mini adalah program Python berbasis terminal (CLI) yang membantu petugas perpustakaan mengelola koleksi buku. Petugas dapat mencatat buku baru, melihat seluruh koleksi, mencari buku, memperbarui status peminjaman, memfilter buku berdasarkan genre, dan menghapus buku dari koleksi. Seluruh data disimpan dalam list of dict (Array of Struct) di memori, sehingga data hilang saat program ditutup (sesuai ketentuan Tahap 1).

## 3. Cara Menjalankan

Prasyarat: Python 3.8 atau lebih baru. Tidak memerlukan library eksternal.

```bash
# 1. Clone repository
git clone https://github.com/putraumbu84/asd-project-perpustakaan-kelompok2.git

# 2. Masuk ke folder project
cd asd-project-perpustakaan-kelompok2

# 3. Jalankan program
python main.py
```

Pengujian otomatis (opsional): `python uji_fitur.py`. Pengujian mencakup F1 sampai F6, pembatalan di F1, validasi tahun terbit, dan pencarian kode yang membedakan huruf besar/kecil. Jika semua lolos, muncul tulisan "SEMUA PENGUJIAN LULUS".

Tips: ketik `batal` pada isian apa pun di Fitur 1 (Tambah Buku) untuk membatalkan proses dan kembali ke menu. Di fitur lain, kata `batal` diperlakukan sebagai teks biasa.

## 4. Fitur yang Sudah Ada

| Kode | Fitur | Keterangan |
|------|-------|------------|
| F1 | Tambah Buku Baru | Validasi: semua isian wajib diisi, kode buku tidak boleh duplikat (huruf besar/kecil tidak dibedakan, jadi `bk001` dan `BK001` dianggap sama), tahun terbit angka bulat positif dan tidak melebihi tahun sekarang. Status otomatis "Tersedia". |
| F2 | Tampilkan Semua Buku | Tabel lengkap dengan penanda [TERSEDIA]/[DIPINJAM] dan ringkasan total, Tersedia, Dipinjam. |
| F3 | Cari Buku | Berdasarkan kode (exact match, huruf besar/kecil dibedakan) atau judul (partial match, tidak case sensitive). |
| F4 | Update Status Buku | Toggle otomatis Tersedia <-> Dipinjam dengan konfirmasi (y/n). Kode buku dicari dengan exact match. |
| F5 | Filter Buku by Genre | Partial match dan tidak case sensitive. |
| F6 | Hapus Buku | Buku berstatus Dipinjam ditolak; konfirmasi (y/n) sebelum dihapus. Kode buku dicari dengan exact match. |

Struktur folder:

```
asd-project-perpustakaan-kelompok2/
|-- main.py          # Entry point: menu utama dan loop program
|-- buku.py          # Data buku (Array of Struct) dan fungsi F1-F6
|-- uji_fitur.py     # Pengujian otomatis Tahap 1
`-- README.md        # Dokumentasi
```

## 5. Pembagian Tugas

| Anggota | Bagian yang Dikerjakan | File / Fungsi |
|---------|------------------------|---------------|
| Putra Umbu Tonga Wohangara | Setup repository, menu utama, README | main.py: tampilkan_menu(), jalankan_program(); README.md |
| Viggrius Dangkur | F1 Tambah Buku beserta seluruh validasinya | buku.py: tambah_buku(), minta_kode_baru(), minta_teks(), minta_tahun(), validasi_tahun(), minta_input_wajib(), buat_buku() |
| Agustian Vianney Calado Jandu | F2 Tampilkan Semua Buku dan F5 Filter Genre | buku.py: tampilkan_semua_buku(), cetak_tabel(), hitung_ringkasan(), potong_teks(), filter_buku_by_genre() |
| Marselus Salvano Tikung | F3 Cari Buku dan F4 Update Status | buku.py: cari_buku(), cari_berdasarkan_kode(), cari_berdasarkan_judul(), cari_indeks_by_kode(), kode_sudah_ada(), update_status_buku(), cetak_detail() |
| Justin Putra Oktavian Lou | F6 Hapus Buku dan pengujian otomatis | buku.py: hapus_buku(), minta_konfirmasi(); uji_fitur.py |

## Rencana Tahap Berikutnya

Linked List (riwayat peminjaman), Stack (undo peminjaman), Queue dan Tree (antrian pemesanan dan kategori genre), serta Sorting.
