# 🛡️ HoneyPhish: Advanced C2 & Forensic Infrastructure

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **A custom-engineered Command & Control (C2) framework designed for Red Team engagements, security awareness training, and network forensic analysis.**

---

## 📖 Project Overview
**HoneyPhish** is a lightweight, modular C2 infrastructure built to simulate advanced credential harvesting attacks. Unlike static phishing tools, HoneyPhish utilizes a dynamic **Python/Flask** backend to handle session management, real-time data exfiltration, and forensic device fingerprinting.

The primary engineering goal of this project was to solve the **"Reverse Proxy Masking"** problem, enabling the extraction of true client IP addresses (IPv6/IPv4) even when traffic is tunneled through services like Ngrok or Cloudflare.

### 🎯 Key Capabilities
* **True Source IP Resolution:** Implements advanced HTTP header parsing (`X-Forwarded-For`, `Real-IP`) to identify victim origin addresses behind reverse proxies, successfully capturing **IPv6 addresses** from mobile carrier networks (4G/5G).
* **High-Fidelity Simulation:** Features pixel-perfect, responsive frontend templates designed to mimic corporate authentication portals (SSO/SaaS) for realistic user behavior analysis.
* **Forensic Telemetry:** distinct logging of `User-Agent` strings, screen resolution, and device type (Mobile vs. Desktop) stored in a structured **SQLite** database.
* **Live C2 Dashboard:** A dark-mode, responsive command center for real-time monitoring of captured sessions and active targets.

---

## 📸 Interface Preview

### 1. The Command Center (Admin Dashboard)!
![Dashboard](https://github.com/user-attachments/assets/731480ef-d566-4f36-8ff7-1a3babe50a8d)

*Real-time monitoring of incoming connections and captured credentials.*
![Dashboard Preview](https://github.com/ekaschhhabra/The_Exploiters_Hackhathon2025/blob/main/assets/dashboard_preview.png?raw=true)


### 2. Mobile Attack Vector
*Responsive login simulation deployed via secure tunnel.*
![Mobile Preview](https://github.com/ekaschhhabra/The_Exploiters_Hackhathon2025/blob/main/assets/mobile_preview.png?raw=true)
<img width="317" height="707" alt="Screenshot 2026-01-05 210915" src="https://github.com/user-attachments/assets/ae1c01b4-299b-433b-9c3d-5ef4709873b2" />

## 🛠️ Technical Architecture

### Tech Stack
* **Backend:** Python 3 (Flask, Jinja2)
* **Database:** SQLite3 (Lightweight, serverless persistence)

* **Frontend:** HTML5, CSS3 (Modern Flexbox/Grid layouts)
* **Tunneling:** Compatible with Ngrok, Serveo, or Cloudflared

### Forensic Logic (Code Snippet)
*How HoneyPhish resolves the true victim IP behind a proxy:*

```python
def get_client_ip():
    # Priority check for X-Forwarded-For to bypass Ngrok masking
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr
