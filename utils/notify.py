import os, platform, subprocess
from utils.profils import cfg
EMAIL_SMTP_SERVER_ADRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_PORT = os.getenv("EMAIL_SMTP_PORT")
EMAIL_RECEIVER_ADRESS = os.getenv("EMAIL_RECEIVER_ADRESS")
EMAIL_SENDER_ADDRESS = os.getenv("EMAIL_SENDER_ADDRESS")
EMAIL_SENDER_LOGIN = os.getenv("EMAIL_SENDER_LOGIN")
EMAIL_SENDER_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")

SMS_PROVIDER = os.getenv("SMS_PROVIDER")

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
DISCORD_NOTIFY_ID = os.getenv("DISCORD_NOTIFY_ID")


def send_sms(message: str):
    getattr(
        getattr(__import__(f"components.sms.{SMS_PROVIDER}"), "sms"), SMS_PROVIDER
    ).send_sms(message)


def send_to_discord_webhook(message):
    if DISCORD_NOTIFY_ID is not None and len(DISCORD_NOTIFY_ID) > 0:
        message = "<@" + DISCORD_NOTIFY_ID + ">\n" + message
    import requests

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=5,
    )


# Fonction pour envoyer un email d'alerte
def send_email(stock_name: str, message: str):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_SENDER_ADDRESS
        message["To"] = EMAIL_RECEIVER_ADRESS
        message["Subject"] = f"Alert: Price change on {stock_name}"
        message.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(EMAIL_SMTP_SERVER_ADRESS, int(EMAIL_SMTP_PORT)) as server:
            server.starttls()
            server.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f"Error on mail sending: {e}")


def desktop_notification(stock_name: str, message: str):
    os = platform.system()
    title = f"Alert: Price change on {stock_name}"
    if os == "Darwin":
        return subprocess.run(
            [
                "osascript",
                "-e",
                "display",
                "notification",
                message,
                "with",
                "title",
                title,
            ],
            capture_output=False,
            timeout=5,
        )

    if os == "Linux":
        return subprocess.run(
            ["notify-send", title, message], capture_output=False, timeout=5
        )

    if os == "Windows":
        from win10toast import ToastNotifier

        toaster = ToastNotifier()
        return toaster.show_toast(title, message, icon_path="mooniorny.png", duration=0)

    print("OS: ", os, " not suported for desktop notification")


def alert(stock_name: str, new_price: float):
    message = f"Price of {stock_name} as reach maturity: {new_price}"
    if (
        "desktop_notification" in cfg["alerts"]
        and cfg["alerts"]["desktop_notification"] is True
    ):
        desktop_notification(stock_name, message)
    send_sms(message)
    send_email(stock_name, message)
