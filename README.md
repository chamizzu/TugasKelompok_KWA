


# Sistem Deteksi Integritas File Sederhana

Proyek ini adalah implementasi sistem sederhana untuk mendeteksi integritas file dan aktivitas mencurigakan pada sebuah direktori. Sistem ini dibuat menggunakan Python sebagai bagian dari tugas kuliah.

## Fitur Utama

-   **Pemantauan Direktori**: Memantau folder `secure_files` terhadap perubahan file (diubah, dihapus, ditambahkan).
-   **Verifikasi Integritas**: Menggunakan hash SHA-256 untuk membuat *baseline* dan membandingkannya dengan kondisi file saat ini.
-   **Logging Komprehensif**: Semua aktivitas (normal maupun mencurigakan) dicatat ke dalam file `security.log` dengan format: `[timestamp] LEVEL: Pesan`.
-   **Simulasi & Pelaporan**: Dilengkapi dengan skrip untuk membaca file log dan menghasilkan laporan ringkas mengenai status keamanan file.

## Cara Penggunaan

### Prasyarat
- Python 3.x

### Instalasi
1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/NAMA_USER_KAMU/NAMA_REPO_KAMU.git
    cd NAMA_REPO_KAMU
    ```

2.  **(Opsional)** Jika ada dependensi, install menggunakan pip:
    ```bash
    pip install -r requirements.txt
    ```

### Menjalankan Program

1.  **Membuat Baseline Awal**
    Jalankan perintah ini untuk pertama kali. Perintah ini akan memindai folder `secure_files` dan membuat file `hash_db.json` sebagai acuan.
    ```bash
    python integrity_checker.py --init
    ```

2.  **Memeriksa Integritas File**
    Untuk memeriksa apakah ada file yang berubah, jalankan perintah berikut:
    ```bash
    python integrity_checker.py --check
    ```

3.  **Melihat Laporan Ringkas**
    Untuk melihat ringkasan status keamanan berdasarkan file `security.log`, jalankan:
    ```bash
    python report_generator.py
    ```

## Contoh Simulasi Serangan

1.  **Ubah file**: Buka `secure_files/data.txt` dan modifikasi isinya.
2.  **Hapus file**: Hapus `secure_files/config.txt`.
3.  **Tambah file baru**: Buat file `hacked.js` di dalam folder `secure_files`.
4.  Jalankan `python integrity_checker.py --check` untuk melihat bagaimana sistem mendeteksi ketiga anomali tersebut.
5.  Jalankan `python report_generator.py` untuk melihat laporannya.
