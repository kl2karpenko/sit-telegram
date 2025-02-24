import os
from flask import Flask, request, jsonify
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, ChatForbidden

app = Flask(__name__)

@app.route('/get_groups', methods=['POST'])
def get_groups():
    """Fetch all Telegram groups where the user is a member."""

    # 🔹 Get API credentials from request JSON
    data = request.json
    api_id = data.get("api_id")
    api_hash = data.get("api_hash")
    session_name = data.get("session_name", "default_session")  # Optional session name

    if not api_id or not api_hash:
        return jsonify({"error": "api_id and api_hash are required"}), 400

    # 🔹 Ensure the session file is copied to /tmp/
    local_session_file = "session_name.session"
    cloud_session_file = "/tmp/session_name.session"

    if not os.path.exists(cloud_session_file):
        shutil.copy(local_session_file, cloud_session_file)  # Copy only if it doesn’t exist

    # 🔹 Initialize Telegram Client
    client = TelegramClient(session_name, api_id, api_hash)

    with client:
        client.start()
        group_list = []

        try:
            # Fetch all dialogs (chats, groups, channels)
            dialogs = client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=100,
                hash=0
            ))

            for chat in dialogs.chats:
                try:
                    # 🔹 Skip restricted (forbidden) groups
                    if isinstance(chat, ChatForbidden):
                        print(f"🚫 No access to {chat.id}, skipping...")
                        continue

                    # 🔹 Check if group has a public username (link)
                    link = f"https://t.me/{chat.username}" if getattr(chat, "username", None) else "🔒 Private group (No public link available)"

                    # 🔹 Store group details
                    group_list.append({
                        "Group Name": chat.title,
                        "Group ID": chat.id,
                        "Access": "Public" if getattr(chat, "username", None) else "Private",
                        "Link": link
                    })

                except Exception as e:
                    print(f"❌ Error retrieving info for {chat.title}: {e}")

            return jsonify({"groups": group_list, "total": len(group_list)})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use PORT=8080 for GCF
    app.run(host="0.0.0.0", port=port, debug=True)
