from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
import pandas as pd
import time

# 🔹 Replace with your Telegram API credentials
api_id = 27604095  # Your API ID
api_hash = '0fb35a13c5f5dc31e48637336294026e'  # Your API Hash

# 🔹 Keywords to search for groups
search_keywords = ["Crypto", "Marketing", "AI", "Finance"]

client = TelegramClient("session_name", api_id, api_hash)

async def search_public_groups_and_get_members(keywords):
    """Search for public groups, get member count, and extract members"""
    all_results = []  # Store found groups
    all_members = []  # Store members list

    for keyword in keywords:
        print(f"🔍 Searching for: {keyword}")
        result = await client(SearchRequest(q=keyword, limit=5))  # Search groups

        for chat in result.chats:
            try:
                # 🔹 Get detailed channel/group info (including member count)
                full_chat = await client(GetFullChannelRequest(chat))
                members_count = full_chat.full_chat.participants_count

                group_info = {
                    "Keyword": keyword,
                    "Title": chat.title,
                    "ID": chat.id,
                    "Type": "Supergroup" if chat.megagroup else "Channel",
                    "Members": members_count
                }
                all_results.append(group_info)

                print(f"✅ Found: {chat.title} (ID: {chat.id}, Members: {members_count})")

                # 🔹 Fetch Members from Public Group (Only works for groups, not channels)
                if chat.megagroup:  # Only works for supergroups
                    participants = await client(GetParticipantsRequest(
                        chat, ChannelParticipantsSearch(''), 0, 100, hash=0
                    ))

                    for user in participants.users:
                        user_info = {
                            "Group": chat.title,
                            "User ID": user.id,
                            "Username": user.username,
                            "First Name": user.first_name,
                            "Last Name": user.last_name
                        }
                        all_members.append(user_info)
                        print(f"   👤 {user.first_name} {user.last_name} (@{user.username})")

            except Exception as e:
                print(f"❌ Error fetching members for {chat.title}: {e}")

    return all_results, all_members

with client:
    group_results, member_results = client.loop.run_until_complete(search_public_groups_and_get_members(search_keywords))

# 🔹 Save groups info to CSV
df_groups = pd.DataFrame(group_results)
df_groups.to_csv("telegram_groups.csv", index=False)

# 🔹 Save members info to CSV
df_members = pd.DataFrame(member_results)
df_members.to_csv("telegram_members.csv", index=False)

print("✅ Group list saved to 'telegram_groups.csv'")
print("✅ Members list saved to 'telegram_members.csv'")
