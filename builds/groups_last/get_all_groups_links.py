from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, ChatForbidden
import pandas as pd

# 🔹 Your API credentials
api_id = 25146169
api_hash = 'a266dde03d03ab4af7df4e7021afb55c'
phone_number = '+380504144151'  # Replace with your phone number

# 🔹 Initialize Telegram Client
client = TelegramClient("session_name", api_id, api_hash)

async def get_user_groups():
    await client.start(phone_number)  # Log in to Telegram

    # 🔹 Fetch all dialogs (chats, groups, channels)
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,  # Increase limit if needed
        hash=0
    ))

    group_list = []

    for chat in dialogs.chats:
        try:
            # Skip forbidden groups (banned/removed)
            if isinstance(chat, ChatForbidden):
                print(f"🚫 No access to {chat.id}, skipping...")
                continue

            # Check if it's a group or channel
            is_group = getattr(chat, "megagroup", False)
            is_channel = getattr(chat, "broadcast", False)

            if is_group or is_channel:
                group_list.append({
                    "Group Name": chat.title,
                    "Group ID": chat.id,
                    "Type": "Supergroup" if is_group else "Channel",
                    "Access": "Public" if getattr(chat, "username", None) else "Private",
                    "Link": f"https://t.me/{chat.username}" if getattr(chat, "username", None) else "🔒 Private"
                })

                print(f"✅ Found: {chat.title} (ID: {chat.id})")

        except Exception as e:
            print(f"❌ Error retrieving info for chat {chat.id}: {e}")

    # 🔹 Save to CSV
    df = pd.DataFrame(group_list)
    df.to_csv("telegram_groups.csv", index=False)

    print(f"✅ Successfully saved {len(group_list)} groups/channels to 'telegram_groups.csv'.")

    await client.disconnect()

# 🔹 Run the script
with client:
    client.loop.run_until_complete(get_user_groups())
