# ==============================================================================
# integrity_checker.py
# Skrip utama untuk membuat baseline dan memverifikasi integritas file.
# ==============================================================================

# BAGIAN 1: IMPORT MODUL
import hashlib
import os
import json
from datetime import datetime
import sys

# BAGIAN 2: KONFIGURASI
MONITOR_DIR = "secure_files"    # Folder yang akan dipantau
HASH_DB_FILE = "hash_db.json"   # File database untuk menyimpan hash baseline
LOG_FILE = "security.log"       # File untuk mencatat semua aktivitas

# BAGIAN 3: FUNGSI-FUNGSI PENDUKUNG

def calculate_hash(filepath):
    """Menghitung hash SHA-256 dari sebuah file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def log_activity(level, message, filename=""):
    """Mencatat aktivitas ke dalam file log dengan format yang ditentukan."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Level diubah menjadi huruf besar sesuai permintaan soal
    level_str = level.upper()
    log_entry = f"[{timestamp}] {level_str}: {message}"
    if filename:
        # Format "File "nama.file"" sesuai permintaan soal
        log_entry += f" File \"{filename}\""
    
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

# BAGIAN 4: FUNGSI-FUNGSI INTI

def create_baseline():
    """TUGAS #2.1: Membuat dan menyimpan baseline hash dari semua file di folder."""
    baseline_hashes = {}
    print(f"Membuat baseline untuk folder '{MONITOR_DIR}'...")
    
    if not os.path.isdir(MONITOR_DIR):
        log_activity("alert", f"Folder '{MONITOR_DIR}' tidak ditemukan! Membuat folder baru.")
        os.makedirs(MONITOR_DIR)

    for filename in os.listdir(MONITOR_DIR):
        filepath = os.path.join(MONITOR_DIR, filename)
        if os.path.isfile(filepath):
            file_hash = calculate_hash(filepath)
            baseline_hashes[filename] = file_hash
            print(f"  - Menghitung hash untuk {filename}")

    with open(HASH_DB_FILE, "w") as f:
        json.dump(baseline_hashes, f, indent=4)
    log_activity("info", f"Baseline berhasil dibuat dan disimpan di '{HASH_DB_FILE}'")

def verify_integrity():
    """TUGAS #1 & #2.2: Memverifikasi integritas file berdasarkan baseline."""
    log_activity("info", "Memulai pengecekan integritas...")
    try:
        with open(HASH_DB_FILE, "r") as f:
            baseline_hashes = json.load(f)
    except FileNotFoundError:
        log_activity("alert", f"File baseline '{HASH_DB_FILE}' tidak ditemukan. Jalankan mode --init terlebih dahulu.")
        return

    current_files = {filename: calculate_hash(os.path.join(MONITOR_DIR, filename)) 
                     for filename in os.listdir(MONITOR_DIR) 
                     if os.path.isfile(os.path.join(MONITOR_DIR, filename))}

    all_files = set(baseline_hashes.keys()) | set(current_files.keys())

    for filename in sorted(list(all_files)):
        # KASUS 1: File diubah
        if filename in baseline_hashes and filename in current_files:
            if baseline_hashes[filename] != current_files[filename]:
                log_activity("warning", "Integritas GAGAL! File telah diubah.", filename)
            else:
                log_activity("info", "Verifikasi OK.", filename)
        # KASUS 2: File dihapus
        elif filename in baseline_hashes and filename not in current_files:
            log_activity("warning", "Integritas GAGAL! File telah dihapus.", filename)
        # KASUS 3: File ditambahkan
        elif filename not in baseline_hashes and filename in current_files:
            log_activity("alert", "File tidak dikenal terdeteksi.", filename)
            
    log_activity("info", "Pengecekan integritas selesai.")

# BAGIAN 5: "OTAK" PROGRAM
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "--init":
            create_baseline()
        elif command == "--check":
            verify_integrity()
        else:
            print(f"Perintah tidak dikenal: {command}. Gunakan '--init' atau '--check'")
    else:
        print("Penggunaan:")
        print("  python integrity_checker.py --init    (Untuk membuat baseline awal)")
        print("  python integrity_checker.py --check   (Untuk memeriksa integritas file)")