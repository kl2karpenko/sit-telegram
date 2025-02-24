from telethon.sync import TelegramClient

# 🔹 Your API credentials
api_id = 25146169
api_hash = 'a266dde03d03ab4af7df4e7021afb55c'
phone_number = '+380504144151'  # Your phone number

# 🔹 Create a new session file
client = TelegramClient("session_name", api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    print("✅ Session created successfully! Now deploy the session file to Google Cloud.")

with client:
    client.loop.run_until_complete(main())