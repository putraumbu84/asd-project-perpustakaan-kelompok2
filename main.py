"""
main.py - Titik masuk program Sistem Perpustakaan Mini (Tahap 1)

Cara menjalankan:
    python main.py
"""

import buku

LEBAR_GARIS = 46


def tampilkan_menu():
    """Mencetak menu utama ke terminal."""
    print()
    print("=" * LEBAR_GARIS)
    print("        SISTEM PERPUSTAKAAN MINI")
    print("=" * LEBAR_GARIS)
    print(" 1. Tambah Buku Baru")
    print(" 2. Tampilkan Semua Buku")
    print(" 3. Cari Buku")
    print(" 4. Update Status Buku (Pinjam/Kembali)")
    print(" 5. Filter Buku Berdasarkan Genre")
    print(" 6. Hapus Buku")
    print(" 0. Keluar")
    print("=" * LEBAR_GARIS)


def jalankan_program():
    """Loop utama: tampilkan menu, jalankan fitur, kembali ke menu."""
    # Peta pilihan menu -> fungsi fitur
    daftar_fitur = {
        "1": buku.tambah_buku,
        "2": buku.tampilkan_semua_buku,
        "3": buku.cari_buku,
        "4": buku.update_status_buku,
        "5": buku.filter_buku_by_genre,
        "6": buku.hapus_buku,
    }

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-6): ").strip()

        if pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        if pilihan in daftar_fitur:
            daftar_fitur[pilihan]()
            input("\nTekan Enter untuk kembali ke menu...")
        else:
            print("[GAGAL] Pilihan tidak valid. Masukkan angka 0 sampai 6.")


if __name__ == "__main__":
    try:
        jalankan_program()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")
