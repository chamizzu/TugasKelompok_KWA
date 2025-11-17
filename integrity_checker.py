import hashlib
import os
import json
from datetime import datetime
import sys
import time

MONITOR_DIR = "secure_files"
HASH_DB_FILE = "hash_db.json"
LOG_FILE = "security.log"

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
    """Mencatat aktivitas ke dalam file log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level_str = level.upper()
    log_entry = f"[{timestamp}] {level_str}: {message}"
    if filename:
        log_entry += f" File \"{filename}\""
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def scan_files_recursively(directory):
    """Memindai semua file di dalam direktori dan subdirektorinya."""
    scanned_files = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, directory).replace("\\", "/")
            scanned_files[relative_path] = calculate_hash(filepath)
    return scanned_files

def get_file_statuses():
    """
    Inti dari logika verifikasi. Fungsi ini MENGEMBALIKAN status file,
    bukan mencetaknya. Ini agar bisa dipakai oleh web dan CLI.
    """
    try:
        with open(HASH_DB_FILE, "r") as f:
            baseline_hashes = json.load(f)
    except FileNotFoundError:
        baseline_hashes = {}

    current_files = scan_files_recursively(MONITOR_DIR)
    
    all_known_files = set(baseline_hashes.keys()) | set(current_files.keys())
    
    statuses = []
    for filename in sorted(list(all_known_files)):
        status_info = {"file": filename, "status": "UNKNOWN", "status_class": "unknown"}
        
        # Cek apakah file ini ada di baseline
        is_tracked = filename in baseline_hashes
        # Cek apakah file ini ada di direktori sekarang
        is_present = filename in current_files
        
        if is_tracked and is_present:
            if baseline_hashes[filename] == current_files[filename]:
                status_info.update({"status": "Aman", "status_class": "ok"})
            else:
                status_info.update({"status": "Diubah", "status_class": "warning"})
        elif is_tracked and not is_present:
            status_info.update({"status": "Dihapus", "status_class": "alert"})
        elif not is_tracked and is_present:
            status_info.update({"status": "Tidak Dilacak", "status_class": "untracked"})
        
        statuses.append(status_info)
    return statuses

def add_to_baseline(files_to_add):
    """Menambahkan atau memperbarui file tertentu ke dalam baseline."""
    try:
        with open(HASH_DB_FILE, "r") as f:
            baseline_hashes = json.load(f)
    except FileNotFoundError:
        baseline_hashes = {}

    if not files_to_add:
        print("Error: Sebutkan nama file yang ingin ditambahkan.")
        return

    for filename in files_to_add:
        filepath = os.path.join(MONITOR_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Peringatan: File '{filename}' tidak ditemukan dan akan dilewati.")
            continue
        
        file_hash = calculate_hash(filepath)
        baseline_hashes[filename.replace("\\", "/")] = file_hash
        print(f"File '{filename}' ditambahkan/diperbarui ke baseline.")

    with open(HASH_DB_FILE, "w") as f:
        json.dump(baseline_hashes, f, indent=4)
    log_activity("info", f"{len(files_to_add)} file ditambahkan/diperbarui ke baseline.")

def run_check_and_log():
    """Menjalankan pengecekan dan mencatat hasilnya ke log."""
    statuses = get_file_statuses()
    anomalies_found = False
    
    log_activity("info", "--- Memulai Pengecekan dan Logging ---")

    for s in statuses:
        if s["status"] == "Diubah":
            log_activity("warning", "Integritas GAGAL! File telah diubah.", s["file"])
            anomalies_found = True
        elif s["status"] == "Dihapus":
            log_activity("warning", "Integritas GAGAL! File telah dihapus.", s["file"])
            anomalies_found = True
            
        elif s["status"] == "Tidak Dilacak":
            log_activity("alert", "File baru tidak dikenal terdeteksi.", s["file"])
            anomalies_found = True
    
    if not anomalies_found:
        log_activity("info", "Semua file yang dilacak aman dan tidak ada file baru yang terdeteksi.")

def run_monitor(interval=10):
    """Menjalankan pengecekan otomatis secara terus-menerus."""
    print(f"Memulai mode monitoring otomatis. Pengecekan setiap {interval} detik. (Tekan CTRL+C untuk berhenti)")
    while True:
        try:
            log_activity("info", "--- Memulai Pengecekan Otomatis ---")
            run_check_and_log()
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring dihentikan.")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan:")
        print("  python integrity_checker.py --add <file1> [file2] ...  (Menambahkan file ke baseline)")
        print("  python integrity_checker.py --status                  (Melihat status file saat ini)")
        print("  python integrity_checker.py --check                   (Mengecek dan mencatat anomali ke log)")
        print("  python integrity_checker.py --monitor [detik]         (Memonitor secara otomatis)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "--add":
        add_to_baseline(sys.argv[2:])
    elif command == "--status":
        for s in get_file_statuses():
            print(f"- {s['file']}: {s['status']}")
    elif command == "--check":
        run_check_and_log()
    elif command == "--monitor":
        try:
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            run_monitor(interval)
        except ValueError:
            print("Error: Interval harus berupa angka (detik).")
    else:
        print(f"Perintah tidak dikenal: {command}")