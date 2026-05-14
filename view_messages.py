# view_messages.py - View customer messages from command line
import sqlite3
import os

def view_messages():
    """Display all customer messages from the database"""
    
    # Check if database exists
    if not os.path.exists('andelectron.db'):
        print("❌ Database not found!")
        print("Please run the website first (python app.py) and submit a test message.")
        return
    
    # Connect to database
    conn = sqlite3.connect('andelectron.db')
    cursor = conn.cursor()
    
    # Get all messages
    cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
    messages = cursor.fetchall()
    
    if not messages:
        print("📭 No messages found in database.")
        print("Submit a test message through the website contact form first.")
        conn.close()
        return
    
    # Display messages
    print("\n" + "="*60)
    print("📧 AND ELECTRON - Customer Messages")
    print("="*60)
    print(f"Total Messages: {len(messages)}\n")
    
    for msg in messages:
        print(f"📌 ID: {msg[0]}")
        print(f"   Name: {msg[1]}")
        print(f"   Email: {msg[2]}")
        print(f"   Phone: {msg[3]}")
        print(f"   Message: {msg[4][:100]}..." if len(msg[4]) > 100 else f"   Message: {msg[4]}")
        print(f"   Status: {msg[5]}")
        print(f"   Received: {msg[6]}")
        print("-"*40)
    
    # Show statistics
    cursor.execute('SELECT status, COUNT(*) FROM contacts GROUP BY status')
    stats = cursor.fetchall()
    print("\n📊 Statistics:")
    for status, count in stats:
        print(f"   {status}: {count}")
    
    conn.close()

# Run the function
if __name__ == '__main__':
    view_messages()