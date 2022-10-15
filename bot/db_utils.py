import requests
import json
from bot import utils

from bot.models import TelegramUser, UZ



def create_user(chat_id, tg_user_id):
    try:
        TelegramUser.objects.create(chat_id=chat_id, tg_user_id=tg_user_id)
    except Exception as e:
        print(f"No user exists: {e}")

def get_user(chat_id):
    users = TelegramUser.objects.filter(chat_id=chat_id)
    if not users.exists():
        return None
    return users.first()


def set_user_lang(user, lang):
    user.lang = lang
    user.save()


def get_user_phone_number(phone_number):
    users = TelegramUser.objects.filter(phone_number=phone_number, chat_id__isnull=True, tg_user_id__isnull=True)
    if not users.exists():
        return None
    return users.first()


def set_phone_number(user, phone_number):
    user.phone_number = phone_number
    user.code = "11111"
    user.save()



def set_user_verified(user):
    user.is_verified = True
    user.save()

