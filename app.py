from flask import Flask, render_template, jsonify

# Import fungsi logika dari skrip utama kita!
from integrity_checker import get_file_statuses

app = Flask(__name__)

LOG_FILE = "security.log"

def get_security_logs(limit=20):
    """Membaca beberapa baris terakhir dari file log."""
    try:
        with open(LOG_FILE, "r") as f:
            # Baca semua baris, ambil 'limit' baris terakhir, lalu balik urutannya
            lines = f.readlines()
            return lines[-limit:][::-1]
    except FileNotFoundError:
        return [f"File log '{LOG_FILE}' tidak ditemukan."]

@app.route('/')
def home():
    """Menampilkan halaman utama dengan daftar status file."""
    statuses = get_file_statuses()
    return render_template('index.html', files=statuses)

@app.route('/api/status')
def api_status():
    """Menyediakan data status file dalam format JSON."""
    statuses = get_file_statuses()
    return jsonify(statuses)

# === INI BAGIAN BARU YANG DITAMBAHKAN ===
@app.route('/api/logs')
def api_logs():
    """Menyediakan data log dalam format JSON."""
    logs = get_security_logs()
    return jsonify(logs)
# === AKHIR BAGIAN BARU ===

if __name__ == '__main__':
    app.run(debug=True)