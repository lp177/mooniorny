import os

SMS_USER = os.getenv("SMS_USER")
SMS_PASSWORD = os.getenv("SMS_PASSWORD")


def send_sms(msg: str):
    import urllib.parse
    import urllib.request

    f = {"user": SMS_USER, "pass": SMS_PASSWORD, "msg": msg}
    urllib.request.urlopen(
        "https://smsapi.free-mobile.fr/sendmsg?" + urllib.parse.urlencode(f)
    )
