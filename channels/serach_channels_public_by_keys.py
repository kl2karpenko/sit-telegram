from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
import asyncio

# 🔹 Replace with your Telegram API credentials
api_id = 27604095  # Your API ID
api_hash = '0fb35a13c5f5dc31e48637336294026e'  # Your API Hash

# 🔹 Keywords to search for
search_keywords = ["Crypto", "Marketing", "AI", "Finance"]  # Add more topics here

client = TelegramClient("session_name", api_id, api_hash)

async def search_public_groups(keywords):
    """Searches for public groups matching multiple keywords."""
    all_results = []  # Store all found groups

    for keyword in keywords:
        print(f"🔍 Searching for: {keyword}")
        result = await client(SearchRequest(q=keyword, limit=10))

        for chat in result.chats:
            group_info = {"Keyword": keyword, "Title": chat.title, "ID": chat.id}
            all_results.append(group_info)
            print(f"✅ Found: {chat.title} (ID: {chat.id})")

    return all_results

with client:
    client.loop.run_until_complete(search_public_groups(search_keywords))