import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path='bot_database.db'):
        # Ensure the directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create the necessary tables if they don't exist."""
        # Profile table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            phone TEXT,
            verified BOOLEAN,
            is_bot BOOLEAN,
            mutual_contact BOOLEAN,
            restricted BOOLEAN,
            photo_path TEXT,
            last_updated TIMESTAMP
        )
        ''')
        
        # Chats table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER UNIQUE,
            chat_name TEXT,
            chat_type TEXT,
            username TEXT,
            is_group BOOLEAN,
            is_channel BOOLEAN,
            member_count INTEGER,
            description TEXT,
            last_updated TIMESTAMP
        )
        ''')
        
        # Messages table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            message_id INTEGER,
            chat_id INTEGER,
            sender_id INTEGER,
            message_text TEXT,
            timestamp TIMESTAMP,
            is_outgoing BOOLEAN,
            FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
        )
        ''')
        
        self.conn.commit()
    
    def update_profile(self, profile_data):
        """Update or insert profile information."""
        self.cursor.execute('''
        INSERT OR REPLACE INTO profile (
            user_id, first_name, last_name, username, phone, verified, 
            is_bot, mutual_contact, restricted, photo_path, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile_data.get('user_id'),
            profile_data.get('first_name'),
            profile_data.get('last_name'),
            profile_data.get('username'),
            profile_data.get('phone'),
            profile_data.get('verified'),
            profile_data.get('is_bot'),
            profile_data.get('mutual_contact'),
            profile_data.get('restricted'),
            profile_data.get('photo_path'),
            datetime.now()
        ))
        self.conn.commit()
    
    def update_chat(self, chat_data):
        """Update or insert chat information."""
        self.cursor.execute('''
        INSERT OR REPLACE INTO chats (
            chat_id, chat_name, chat_type, username, is_group, 
            is_channel, member_count, description, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chat_data.get('chat_id'),
            chat_data.get('chat_name'),
            chat_data.get('chat_type'),
            chat_data.get('username'),
            chat_data.get('is_group'),
            chat_data.get('is_channel'),
            chat_data.get('member_count'),
            chat_data.get('description'),
            datetime.now()
        ))
        self.conn.commit()
    
    def store_message(self, message_data):
        """Store message information."""
        self.cursor.execute('''
        INSERT INTO messages (
            message_id, chat_id, sender_id, message_text, timestamp, is_outgoing
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            message_data.get('message_id'),
            message_data.get('chat_id'),
            message_data.get('sender_id'),
            message_data.get('message_text'),
            message_data.get('timestamp', datetime.now()),
            message_data.get('is_outgoing')
        ))
        self.conn.commit()
    
    def get_profile(self):
        """Retrieve profile information."""
        self.cursor.execute('SELECT * FROM profile')
        return self.cursor.fetchone()
    
    def get_chats(self):
        """Retrieve all chats."""
        self.cursor.execute('SELECT * FROM chats')
        return self.cursor.fetchall()
    
    def get_messages(self, chat_id=None, limit=100):
        """Retrieve messages for a specific chat or all messages."""
        if chat_id:
            self.cursor.execute('SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?', (chat_id, limit))
        else:
            self.cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?', (limit,))
        return self.cursor.fetchall()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
