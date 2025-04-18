from telethon import TelegramClient, events, sync, types
import sys
import os
import asyncio
from datetime import datetime

# Add parent directory to path to import from other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_ID, API_HASH, PHONE_NUMBER
from database.database import Database

async def main():
    # Initialize database
    db = Database('bot_database.db')
    
    # Create the client and connect
    print(f"Connecting to Telegram with API_ID: {API_ID}")
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    
    # Ensure you're connected
    if await client.is_user_authorized():
        print("Successfully connected!")
    else:
        print("Failed to authenticate. Please check your credentials.")
        db.close()
        return
    
    # Get information about yourself
    me = await client.get_me()
    
    # Store profile information
    profile_photo_path = None
    profile_photo = await client.download_profile_photo('me', file='profile_photo.jpg')
    if profile_photo:
        profile_photo_path = str(profile_photo)
        print(f"Profile photo saved as: {profile_photo_path}")
    
    profile_data = {
        'user_id': me.id,
        'first_name': me.first_name,
        'last_name': me.last_name,
        'username': me.username,
        'phone': me.phone,
        'verified': me.verified,
        'is_bot': me.bot,
        'mutual_contact': me.mutual_contact,
        'restricted': me.restricted,
        'photo_path': profile_photo_path
    }
    
    db.update_profile(profile_data)
    print("\nProfile Information stored in database:")
    print(f"ID: {me.id}")
    print(f"Name: {me.first_name} {me.last_name if me.last_name else ''}")
    print(f"Username: @{me.username if me.username else 'N/A'}")
    
    # Get and store chat information
    print("\nRetrieving chat information...")
    async for dialog in client.iter_dialogs(limit=50):
        chat = dialog.entity
        chat_data = {
            'chat_id': dialog.id,
            'chat_name': dialog.name,
            'chat_type': 'private' if isinstance(chat, types.User) else 
                        'group' if isinstance(chat, types.Chat) else 
                        'channel' if isinstance(chat, types.Channel) else 'unknown',
            'username': getattr(chat, 'username', None),
            'is_group': isinstance(chat, types.Chat) or (isinstance(chat, types.Channel) and chat.megagroup),
            'is_channel': isinstance(chat, types.Channel) and not chat.megagroup,
            'member_count': getattr(chat, 'participants_count', None),
            'description': getattr(chat, 'about', None)
        }
        
        db.update_chat(chat_data)
    
    print(f"Stored {len(await client.get_dialogs(limit=50))} chats in database")
    
    # Store recent messages from each chat
    print("\nStoring recent messages...")
    message_count = 0
    async for dialog in client.iter_dialogs(limit=20):
        async for message in client.iter_messages(dialog, limit=10):
            if message.text:  # Only store text messages
                message_data = {
                    'message_id': message.id,
                    'chat_id': dialog.id,
                    'sender_id': message.sender_id,
                    'message_text': message.text,
                    'timestamp': message.date,
                    'is_outgoing': message.out
                }
                db.store_message(message_data)
                message_count += 1
    
    print(f"Stored {message_count} messages in database")
    
    # Close connections
    await client.disconnect()
    db.close()
    print("\nDatabase updated successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
