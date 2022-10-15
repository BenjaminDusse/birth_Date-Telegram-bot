from email.policy import default
from enum import auto
from django.db import models



UZ = "uz"
RU = "ru"


PHONE = "phone"
TELEGRAM = "telegram"
BOTH = "both"


class TelegramUser(models.Model):
    LANGUAGE_CHOICE = (
        (UZ, 'uz'),
        (RU, 'ru'),
    )
    CONTACT_TYPE = (
        (PHONE, 'phone'),
        (TELEGRAM, 'telegram'),
        (BOTH, 'both'),
    )

    tg_user_id = models.PositiveBigIntegerField(unique=True)
    chat_id = models.PositiveBigIntegerField(unique=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    lang = models.CharField(max_length=3, choices=LANGUAGE_CHOICE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=12, null=True, blank=True)
    send_message_type = models.CharField(max_length=25, choices=CONTACT_TYPE, null=True, blank=True)
    dob = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
