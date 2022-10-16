from datetime import datetime, date 
import requests
import telebot
from bot import db_utils, const, utils
from bot import db_utils, const, utils
from django.utils import timezone
from datetime import timedelta
from bot.models import UZ, RU
from core.settings import ENV
from telebot.types import ReplyKeyboardMarkup
from bot.models import TelegramUser

bot = telebot.TeleBot(ENV.get('BOT_TOKEN'), parse_mode=None)

branches_list = []


# Methods

class UserState:
    start = 0
    language = 1
    contact = 2
    verification = 3
    birth_date = 4
    main_menu = 5
    personal = 6
    personal_deposit_source = 7
    personal_deposit_currency = 8
    personal_deposit_bank = 9
    personal_deposit_mobile = 10
    personal_credit_type = 11
    personal_credit = 13
    personal_card_currency = 14
    personal_card = 15
    personal_national_card = 16
    personal_internation_card = 17
    # into personal vkladi
    contributions = 18
    contributions_via_bank = 19
    contributions_via_mobile = 20
    contributions_national_pay = 21
    # 3 value
    contributions_internation_pay = 22
    corporate = 23
    entrepreneur = 25
    regions = 30
    branches = 31
    branches_tashkent = 32
    settings = 33
    change_language = 34
    contact_us = 35
    write_consultant = 36
    # 1 value only

    money_transfers = 41
    money_transfers_western = 42
    money_transfers_golden_crone = 43
    money_transfers_western_oae = 45
    money_transfers_western_central_asia = 46
    money_transfers_western_central_china = 47
    money_transfers_western_all = 48

    money_transfers_unistream = 49
    money_transfers_ria = 52
    money_transfers_moneygram = 56
    money_transfers_contact = 60
    money_transfers_asia_express = 64
    # contributions_via_mobile = 65
    # consumer credit
    personal_credit_consumer_type = 65
    personal_consumer_credit = 66
    # send message only values 2


def check_user(chat_id, tg_user_id):
    user = db_utils.get_user(chat_id)
    datetime_now = timezone.now()
    now_day, now_month = datetime_now.day, datetime_now.month
    birth_day_users = TelegramUser.objects.filter(dob__day=now_day, dob__month=now_month)
    for b_user in birth_day_users:
        send_happy_birthday_message(b_user, chat_id, b_user.lang)
    if not user:
        db_utils.create_user(chat_id, tg_user_id)
        send_welcome(chat_id)
        ask_language(chat_id)
    elif not user.lang:
        ask_language(chat_id)
    elif not user.phone_number:
        ask_contact(chat_id, user.lang)
    elif not user.is_verified:
        send_notify(chat_id, user.phone_number, user.lang)
    elif user.is_verified:
        send_main_menu(user)
    elif not user.dob:
        print("No date of birth")

        # send_happy_birthday_message(user, chat_id, user.lang)
    else:
        send_error(chat_id)


# Send message

# start
def send_welcome(chat_id):
    bot.send_message(chat_id, const.WELCOME_MESSAGE)


# register
def ask_language(chat_id):
    bot.send_message(chat_id, const.ASK_LANGUAGE, reply_markup=utils.get_buttons(const.LIST_LANG))
    bot.set_state(chat_id, UserState.language)


def ask_contact(chat_id, lang):
    bot.send_message(chat_id, const.ASK_PHONE_NUMBER[lang], reply_markup=utils.get_phone_number_button(lang))
    bot.set_state(chat_id, UserState.contact)


def send_notify(chat_id, phone_number, lang):
    bot.send_message(chat_id, const.SENT_NOTIFY[lang].format(phone_number=phone_number),
                     reply_markup=utils.get_remove_keyboard())
    bot.set_state(chat_id, UserState.verification)


def send_wrong_code(chat_id, lang):
    bot.send_message(chat_id, const.WRONG_CODE[lang])


def send_phone_number_not_found(chat_id, lang):
    bot.send_message(chat_id, const.WRONG_PHONE_NUMBER[lang])

def get_birth_date(chat_id, lang):
    bot.send_message(chat_id, )


# main menu
def send_main_menu(user):
    bot.send_message(user.chat_id, const.MAIN_MENU[user.lang], reply_markup=utils.get_main_menu_keyboard(user.lang))
    bot.set_state(user.chat_id, UserState.main_menu)


def send_error(chat_id):
    bot.send_message(chat_id, const.ERROR)
    bot.set_state(chat_id, UserState.start)


def send_error_choice(chat_id, lang):
    bot.send_message(chat_id, const.ERROR_CHOICE[lang])


def send_no_content(chat_id, lang):
    bot.send_message(chat_id, const.NO_CONTENT[lang])


def send_happy_birthday_message(user, chat_id, lang):
        bot.send_message(
            chat_id, const.SEND_HAPPY_BIRTHDAY[lang],
        )
        bot.set_state(chat_id, UserState.birth_date)
#     datetime_now = timezone.now()
#     now_day, now_month = datetime_now.day, datetime_now.month

#     birth_day_users = TelegramUser.objects.filter(dob__day=now_day, dob__month=now_month)
#     for b_user in birth_day_users:

    #     bot.send_message(
    #         chat_id, const.SEND_HSEND_HAPPY_BIRTHDAY[lang], const.ASK_BIRTH_DATE_MSG[lang])
    #     bot.set_state(chat_id, UserState.birth_date)
    # else:
    #     bot.set_state(chat_id, UserState.main_menu)

