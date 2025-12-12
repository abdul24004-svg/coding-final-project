import sqlite3
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Render tanpa GUI
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file

app = Flask(__name__)

# ======== PATH DATABASE =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "data.db")


def get_data():
    """Ambil semua data dari DB sebagai list angka."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT status FROM alat_status ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()

    if rows:
        data = [row[0] for row in rows]
    else:
        data = []

    return data


@app.route('/')
def dashboard():
    data = get_data()

    if len(data) == 0:
        return render_template("dashboard.html",
                               minimum="N/A",
                               maximum="N/A",
                               rata2="N/A",
                               stdv="N/A"
                               )

    # Hitung statistik
    minimum = np.min(data)
    maximum = np.max(data)
    rata2 = round(np.mean(data), 2)
    stdv = np.std(data)

    return render_template("dashboard.html",
                           minimum=minimum,
                           maximum=maximum,
                           rata2=rata2,
                           stdv=stdv)


@app.route('/chart.png')
def line_chart():
    data = get_data()

    if len(data) == 0:
        data = [0]

    plt.figure(figsize=(10, 4))
    plt.plot(data, linewidth=2)
    plt.title("Grafik Intensitas Sensor (100 Data Terakhir)")
    plt.xlabel("Data ke-")
    plt.ylabel("Nilai Sensor")
    plt.tight_layout()

    chart_path = os.path.join(BASE_DIR, "chart.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype='image/png')


@app.route('/freq.png')
def freq_chart():
    data = get_data()

    if len(data) == 0:
        data = [0]

    plt.figure(figsize=(10, 4))
    plt.hist(data, bins=10, edgecolor="black")
    plt.title("Distribusi Frekuensi Data Sensor")
    plt.xlabel("Rentang Nilai")
    plt.ylabel("Frekuensi")
    plt.tight_layout()

    chart_path = os.path.join(BASE_DIR, "freq.png")
    plt.savefig(chart_path)
    plt.close()

    return send_file(chart_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)