import asyncio
from flask import Request, jsonify
from telethon import TelegramClient

def telegram_message_handler(request: Request):
    """Cloud Function Entry Point to Send Telegram Messages."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON request"}), 400

    # ✅ Get Telegram API credentials from the request body
    api_id = data.get("api_id")
    api_hash = data.get("api_hash")
    phone_number = data.get("phone_number")
    recipients = data.get("recipients")  # Array of Telegram usernames, phone numbers, or Group IDs
    message_text = data.get("message")

    if not all([api_id, api_hash, phone_number, recipients, message_text]):
        return jsonify({"error": "Missing required parameters"}), 400

    if not isinstance(recipients, list):
        return jsonify({"error": "Recipients must be an array"}), 400

    # ✅ Initialize Telegram Client
    client = TelegramClient("/tmp/user_session", int(api_id), api_hash, device_model="iPhone 13", system_version="iOS 16.0")

    async def send():
        await client.start(phone=phone_number)
        results = []

        for recipient in recipients:
            try:
                await client.send_message(recipient, message_text)
                results.append({"recipient": recipient, "status": "Message sent!"})
            except Exception as e:
                results.append({"recipient": recipient, "error": str(e)})

        return results

    # ✅ Explicitly Create and Use a New Async Event Loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(send())

    return jsonify({"results": result})
