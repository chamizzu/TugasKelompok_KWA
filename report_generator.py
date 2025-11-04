# ==============================================================================
# report_generator.py (VERSI PERBAIKAN)
# Skrip untuk membaca security.log dan membuat laporan ringkas.
# ==============================================================================

LOG_FILE = "security.log"

def generate_report():
    """TUGAS #4: Membaca log dan menampilkan ringkasan (dengan parsing yang sudah diperbaiki)."""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File log '{LOG_FILE}' tidak ditemukan. Jalankan integrity_checker.py terlebih dahulu.")
        return

    # Menggunakan dictionary untuk menyimpan status TERAKHIR dari setiap file
    file_statuses = {} 
    last_anomaly_time = "Belum ada anomali terdeteksi."
    anomaly_levels = ["WARNING", "ALERT"]

    for line in lines:
        try:
            # Lewati baris yang tidak memiliki format yang kita harapkan
            if '] ' not in line or ': ' not in line:
                continue

            # CARA PARSING BARU YANG LEBIH ANDAL
            # 1. Pisahkan timestamp dari sisa baris
            timestamp_part, rest_of_line = line.split('] ', 1)
            timestamp = timestamp_part[1:]

            # 2. Pisahkan level dari pesan
            level, message = rest_of_line.split(': ', 1)
            
            filename = ""
            if '"' in message:
                filename = message.split('"')[1]

            # Hanya proses baris yang memiliki nama file
            if filename:
                if level == "INFO" and "OK" in message:
                    file_statuses[filename] = "Aman"
                elif level in anomaly_levels:
                    file_statuses[filename] = "Rusak/Anomali"
                    last_anomaly_time = timestamp
        
        except ValueError:
            # Jika terjadi error saat membelah string, lewati saja baris ini
            continue
            
    # Hitung jumlah file aman dan rusak dari status terakhir mereka
    total_safe = list(file_statuses.values()).count("Aman")
    total_corrupted = list(file_statuses.values()).count("Rusak/Anomali")

    print("\n--- Laporan Status Keamanan ---")
    print(f"Jumlah file yang aman        : {total_safe}")
    print(f"Jumlah file rusak/anomali    : {total_corrupted}")
    print(f"Waktu terakhir ada anomali   : {last_anomaly_time}")
    print("-------------------------------\n")

if __name__ == "__main__":
    generate_report()