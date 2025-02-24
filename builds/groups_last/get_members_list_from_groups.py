from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import pandas as pd

# 🔹 Your API credentials
api_id = 25146169
api_hash = 'a266dde03d03ab4af7df4e7021afb55c'

# 🔹 Group ID you want to scrape
group_id = 2007705377  # Replace with the Group ID

client = TelegramClient("session_name", api_id, api_hash)

async def get_members():
    await client.start()

    try:
        # 🔹 Fetch group entity
        group = await client.get_entity(group_id)

        # 🔹 Fetch participants (first 10,000)
        participants = await client(GetParticipantsRequest(
            group, ChannelParticipantsSearch(''), 0, 10000, hash=0
        ))

        members_list = []

        for user in participants.users:
            members_list.append({
                "User ID": user.id,
                "Username": user.username,
                "First Name": user.first_name,
                "Last Name": user.last_name
            })
            print(f"👤 {user.first_name} {user.last_name} (@{user.username})")

        # 🔹 Save to CSV
        df = pd.DataFrame(members_list)
        df.to_csv("group_members.csv", index=False)

        print(f"✅ Successfully saved {len(members_list)} members to 'group_members.csv'.")

    except Exception as e:
        print(f"❌ Error retrieving members: {e}")

    await client.disconnect()

# Run the script
with client:
    client.loop.run_until_complete(get_members())
