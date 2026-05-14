# create_user.py - Interactive User Creator for AND ELECTRON Database
import sqlite3
import os

def create_new_user():
    """Interactive user creation"""
    
    print("\n" + "="*50)
    print("CREATE NEW USER")
    print("="*50)
    
    # Get user input
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    print("\nSelect role:")
    print("1. Admin (full access - can add/delete users)")
    print("2. Manager (can view and update message status)")
    print("3. Viewer (can only view messages)")
    
    role_choice = input("Enter choice (1/2/3): ").strip()
    
    if role_choice == '1':
        role = 'admin'
        role_desc = "Admin - Full Access"
    elif role_choice == '2':
        role = 'manager'
        role_desc = "Manager - View & Update"
    else:
        role = 'viewer'
        role_desc = "Viewer - Read Only"
    
    # Check if database exists
    if not os.path.exists('andelectron.db'):
        print("\n❌ Database not found!")
        print("Please run the website first: python app.py")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect('andelectron.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("\n❌ Users table not found!")
            print("Please run the website first to create the database.")
            conn.close()
            return
        
        # Insert user
        cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', (username, password, role))
        
        conn.commit()
        print(f"\n✅ User '{username}' created successfully!")
        print(f"   Role: {role_desc}")
        print(f"   Password: {password}")
        print("\n⚠️  Please change password after first login!")
        
    except sqlite3.IntegrityError:
        print(f"\n❌ Username '{username}' already exists!")
        print("Please choose a different username.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        conn.close()

def list_all_users():
    """Show all users"""
    if not os.path.exists('andelectron.db'):
        print("\n❌ Database not found!")
        return
    
    conn = sqlite3.connect('andelectron.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id, username, role FROM users')
        users = cursor.fetchall()
        
        if not users:
            print("\n📭 No users found in database.")
        else:
            print("\n" + "="*50)
            print("ALL REGISTERED USERS")
            print("="*50)
            for user in users:
                # Role display with emoji
                if user[2] == 'admin':
                    role_display = "👑 Admin"
                elif user[2] == 'manager':
                    role_display = "📋 Manager"
                else:
                    role_display = "👁️ Viewer"
                    
                print(f"ID: {user[0]} | Username: {user[1]} | Role: {role_display}")
            print("="*50)
    except Exception as e:
        print(f"\n❌ Error reading users: {e}")
    finally:
        conn.close()

def delete_user_interactive():
    """Delete user interactively"""
    if not os.path.exists('andelectron.db'):
        print("\n❌ Database not found!")
        return
    
    # First show current users
    list_all_users()
    
    username = input("\nEnter username to delete: ").strip()
    
    # Prevent deleting the default admin
    if username.lower() == 'admin':
        print("\n❌ Cannot delete the default 'admin' user!")
        print("This is the master administrator account.")
        return
    
    conn = sqlite3.connect('andelectron.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"\n✅ User '{username}' deleted successfully!")
    else:
        print(f"\n❌ User '{username}' not found")
    
    conn.close()

def change_password():
    """Change user password"""
    if not os.path.exists('andelectron.db'):
        print("\n❌ Database not found!")
        return
    
    username = input("\nEnter username: ").strip()
    new_password = input("Enter new password: ").strip()
    
    conn = sqlite3.connect('andelectron.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET password = ? WHERE username = ?', 
                   (new_password, username))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"\n✅ Password changed for '{username}'!")
    else:
        print(f"\n❌ User '{username}' not found")
    
    conn.close()

# Main menu
if __name__ == '__main__':
    while True:
        print("\n" + "="*50)
        print("👥 AND ELECTRON - USER MANAGEMENT SYSTEM")
        print("="*50)
        print("1. 📝 Create new user")
        print("2. 📋 List all users")
        print("3. 🗑️  Delete user")
        print("4. 🔑 Change password")
        print("5. 🚪 Exit")
        print("="*50)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            create_new_user()
            input("\nPress Enter to continue...")
        elif choice == '2':
            list_all_users()
            input("\nPress Enter to continue...")
        elif choice == '3':
            delete_user_interactive()
            input("\nPress Enter to continue...")
        elif choice == '4':
            change_password()
            input("\nPress Enter to continue...")
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter 1-5")
            input("\nPress Enter to continue...")