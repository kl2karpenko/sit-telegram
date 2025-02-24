from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import pandas as pd

# 🔹 Replace with your Telegram API credentials
api_id = 27604095  # Замінити на твій API ID
api_hash = '0fb35a13c5f5dc31e48637336294026e'  # Замінити на твій API Hash
phone_number = '+420774895021'

# 🔹 Keywords for searching groups & channels
search_keywords = ["київ"]  # Add your topics here

# Initialize Telegram Client
client = TelegramClient("userbot_session", api_id, api_hash)

async def search_groups():
    await client.start(phone_number)

    results = []

    # Get all dialogs (chats, groups, channels)
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,  # Adjust limit for more results
        hash=0
    ))

    # Filter for groups/channels with the keyword
    for chat in dialogs.chats:
        for keyword in search_keywords:
            if keyword.lower() in chat.title.lower():
                results.append({
                    "Name": chat.title,
                    "ID": chat.id,
                    "Type": "Supergroup" if chat.megagroup else "Channel"
                })

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv("telegram_groups.csv", index=False)

    print(f"✅ {len(results)} groups/channels found and saved to 'telegram_groups.csv'")

    await client.disconnect()

# Run the function
with client:
    client.loop.run_until_complete(search_groups())
