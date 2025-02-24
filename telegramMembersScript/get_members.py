import os
from flask import Flask, request, jsonify
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

app = Flask(__name__)

@app.route('/get_members', methods=['POST'])
def get_members():
    """Fetch members from a Telegram group based on API credentials and Group ID."""

    data = request.json  # Get JSON data from request
    api_id = data.get("api_id")
    api_hash = data.get("api_hash")
    group_id = data.get("group_id")

    if not api_id or not api_hash or not group_id:
        return jsonify({"error": "api_id, api_hash, and group_id are required"}), 400

    # 🔹 Ensure the session file is copied to /tmp/
    local_session_file = "session_name.session"
    cloud_session_file = "/tmp/session_name.session"

    if not os.path.exists(cloud_session_file):
        shutil.copy(local_session_file, cloud_session_file)  # Copy only if it doesn’t exist

    # 🔹 Initialize client with dynamic credentials
    client = TelegramClient("session_name", api_id, api_hash)

    with client:
        client.start()

        try:
            # 🔹 Fetch group entity
            group = client.get_entity(int(group_id))

            # 🔹 Fetch participants (up to 10,000)
            participants = client(GetParticipantsRequest(
                group, ChannelParticipantsSearch(''), 0, 10000, hash=0
            ))

            members_list = [
                {
                    "User ID": user.id,
                    "Username": user.username,
                    "First Name": user.first_name,
                    "Last Name": user.last_name
                }
                for user in participants.users
            ]

            return jsonify({"members": members_list, "total": len(members_list)})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            client.disconnect()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use PORT=8080 for GCF
    app.run(host="0.0.0.0", port=port, debug=True)
