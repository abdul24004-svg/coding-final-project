import sqlite3
import os
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# Pastikan folder database ada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "data.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ====== INIT DATABASE ======
conn = sqlite3.connect(DB_PATH)
conn.execute("""
    CREATE TABLE IF NOT EXISTS alat_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()

# ====== API TERIMA DATA DARI ARDUINO ======
@app.route("/api/update", methods=["POST"])
def update_status():
    data = request.get_json()
    status = data.get("status", 0)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO alat_status (status) VALUES (?)", (status,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated", "status": status})

# ====== DASHBOARD ======
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ====== HOME ======
@app.route("/")
def home():
    return redirect("/dashboard")

# ====== JALANKAN SERVER ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)