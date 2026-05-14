AND ELECTRON - Complete README File

# ⚡ AND ELECTRON - Industrial Energy Solutions Website

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-2.0+-green)
![Database](https://img.shields.io/badge/database-SQLite-orange)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [How to Run the Application](#how-to-run-the-application)
- [Accessing the Website](#accessing-the-website)
- [Admin Dashboard](#admin-dashboard)
- [User Management](#user-management)
- [Database Management](#database-management)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## 🎯 Project Overview

**AND ELECTRON** is a professional business website for an industrial energy solutions company. The website showcases products, handles customer inquiries, and provides an admin dashboard for managing messages.

### Company Information
- **Founded:** 2021
- **Industry:** Industrial Batteries, Solar Solutions, Material Handling Equipment
- **Expertise:** 20+ years of industry experience
- **Services:** Sales, Service, Rentals, AMC

---

## ✨ Features

### Customer Features
- ✅ Responsive, mobile-friendly design
- ✅ 6 product categories with detailed pages
- ✅ Contact form with database storage
- ✅ Company information and statistics
- ✅ Partner and client showcase
- ✅ PDF brochure download

### Admin Features
- ✅ Secure admin login system
- ✅ View all customer inquiries
- ✅ Update message status (Pending/In Progress/Replied)
- ✅ Delete old messages
- ✅ Add/Manage admin users
- ✅ Real-time statistics dashboard

### Technical Features
- ✅ SQLite database integration
- ✅ Flask backend framework
- ✅ RESTful API endpoints
- ✅ Session management
- ✅ Cross-platform compatibility

---

## 💻 System Requirements

### Minimum Requirements
| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 10/11, macOS, or Linux |
| RAM | 4GB (8GB recommended) |
| Disk Space | 500MB free |
| Python | 3.8 or higher |
| Browser | Chrome/Firefox/Edge (latest) |

### Software to Install
1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Flask** - Install via pip
3. **SQLite** - Built-in with Python

---

## 🚀 Quick Installation

### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Click "Install Now"

**Verify installation:**
```bash
python --version
Step 2: Install Flask
Open Command Prompt/Terminal and run:

bash
pip install flask
If you get an error:

bash
python -m pip install flask
Step 3: Download Project Files
Create the following folder structure:

text
AND ELECTRON/
│
├── app.py
├── create_user.py (optional)
├── view_messages.py (optional)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── product_detail.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
└── static/
    └── style.css
Copy all the code files into their respective locations.

🏃 How to Run the Application
Method 1: Using VS Code (Recommended)
Open VS Code

Open project folder: File → Open Folder → Select AND ELECTRON

Open terminal: Ctrl + `

Run the app:

bash
python app.py
Ctrl + Click on http://localhost:5000/

Method 2: Using Command Prompt

Windows:

bash
cd C:\Users\godab\OneDrive\Desktop\AND ELECTRON
python app.py

macOS/Linux:

bash
cd /path/to/AND\ ELECTRON
python3 app.py

Main Access Links
Page	URL	Description
🏠 Homepage	http://localhost:5000	Main company website
🔐 Admin Login	http://localhost:5000/admin/login	Admin dashboard access

Product Direct Links
Product	URL
Industrial Batteries	http://localhost:5000/product/1
Zapi & Chloride Chargers	http://localhost:5000/product/2
Solar Power Systems	http://localhost:5000/product/3
Material Handling Equipment	http://localhost:5000/product/4
Data Center Batteries	http://localhost:5000/product/5
Power Backup Solutions	http://localhost:5000/product/6

Quick Navigation
Products Section: http://localhost:5000/#products
Contact Section: http://localhost:5000/#contact
About Section: http://localhost:5000/#about

🔐 Admin Dashboard
Default Login Credentials

Field	Value
Username	admin
Password	admin123

Accessing Admin Dashboard
Go to: http://localhost:5000/admin/login
Enter username and password
Click "Login"

Dashboard Features
Feature	Description
Statistics Cards	Total messages, pending, replied counts
Messages Table	All customer inquiries with details
Status Dropdown	Change message status
View Button	See full message content
Delete Button	Remove old messages
Auto-Refresh	Updates every 30 seconds

Message Status Types
Status	Meaning
🟡 Pending	New message, not yet responded
🔵 In Progress	Currently working on response
🟢 Replied	Customer has been contacted

👥 User Management
Adding New Users

Method 1: Using VS/terminal
Run it:

bash
python create_user.py 

Method 2: Direct SQL

bash
go to database ----> sqlite3 andelectron.db
INSERT INTO users (username, password, role) VALUES ('newuser', 'pass123', 'manager');
.quit

User Roles
Role	Permissions
Admin	Full access - can add/delete users, all dashboard features
Manager	Can view and update message status
Viewer	Can only view messages (read-only)

Changing Passwords
sql
-- In SQLite
UPDATE users SET password = 'newpassword' WHERE username = 'username';

🗄️ Database Management
Database Location
C:\Users\godab\OneDrive\Desktop\AND ELECTRON\andelectron.db

Database Schema
contacts table (customer messages)

Column	Type	Description
id	INTEGER	Auto-increment ID
name	TEXT	Customer name
email	TEXT	Customer email
phone	TEXT	Customer phone
message	TEXT	Their inquiry
status	TEXT	pending/inprogress/replied
created_at	TIMESTAMP	Submission time
replied_at	TIMESTAMP	Response time
notes	TEXT	Admin notes

users table (admin accounts)

Column	Type	Description
id	INTEGER	Auto-increment ID
username	TEXT	Login username
password	TEXT	Login password
role	TEXT	admin/manager/viewer

Viewing Database Contents
Method 1: Admin Dashboard (Easiest)

Login at http://localhost:5000/admin/login

Method 2: Command Line
bash
sqlite3 andelectron.db
SELECT * FROM contacts;
.quit

🛠️ Troubleshooting
Common Issues and Solutions
Problem	Solution
'python' not recognized	Reinstall Python and check "Add to PATH"
Flask not found	Run pip install flask
Port 5000 already in use	Change port in app.py: port=5001
Database locked error	Close DB Browser or stop other programs using the database
Can't find andelectron.db	Run python app.py first - it creates the database
Admin login fails	Use username: admin, password: admin123
Images not showing	Add images to static/images/ folder
Form not submitting	Check Flask is running (look for terminal output)
CSS not loading	Check that style.css is in static/ folder

Port Already in Use - Fix
Edit the last line of app.py:

python
# Change from:
app.run(debug=True, host='0.0.0.0', port=5000)

# To:
app.run(debug=True, host='0.0.0.0', port=5001)
Then access at: http://localhost:5001

🔒 Security Recommendations
For production deployment:
Change default admin password immediately
Implement password hashing (use bcrypt or SHA256)
Use environment variables for sensitive data
Enable HTTPS in production
Regular database backups
Limit login attempts to prevent brute force
Use strong passwords (min 8 chars, mix of letters/numbers/symbols)