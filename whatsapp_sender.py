import pandas as pd
import pywhatkit
import re
import time

MODE = "live"   
MAX_LIVE_MESSAGES = 2
live_sent = 0


df = pd.read_csv(r"C:\Users\Huawei\OneDrive\Attachments\message - Sheet1 (1).csv", encoding="utf-8-sig")

df.columns = df.columns.str.strip().str.lower()

print("Columns found:", df.columns.tolist())

for index, row in df.iterrows():
    phone = str(row["phone"]).strip()
    message = row["message"]
    if phone.startswith('8') and len(phone) == 11:
        phone = '+7' + phone[1:]

        
    elif phone.startswith('7') and len(phone) == 11:
        phone = '+' + phone
    try:
        if not re.match(r'^\+7\d{10}$', phone):
            raise ValueError("Неверный номер")

        if MODE == "dry-run":
            print(f"[DRY RUN] {phone}")
            print(message)
            print()

            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"[DRY RUN] {phone}: {message}\n")

        else:
            if live_sent >= MAX_LIVE_MESSAGES:
                print("Достигнут лимит live-сообщений.")
                break

            print(f"Отправка на {phone}...")

            pywhatkit.sendwhatmsg_instantly(
                phone,
                message,
                wait_time=20,
                tab_close=True
            )

            print("Отправлено.")
            live_sent += 1
            time.sleep(10)

    except ValueError as e:
        print(f"Ошибка: {phone} → {e}")

    except Exception as e:
        print(f"Ошибка отправки: {phone}")
        print(e)