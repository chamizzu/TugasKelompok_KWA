# TUGAS KELOMPOK KWA
### Anggota Kelompok :
|             Nama              |     NRP    |
|-------------------------------|------------|
| Nayla Raissa Azzahra          | 5027231054 |
| Aisha Ayya Ratiandari              | 5027231056 |
| Adlya Isriena Aftarsiya              | 5027231066 |
| Aisyah Rahmasari              | 5027231072 |

# Sistem Deteksi Integritas File Sederhana

## Fitur Utama

-   **Dashboard Web Real-time (Flask)**: Memantau status semua file melalui antarmuka web yang dinamis dan diperbarui secara otomatis tanpa perlu refresh.
-   **Monitoring Otomatis**: Kemampuan untuk menjalankan sistem di latar belakang yang secara periodik memeriksa dan mencatat anomali.
-   **Pelacakan File Selektif (Mirip `git add`)**: Pengguna dapat memilih file mana yang akan dipantau. File yang tidak dilacak akan diabaikan dari pengecekan integritas namun tetap ditampilkan di dashboard.
-   **Pemindaian Folder Rekursif**: Sistem secara otomatis memindai semua file di dalam direktori `secure_files` dan seluruh subdirektorinya.
-   **Verifikasi Integritas (SHA-256)**: Menggunakan hash SHA-256 untuk membuat *baseline* dan membandingkannya dengan kondisi file saat ini.
-   **Logging Komprehensif**: Semua anomali (file diubah, dihapus, atau file baru yang tidak dikenal) dicatat ke dalam `security.log` dan langsung ditampilkan di dashboard.

## Cara Penggunaan

### Prasyarat
- Python 3.x
- Flask

### Menjalankan Program

1.  **Membuat Baseline Awal**
    Perintah ini akan memindai semua file di `secure_files` dan menambahkannya ke baseline.
    ```bash
    python integrity_checker.py --add .
    ```

2.  **Menambahkan File Spesifik**:
    ```bash
    python integrity_checker.py --add file1.txt subfolder/file2.txt
    ```
    
3.  **Melihat Status File Saat Ini**:
    Perintah ini akan menampilkan status semua file (Aman, Diubah, Dihapus, Tidak Dilacak) di
    terminal.
    ```bash
    python integrity_checker.py --status
    ```

5.  **Menjalankan Monitoring Otomatis**
    Untuk pencatatan anomali ke security.log secara otomatis, buka terminal kedua dan jalankan:
    ```bash
    python integrity_checker.py --monitor 5
    ```
    
7.  **Menjalankan Dashboard Web**
    Setelah baseline diatur, jalankan server web untuk memulai pemantauan visual.
    ```bash
    python app.py
    ```

## Contoh Simulasi Serangan

1. **Lakukan “Serangan”**
   Ubah, hapus, atau tambahkan file baru di dalam folder `secure_files`.

2. **Amati Dashboard**
   Dashboard web akan **secara otomatis mendeteksi semua perubahan** (file diubah, dihapus, atau tidak dilacak) **tanpa perlu refresh**.

3. **Catat ke Log**
   Jalankan perintah berikut di terminal untuk mencatat anomali secara permanen:

   ```bash
   python integrity_checker.py --check
   ```

4. **Lihat Hasil Akhir**
   Kotak *Activity Log* pada dashboard akan otomatis **ter-update** dengan catatan anomali terbaru.


# Panduan Simulasi Serangan dan Deteksi

## LANGKAH 1: Persiapan dan Menjalankan Dashboard

1. Pastikan folder `secure_files` sudah berisi beberapa file, termasuk subfolder.
2. Jalankan server web di **Terminal 1**:
   ```bash
   python app.py
   ```
3. Buka **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.
   Pada tahap ini, semua file akan berstatus **“Tidak Dilacak”** karena baseline masih kosong.
   <img width="2512" height="1305" alt="image" src="https://github.com/user-attachments/assets/b47179a0-28c4-4a15-abac-ad0d08a24cd4" />

## LANGKAH 2: Menambahkan File ke Baseline

1. Buka **Terminal 2**.
2. Jalankan perintah berikut untuk melacak semua file:
   ```bash
   python integrity_checker.py --add .
   ```
   <img width="2116" height="356" alt="image" src="https://github.com/user-attachments/assets/b0eb68d4-f6ef-4707-9e9c-58ee643004f8" />
3. Refresh halaman dashboard.
   Semua file kini akan berstatus **“Aman”** (warna hijau).
   <img width="2493" height="1397" alt="Screenshot 2025-11-17 211738" src="https://github.com/user-attachments/assets/da39e03b-be2f-4fc9-bf56-976339db3a22" />

## LANGKAH 3: Melakukan “Serangan”

Lakukan perubahan pada folder `secure_files`:
* **Ubah File:** Modifikasi isi `data.txt`.
* **Hapus File:** Hapus `folder_penting/rahasia.txt`.
* **Tambah File Baru:** Buat file baru bernama `data3.txt`.

## LANGKAH 4: Mengamati Deteksi Real-time di Dashboard

Tanpa perlu refresh, dashboard akan otomatis memperbarui status:
* `data.txt` → **Diubah** (kuning)
* `folder_penting/rahasia.txt` → **Dihapus** (merah)
* `data3.txt` → **Tidak Dilacak** (abu-abu)

<img width="2512" height="1265" alt="Screenshot 2025-11-17 211821" src="https://github.com/user-attachments/assets/bbd341ab-9529-4558-b093-f4d689287ee1" />
<img width="2491" height="1137" alt="Screenshot 2025-11-17 211919" src="https://github.com/user-attachments/assets/a70c4756-cbda-4294-ba65-7d93555d6d8d" />
<img width="2642" height="1416" alt="Screenshot 2025-11-17 212435" src="https://github.com/user-attachments/assets/2cd8ae39-f5d3-42f2-a62f-4acb79457237" />
*Deskripsi: Dashboard mendeteksi perubahan secara otomatis tanpa perlu refresh.*




