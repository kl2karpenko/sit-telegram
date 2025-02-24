from telethon.sync import TelegramClient
import csv
import os

# 🔹 Введи свої API-дані (отримати тут: https://my.telegram.org/apps)
# 🔹 Ukraine Telegram
api_id = 25146169
api_hash = 'a266dde03d03ab4af7df4e7021afb55c'

# api_id = 27604095  # Замінити на твій API ID
# api_hash = '0fb35a13c5f5dc31e48637336294026e'  # Замінити на твій API Hash
group_link = 'marketing_backpack'  # Замінити на назву групи або ID

# 🔹 Створюємо клієнта (не треба викликати .start() всередині функції)
client = TelegramClient('userbot_session', api_id, api_hash)

async def scrape_members(group_link):
    """Збирає список учасників з групи та зберігає у CSV."""
    try:
        await client.start()

        # 🛠 Обробка, якщо передано повний лінк "https://t.me/group_name"
        if "t.me/" in group_link:
            group_link = group_link.split("/")[-1]

        # 📌 Отримуємо дані групи
        group = await client.get_entity(group_link)
        print(f"📌 Збір учасників із групи: {group.title} (ID: {group.id})")

        # 📌 Отримуємо список учасників
        participants = await client.get_participants(group)

        if not participants:
            print("⚠️ У групі немає учасників або не вдалося отримати список.")
            return

        # 📌 Записуємо у CSV
        csv_file = 'members.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Username", "First Name", "Last Name"])

            for user in participants:
                writer.writerow([
                    user.id,
                    user.username or "",  # Запобігає NoneType error
                    user.first_name or "",
                    user.last_name or ""
                ])

        print(f"✅ Успішно зібрано {len(participants)} учасників та збережено у {csv_file}.")

    except Exception as e:
        print(f"❌ Помилка: {e}")

    finally:
        await client.disconnect()

# 🔹 Виклик функції
with client:
    client.loop.run_until_complete(scrape_members(group_link))
