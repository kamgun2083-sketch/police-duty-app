import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = 'sec'
DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'duty_records.db')
def get_db():
    conn = sqlite3.connect(DATABASE); conn.row_factory = sqlite3.Row; return conn
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = get_db(); conn.execute('INSERT INTO duty_log (date_logged, shift, rank_name, batch_team, location, duty_type, time_duration, weapons, achievements, remarks) VALUES (?,?,?,?,?,?,?,?,?,?)', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.form.get('shift'), request.form.get('rank_name'), request.form.get('batch_team'), request.form.get('location'), request.form.get('duty_type'), request.form.get('time_duration'), request.form.get('weapons'), request.form.get('achievements'), request.form.get('remarks'))); conn.commit(); conn.close(); flash('सफलतापूर्वक दर्ता भयो।', 'success')
    return render_template('form.html')
@app.route('/dashboard')
def dashboard():
    conn = get_db(); r = conn.execute('SELECT * FROM duty_log ORDER BY id DESC').fetchall(); conn.close(); return render_template('dashboard.html', records=r)
if __name__ == '__main__':
    c = get_db(); c.execute('CREATE TABLE IF NOT EXISTS duty_log (id INTEGER PRIMARY KEY AUTOINCREMENT, date_logged TEXT, shift TEXT, rank_name TEXT, batch_team TEXT, location TEXT, duty_type TEXT, time_duration TEXT, weapons TEXT, achievements TEXT, remarks TEXT)'); c.commit(); c.close()
    app.run(host='0.0.0.0', port=5000, debug=True)
