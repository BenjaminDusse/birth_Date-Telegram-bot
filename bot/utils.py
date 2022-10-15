import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot import const
from bot.models import UZ


def check_phone_number(phone_number):
    if phone_number and len(phone_number) == 12 and phone_number.isdecimal() and phone_number.startswith("998"):
        return True
    return False


def get_phone_number(contact):
    if not (contact and contact.phone_number):
        return None
    if "+" in contact.phone_number:
        return contact.phone_number[1:]
    return contact.phone_number[1:]


def get_buttons(buttons, lang=None, n=2):
    rkm = ReplyKeyboardMarkup(True, row_width=n)
    if lang is None:
        rkm.add(*(KeyboardButton(btn) for btn in buttons))
    else:
        rkm.add(*(KeyboardButton(btn[lang]) for btn in buttons))
    return rkm


def get_phone_number_button(lang):
    return ReplyKeyboardMarkup(True, row_width=1).add(
        KeyboardButton(const.ASK_PHONE_NUMBER_BTN[lang], request_contact=True),
    )


def get_main_menu_keyboard(lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.add(*(KeyboardButton(btn[lang]) for btn in const.MAIN_MENU_KEYBOARD))
    rkm.add(KeyboardButton(const.CONTACT_US[lang]))
    return rkm


def get_remove_keyboard():
    return ReplyKeyboardRemove()


def get_currency(lang):
    lang_name = f"CcyNm_{lang.upper()}"
    url, codes, flags, text, c = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/", ['840', '978', '643'], ["🇺🇸", "🇪🇺",
                                                                                                         "🇷🇺"], "", 0
    result = requests.get(url).json()
    for i in result:
        if i["Code"] in codes:
            text += f"{flags[c]} {i[lang_name]} = <strong>{i['Rate']}</strong>\t ({i['Diff']})\n\n"
            c += 1
    return f"{const.CURRENCY[lang]}  {i['Date']}\n\n{text}"


def get_feedbacks_text(feedback_parts):
    text = ""
    for part in feedback_parts:
        text += part.text + "\n\n"
    text = text[:-2]
    return text


def get_regions_keyboard(regions, lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    if lang == UZ:
        rkm.add(*(KeyboardButton(region.title_uz) for region in regions))
    else:
        rkm.add(*(KeyboardButton(region.title_ru) for region in regions))
    rkm.add(KeyboardButton(const.BACK[lang]))
    return rkm


def get_products_keyboard(products, lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    if lang == UZ:
        rkm.add(*(KeyboardButton(product.title_uz) for product in products))
    else:
        rkm.add(*(KeyboardButton(product.title_ru) for product in products))
    rkm.add(KeyboardButton(const.BACK[lang]))
    return rkm


def get_product_text(product, lang):
    return product.description_uz if lang == UZ else product.description_ru


def get_contributions_keyboards(contribs, lang):
    buttons = ReplyKeyboardMarkup(True, row_width=2)
    if lang == UZ:
        buttons.add(*(KeyboardButton(contrib.title.uz)
                    for contrib in contribs))
    else:
        buttons.add(*(KeyboardButton(contrib.title.ru)
                    for contrib in contribs))
    buttons.add(KeyboardButton(const.BACK[lang]))
    return buttons


def get_user_birth_date(user, message, lang):
    for _ in message.split():
        day = message[0]
        month = message[1]
        year = message[2]
    user.birth_date(day, month, year)
    user.save()
