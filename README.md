
### Anggota Kelompok :
|             Nama              |     NRP    |
|-------------------------------|------------|
| Nayla Raissa Azzahra          | 5027231054 |
| Aisha Ayya Ratiandari              | 5027231056 |
| Aisyah Rahmasari              | 5027231072 |

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


# Panduan Simulasi Serangan dan Deteksi Anomali
## LANGKAH 0: Persiapan Awal 

**Struktur Folder Awal**
<img width="402" height="433" alt="Screenshot 2025-11-04 232149" src="https://github.com/user-attachments/assets/d8ee2e54-64f1-478b-8b91-4a254ef2d13c" />
*Deskripsi foto: Menunjukkan folder `secure_files` dan file-file Python sebelum program dijalankan.*

---

## LANGKAH 1: Membuat Baseline Awal

1. Buka Terminal (atau Command Prompt) di dalam folder proyekmu.
2. Jalankan perintah berikut:

   ```bash
   python integrity_checker.py --init
    ````

Perhatikan output di terminal. Program akan memberitahu bahwa ia sedang membuat baseline dan berhasil menyimpannya.
<img width="1557" height="173" alt="Screenshot 2025-11-04 235013" src="https://github.com/user-attachments/assets/8a895fcb-a23c-4d9c-9cdc-15fb135709df" />

---

## LANGKAH 2: Verifikasi Kondisi Normal

1. Di terminal yang sama, jalankan perintah pengecekan:

   ```bash
   python integrity_checker.py --check
   ```

   Outputnya akan menunjukkan "Verifikasi OK" untuk setiap file.
<img width="1545" height="179" alt="Screenshot 2025-11-04 235251" src="https://github.com/user-attachments/assets/26362a74-7912-4393-aecf-7af4a5f34196" />
*Deskripsi foto: Terminal menampilkan log `INFO: Verifikasi OK` untuk semua file, menandakan tidak ada perubahan yang terdeteksi.*

---

## LANGKAH 3: Melakukan "Serangan"

Sekarang adalah bagian utamanya. Kita akan memodifikasi folder `secure_files` secara manual.

1. **Ubah File**: Buka file `secure_files/data.txt` menggunakan Notepad atau teks editor. Ganti isinya menjadi:

   ```
   Isi data rahasia ini sudah diubah!
   ```

   Lalu simpan.

2. **Hapus File**: Di File Explorer, klik kanan pada file `secure_files/config.txt` dan hapus file tersebut.

3. **Tambah File Baru**: Di dalam folder `secure_files`, buat sebuah file baru. Beri nama `hacked.js` dan isi dengan teks:

   ```javascript
   alert('kamu sudah di-hack');
   ```

**Screenshot 4: Kondisi Folder Setelah Diserang**
*Deskripsi foto: Folder `secure_files` sekarang berisi `data.txt` (yang isinya sudah diubah), file baru `hacked.js`, dan file `config.txt` sudah tidak ada.*

---

## LANGKAH 4: Menjalankan Deteksi Anomali

Waktunya melihat apakah sistem kita berhasil mendeteksi semua perubahan mencurigakan tersebut.

1. Kembali ke terminal.
2. Jalankan lagi perintah pengecekan:

   ```bash
   python integrity_checker.py --check
   ```

   Perhatikan outputnya dengan saksama! Kamu akan melihat sistem melaporkan ketiga anomali dengan level yang berbeda (WARNING dan ALERT).

**Screenshot 5: Sistem Mendeteksi Anomali**
*Deskripsi foto: Output terminal setelah menjalankan `--check`. Terlihat jelas log `WARNING` untuk file yang diubah dan dihapus, serta log `ALERT` untuk file baru yang tidak dikenal.*

---

## LANGKAH 5: Melihat Laporan Ringkas

Terakhir, mari kita lihat ringkasan dari semua aktivitas yang tercatat di `security.log`.

1. Di terminal, jalankan skrip laporan:

   ```bash
   python report_generator.py
   ```

   Hasilnya akan berupa ringkasan jumlah file yang aman dan yang terdeteksi memiliki anomali, beserta waktu anomali terakhir.

**Screenshot 6: Laporan Akhir Status Keamanan**
*Deskripsi foto: Hasil akhir dari `report_generator.py` yang merangkum jumlah file rusak/anomali dan waktu kejadian terakhir, memberikan gambaran cepat tentang status keamanan sistem.*

---

Dengan panduan ini, kamu bisa membuat dokumentasi yang sangat jelas dan profesional di README.md GitHub-mu atau untuk laporan tugasmu. Selamat mencoba!

```

Kamu bisa langsung menyalin dan menempelkan markdown di atas ke file README.md GitHub-mu. Panduan ini sudah terstruktur dengan baik dan siap untuk digunakan!
```

