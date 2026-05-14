from flask import Flask, render_template, request, jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'andelectron_secret_key_2026'

# Database setup
DATABASE = 'andelectron.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            replied_at TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Create users table for admin login (optional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    
    # Insert default admin user (change password after first login)
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Initialize database when app starts
init_db()

# Complete Product Data based on your catalog
products = [
    {
        "id": 1,
        "name": "Industrial Batteries",
        "short_desc": "High-performance lead-acid & lithium-ion batteries for industrial applications.",
        "full_desc": "Industrial batteries designed for maximum reliability and efficiency in demanding environments.",
        "image": "industrial_battery.jpg",
        "details": [
            {
                "title": "Lead-Acid Batteries",
                "image": "leadacid.jpg",
                "content": [
                    "One of the oldest and most widely used industrial battery types",
                    "Types: Flooded, VRLA & GEL Lead Acid Batteries",
                    "Applications: Forklifts, VNA, Reach trucks, Pallet trucks, Electric Stackers, Tow Trucks",
                    "Voltage Range: 24V, 36V, 48V, 72V, 80V",
                    "Capacity: 160Ah – 930Ah (max 1500Ah)",
                    "Make: EXIDE Industries Limited"
                ]
            },
            {
                "title": "Lithium-Ion Batteries",
                "image": "lithium.jpg",
                "content": [
                    "High energy density, longer lifespan, lightweight design",
                    "Types: LiFePO4 (LFP) & NMC (LiNiMnCoO2)",
                    "Applications: Forklifts, VNA, Reach trucks, Electric vehicles, Renewable energy storage",
                    "Voltage Range: 24V, 36V, 48V, 72V, 80V",
                    "Capacity: 160Ah to 1500Ah",
                    "Make: EXIDE & AMARON"
                ]
            }
        ]
    },
    {
        "id": 2,
        "name": "Zapi & Chloride Chargers",
        "short_desc": "High-efficiency industrial charging solutions for electric vehicles and critical infrastructure.",
        "full_desc": "Advanced charging systems from ZAPI GROUP and Chloride for industrial and commercial applications.",
        "image": "charger.jpg",
        "details": [
            {
                "title": "ZAPI Group Chargers",
                "image": "zapi_charger.jpg",
                "content": [
                    "High-efficiency, durable on-board and off-board chargers",
                    "Power Range: 350W to 36kW",
                    "High-Voltage Solutions: 7.2 kW to 22 kW liquid-cooled for 400V & 800V battery packs",
                    "Compact & Durable: Sealed, vibration-proof for harsh environments",
                    "Applications: Agriculture, construction, e-mobility, material handling, robotics",
                    "Models: Delta-Q XV3300 (3-in-1 solution), ZIVAN SG9 (9kW portable fast charger)"
                ]
            },
            {
                "title": "Chloride Chargers",
                "image": "chloride_charger.jpg",
                "content": [
                    "High-reliability industrial DC chargers for critical infrastructure",
                    "Applications: Industrial UPS systems, safety lighting, standby power backup",
                    "Types: Small DC chargers, ATEX/IECEx certified for hazardous areas",
                    "Features: Boost function for voltage increase, automatic battery testing",
                    "Range: <900W to large systems supporting 12V, 24V, 48V, 110-127Vdc",
                    "Manufacturing: CBSEA Singapore & Exide Industries India"
                ]
            }
        ]
    },
    {
        "id": 3,
        "name": "Solar Power Systems",
        "short_desc": "Complete renewable energy solutions from 1KW to 10MW for industrial & commercial use.",
        "full_desc": "Sustainable solar energy systems designed to reduce carbon footprint and energy costs.",
        "image": "solar_system.jpg",
        "details": [
            {
                "title": "Solar PV Systems",
                "image": "solar_panel.jpg",
                "content": [
                    "Grid-Connected & Off-Grid PV Systems",
                    "Applications: Solar street lights, Industrial & Commercial Solar Plants",
                    "Capacity Range: 1KW to 10MW",
                    "Textile Industry: High rooftop space for panel deployment",
                    "Cement & Steel: High energy consumption sectors benefit from solar",
                    "Agriculture: Solar-powered pumps and processing units",
                    "Logistics & Warehousing: Utilizing vast flat rooftops",
                    "Make: WAAREE Energies & EXIDE"
                ]
            }
        ]
    },
    {
        "id": 4,
        "name": "Material Handling Equipment",
        "short_desc": "Complete range of battery-operated and manual material handling solutions.",
        "full_desc": "Efficient material handling equipment for warehouses, factories, and logistics centers.",
        "image": "mhe.jpg",
        "details": [
            {
                "title": "Battery-Operated MHE",
                "image": "electric_forklift.jpg",
                "content": [
                    "Electric Forklifts",
                    "Electric Pallet Jacks",
                    "Electric Reach Trucks",
                    "Electric Stackers",
                    "Electric Tow Tractors",
                    "Electric Pallet Trucks with Scales",
                    "Electric Conveyor Systems",
                    "Range: 50Kg to 10T capacity"
                ]
            },
            {
                "title": "Manual MHE",
                "image": "manual_mhe.jpg",
                "content": [
                    "Hand Trucks & Dollies",
                    "Pallet Jacks",
                    "Wheelbarrows",
                    "Manual Trolleys",
                    "Manual Lifts",
                    "Make: Godrej & other leading brands"
                ]
            }
        ]
    },
    {
        "id": 5,
        "name": "Data Center Batteries",
        "short_desc": "High-performance UPS batteries for critical IT infrastructure and data centers.",
        "full_desc": "Specialized battery solutions ensuring uninterrupted power for modern data centers.",
        "image": "datacenter_battery.jpg",
        "details": [
            {
                "title": "Lithium-Ion for Data Centers",
                "image": "lithium_dc.jpg",
                "content": [
                    "Industry standard for new high-density data centers",
                    "Smaller footprint (20-40% smaller than traditional)",
                    "Longer service life: 7+ years",
                    "Faster charging times",
                    "Types: LFP (high reliability) & NCM (high energy density)",
                    "Advanced BMS for monitoring and safety"
                ]
            },
            {
                "title": "VRLA & Specialized Batteries",
                "image": "vrla_battery.jpg",
                "content": [
                    "Valve-Regulated Lead-Acid - reliable, cost-effective",
                    "High power at high-rate discharge",
                    "Front terminal batteries for space optimization",
                    "Nickel-Cadmium for harsh environments",
                    "Nickel-Zinc as safer, higher-density alternative",
                    "Future Tech: Solid-state batteries emerging",
                    "Compliance: UL94-V0 fire safety standards"
                ]
            }
        ]
    },
    {
        "id": 6,
        "name": "Power Backup Solutions",
        "short_desc": "Complete backup power infrastructure for uninterrupted business operations.",
        "full_desc": "Comprehensive power backup solutions for homes, businesses, and industrial facilities.",
        "image": "power_backup.jpg",
        "details": [
            {
                "title": "UPS Systems & Backup",
                "image": "ups_system.jpg",
                "content": [
                    "Industrial UPS Systems",
                    "Home Inverter Solutions",
                    "Diesel Generator Integration",
                    "Solar Hybrid Backup Systems",
                    "Voltage Stabilizers & AVR",
                    "Custom capacity solutions",
                    "24/7 Technical Support",
                    "Annual Maintenance Contracts available"
                ]
            }
        ]
    }
]

# Partners data
partners = [
    {"name": "Exide Industries Limited", "logo": "exide.png", "desc": "Leading battery manufacturer"},
    {"name": "Zapi Group", "logo": "zapi.png", "desc": "Advanced motion controls & chargers"},
    {"name": "Waaree Energies", "logo": "waaree.png", "desc": "Solar PV modules & EPC"},
    {"name": "Amaron", "logo": "amaron.png", "desc": "VRLA & Lithium batteries"},
    {"name": "Godrej", "logo": "godrej.png", "desc": "Material handling equipment"},
    {"name": "Chloride", "logo": "chloride.png", "desc": "Industrial DC chargers"}
]

# Clients data
clients = [
    "AMNS", "Pidilite", "ITC", "Pfizer", 
    "Snowman", "Blue Star", "L&T", "Tata Motors",
    "Reliance Industries", "Adani Group"
]

@app.route('/')
def home():
    return render_template('index.html', products=products, partners=partners, clients=clients)

@app.route('/product/<int:id>')
def product_detail(id):
    product = next((p for p in products if p["id"] == id), None)
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # Validate input
        if not all([name, email, phone]):
            return jsonify({"status": "error", "message": "Please fill all required fields."}), 400
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, message, status, created_at)
            VALUES (?, ?, ?, ?, 'pending', ?)
        ''', (name, email, phone, message, datetime.now()))
        
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Print to console for debugging
        print("=" * 50)
        print(f"New Contact Form Submission - ID: {contact_id}")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Message: {message}")
        print("=" * 50)
        
        # Optional: Send email notification
        """
        # Uncomment to send email notifications
        send_email_notification(name, email, phone, message)
        """
        
        return jsonify({
            "status": "success", 
            "message": "Thank you! We have received your inquiry. Our team will contact you within 24 hours.",
            "contact_id": contact_id
        })
        
    except Exception as e:
        print(f"Error saving contact: {str(e)}")
        return jsonify({"status": "error", "message": "Something went wrong. Please try again."}), 500

# Admin routes to view and manage contacts
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # In production, use session management
            return render_template('admin_dashboard.html', contacts=get_all_contacts())
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    
    return render_template('admin_login.html')

@app.route('/admin/contacts')
def get_all_contacts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
    contacts = cursor.fetchall()
    conn.close()
    return [dict(contact) for contact in contacts]

@app.route('/admin/update_status/<int:contact_id>', methods=['POST'])
def update_contact_status(contact_id):
    status = request.json.get('status')
    notes = request.json.get('notes', '')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contacts 
        SET status = ?, notes = ?, replied_at = ? 
        WHERE id = ?
    ''', (status, notes, datetime.now(), contact_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

@app.route('/admin/delete_contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

def send_email_notification(name, email, phone, message):
    """Send email notification (configure with your SMTP settings)"""
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "your_email@gmail.com"  # Replace with your email
        smtp_password = "your_password"  # Replace with your password
        
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = "sales@andelectron.in"
        msg['Subject'] = f"New Contact Form Submission from {name}"
        
        body = f"""
        New inquiry received:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        
        Please respond within 24 hours.
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print("Email notification sent")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)