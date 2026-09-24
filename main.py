import os
import time
import requests
from datetime import datetime

# =========================
# НАСТРОЙКИ
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверяем даты до конца июля 2027
DATE_FROM = datetime.now().date()
DATE_TO = datetime(2027, 7, 31).date()

# Проверка каждые 5 минут
CHECK_INTERVAL = 300


def send_telegram(message):
    """Отправляет уведомление в Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Не заданы TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=20
        )

        if response.ok:
            print("Telegram notification sent")
        else:
            print("Telegram error:", response.text)

    except Exception as e:
        print("Telegram connection error:", e)


def check_appointments():
    """
    Здесь будет выполняться проверка календаря
    записи на интервью США в Астане для нерезидентов.

    Бот предназначен только для мониторинга
    и отправки уведомлений.
    Автоматическая запись не выполняется.
    """

    print(
        f"[{datetime.now()}] Checking Astana appointments "
        f"from {DATE_FROM} to {DATE_TO}"
    )

    # Следующим шагом подключим сюда
    # проверку календаря записи.
    return []


def main():

    print("US Visa Astana Monitor started")

    send_telegram(
        "✅ Мониторинг запущен.\n\n"
        "🇺🇸 Посольство США: Астана\n"
        "👤 Категория: нерезиденты\n"
        "📅 Ищем даты до 31.07.2027\n"
        "🔔 Режим: только уведомления"
    )

    while True:

        try:
            available_dates = check_appointments()

            if available_dates:

                dates_text = "\n".join(
                    str(date) for date in available_dates
                )

                send_telegram(
                    "🚨 НАЙДЕНА СВОБОДНАЯ ДАТА!\n\n"
                    f"{dates_text}\n\n"
                    "Зайдите в личный кабинет и проверьте запись."
                )

        except Exception as e:
            print("Monitor error:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
