cfg = {
    "desktop_notification": True,
    "email": {
        "smtp_server_adress": "smtp.gmail.com",
        "smtp_port": 587,
        "receiver_adress": "notify_me_on_maturity@exemple.com",
        "sender_address": "my_account_create_for_this_app@gmail.com",
        "sender_login": "my_account_create_for_this_app@gmail.com",
        "sender_password": "my_password_or_app_key_generate_for_this_access",  # https://support.google.com/mail/answer/185833
    },
    "sms": {
        "provider": "free_mobile",  # Check components/sms/* for find or add your provider
        "user": "pseudo",
        "password": "password",
    },
    "discord": {
        "webhook": "https://discord.com/api/webhooks/***",  # https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
        "notify_id": "generaly ~18 numbers",  # optional: for ping specific user/group https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID
    },
}
