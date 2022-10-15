import telebot
from bot.models import TelegramUser
from bot import db_utils, const, utils
from bot.models import UZ, RU
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from telebot import custom_filters
from telebot.types import Update, ReplyKeyboardMarkup
from bot.utils import get_remove_keyboard
from .methods import *


class UpdateBot(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        json_string = request.body.decode('UTF-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start(message):
    check_user(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['del'])
def del_user(message):
    try:
        TelegramUser.objects.filter().delete()
        get_remove_keyboard()
        bot.send_message(message.chat.id, "Deleted")
    except TelegramUser.DoesNotExist:
        print("User not found")


# Bot Handlers

# register

@bot.message_handler(state=UserState.language)
def language_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat.id)
    elif message.text == const.UZBEK:
        db_utils.set_user_lang(user, UZ)
        ask_contact(message.chat.id, user.lang)
    elif message.text == const.RUSSIAN:
        db_utils.set_user_lang(user, RU)
        ask_contact(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(content_types=["contact"])
def phone_number_handler(message):
    user = db_utils.get_user(message.chat.id)
    if bot.get_state(message.chat.id) != UserState.contact:
        send_error(message.chat.id)
        return
    phone_number = utils.get_phone_number(message.contact)
    if not phone_number:
        send_error(message.chat.id)
        return
    db_utils.set_phone_number(user, phone_number)
    send_notify(message.chat.id, phone_number, user.lang)


@bot.message_handler(state=UserState.verification)
def verification_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat.id)
        return
    elif user.code != message.text:
        send_wrong_code(message.chat.id, user.lang)
        return
    db_utils.set_user_verified(user)
    send_main_menu(user)


@bot.message_handler(state=UserState.birth_date)
def happy_birthday_handler(message):
    user = db_utils.get_user(message.from_user.id)
    if not user:
        send_error(message.chat.id)
        return
    else:
        send_main_menu(user)


# main menu
@bot.message_handler(state=UserState.main_menu)
def main_menu_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat.id)
    elif message.text == const.PERSONAL[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    elif message.text == const.LEGAL_ENTITY[user.lang]:
        send_corporate_message(message.chat.id, user.lang)
    elif message.text == const.SMALL_BUSINESS_N_ENTREPRENEURS[user.lang]:
        send_entrepreneur_message(message.chat.id, user.lang)
    elif message.text == const.COURSE_CURRENCY[user.lang]:
        send_currency(message.chat.id, user.lang)
    elif message.text == const.MOBILE_APP[user.lang]:
        send_mobile_app_message(message.chat.id, user.lang)
    elif message.text == const.BRANCHES_N_MINIBANKS[user.lang]:
        send_branches_message(message.chat.id, user.lang)
    elif message.text == const.SETTINGS[user.lang]:
        send_settings(message.chat.id, user.lang)
    elif message.text == const.CONTACT_US[user.lang]:
        send_contact_us(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


# was
@bot.message_handler(state=UserState.personal)
def personal_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.DEPOSITS[user.lang]:
        send_personal_source_deposit_message(message.chat.id, user.lang)
    elif message.text == const.CREDITS[user.lang]:
        send_credit_type(message.chat.id, user.lang)
    elif message.text == const.CARDS[user.lang]:
        send_card_currency(message.chat.id, user.lang)
    elif message.text == const.MONEY_TRANSFERS[user.lang]:
        send_money_transfers_types(message.chat.id, user.lang)
    elif message.text == const.CONTRIBUTIONS[user.lang]:
        send_contrib_message(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers)
def money_transfer_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    elif message.text == const.WESTERN_UNION[user.lang]:
        send_money_transfers_western_types(message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE[user.lang]:
        send_money_transfers_golden_crone(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM[user.lang]:
        send_money_gram(message.chat.id, user.lang)
    elif message.text == const.CONTACT[user.lang]:
        send_money_transfers_contact(message.chat.id, user.lang)
    elif message.text == const.ASIA_EXPRESS[user.lang]:
        bot_send_asia_express(message.chat.id, user.lang)
    elif message.text == const.PAYSEND[user.lang]:
        send_money_transfers_paysend_msg(message.chat.id, user.lang)
    elif message.text == const.RIA[user.lang]:
        send_ria_msg(message.chat.id, user.lang)
    elif message.text == const.UniStream[user.lang]:
        send_unistream_msg(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers_western)
def money_transfers_western_union_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_money_transfers(message.chat.id, user.lang)
    elif message.text == const.WESTERN_CENTRAL_ASIA[user.lang]:
        send_money_transfers_western_central_asia_msg(
            message.chat.id, user.lang)
    elif message.text == const.WESTERN_CHINA[user.lang]:
        send_money_transfers_western_china_msg(message.chat.id, user.lang)
    elif message.text == const.WESTERN_OAE[user.lang]:
        send_money_transfers_western_oae(message.chat.id, user.lang)
    elif message.text == const.WESTERN_ALL_COUNTRIES[user.lang]:
        send_money_transfers_western_all_countries(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers_western_central_asia)
def money_transfers_western_inner_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_money_transfers_western_types(message.chat.id, user.lang)
    elif message.text == const.WESTERN_CENTRAL_ASIA_SPECIAL[user.lang]:
        send_money_transfers_western_central_asia_special_msg(
            message.chat.id, user.lang)
    elif message.text == const.WESTERN_CENTRAL_ASIA_TWELWE_HOURS[user.lang]:
        send_money_transfers_western_central_asia_twelwe_hours_msg(
            message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers_golden_crone)
def money_transfers_golden_crone_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_money_transfers(message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_ASIA[user.lang]:
        send_money_transfers_golden_crone_asia_message(
            message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_EUROPE[user.lang]:
        send_money_transfers_golden_crone_europe_message(
            message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_CENTRAL_ASIA[user.lang]:
        send_money_transfers_golden_crone_central_asia_msg(
            message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_CENTRAL_ASIA_NEXT[user.lang]:
        send_money_transfers_golden_crone_central_asia_msg(
            message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_CHINA[user.lang]:
        send_money_transfers_golden_crone_china_message(
            message.chat.id, user.lang)
    elif message.text == const.GOLDEN_CRONE_KOREA[user.lang]:
        send_money_transfers_golden_crone_korea(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers_moneygram)
def money_transfers_money_gram_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_money_transfers(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM_CHINA[user.lang]:
        send_money_gram_china_message(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM_UKRAIN[user.lang]:
        send_money_gram_ukrain_message(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM_MIX[user.lang]:
        send_money_gram_mix_message(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM_RUSSIA[user.lang]:
        send_money_gram_russia_message(message.chat.id, user.lang)
    elif message.text == const.MONEY_GRAM_ALL[user.lang]:
        send_money_gram_all_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.money_transfers_asia_express)
def money_transfers_asia_express_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_money_transfers(message.chat.id, user.lang)
    elif message.text == const.MONEY_TRANSFERS_ASIA_EXPRESS[user.lang]:
        send_money_transfers_asia_express_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_deposit_source)
def personal_deposit_source_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.VIA_BANK[user.lang]:
        send_personal_currency_deposit_message(message.chat.id, user.lang)
    elif message.text == const.VIA_MOBILE[user.lang]:
        send_deposits(message.chat.id, user.lang,
                      UserState.personal_deposit_mobile, None)
    elif message.text == const.BACK[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_deposit_currency)
def personal_deposit_currency_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.NATIONAL_CURRENCY[user.lang]:
        send_deposits(message.chat.id, user.lang,
                      UserState.personal_deposit_bank, UZS)
    elif message.text == const.INTERNATION_CURRENCY[user.lang]:
        send_deposits(message.chat.id, user.lang,
                      UserState.personal_deposit_bank, USD)
    elif message.text == const.BACK[user.lang]:
        send_personal_source_deposit_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_deposit_bank)
def personal_deposit_bank_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_personal_currency_deposit_message(message.chat.id, user.lang)
    else:
        deposit = db_utils.get_deposit_by_title(message.text, user.lang)
        if not deposit:
            send_error_choice(message.chat.id, user.lang)
            return
        send_deposit(message.chat.id, user.lang, deposit)


@bot.message_handler(state=UserState.personal_deposit_mobile)
def personal_deposit_mobile_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_personal_currency_deposit_message(message.chat.id, user.lang)
    else:
        deposit = db_utils.get_deposit_by_title(message.text, user.lang)
        if not deposit:
            send_error_choice(message.chat.id, user.lang)
            return
        send_deposit(message.chat.id, user.lang, deposit)


# personal_consumer_credit
@bot.message_handler(state=UserState.personal_credit)
def personal_credit_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_credit_type(message.chat.id, user.lang)
    elif message.text == const.IPO_CREDIT[user.lang]:
        send_personal_ipo_credit_message(message.chat.id, user.lang)
    elif message.text == const.CONSUMER_CREDIT[user.lang]:
        send_personal_credit_consumer(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_credit_type)
def personal_credit_type_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.IPO_CREDIT[user.lang]:
        send_personal_ipo_credit_message(message.chat.id, user.lang)
    elif message.text == const.CONSUMER_CREDIT[user.lang]:
        send_personal_credit_consumer(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_consumer_credit)
def personal_consumer_credit_type_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        user = db_utils.get_user(message.chat.id)
    elif message.text == const.BACK[user.lang]:
        send_credit_type(message.chat.id, user.lang)
    elif message.text == const.CONSUMER_CREDIT_MIKROZIME[user.lang]:
        send_credit_consumer_credit_mikrozime(message.chat.id, user.lang)
    elif message.text == const.CONSUMER_CREDIT_ONLINE_MIKROZIME[user.lang]:
        send_credit_consumer_credit_online_mikrozime(
            message.chat.id, user.lang)
    elif message.text == const.CONSUMER_CREDIT_INNER[user.lang]:
        send_credit_consumer_credit_simple(message.chat.id, user.lang)
    elif message.text == const.CONSUMER_STUDY[user.lang]:
        send_credit_consumer_study(message.chat.id, user.lang)
    elif message.text == const.FADIN[user.lang]:
        send_credit_fadin(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_card_currency)
def personal_card_currency_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.NATIONAL_CURRENCY[user.lang]:
        send_personal_national_cards(message.chat.id, user.lang)
    elif message.text == const.INTERNATION_CURRENCY[user.lang]:
        send_personal_internation_cards(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_national_card)
def personal_card_national_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_card_currency(message.chat.id, user.lang)
    elif message.text == const.UZCARD_CARD[user.lang]:
        send_personal_national_uzcard_message(message.chat.id, user.lang)
    elif message.text == const.HUMO_CARD[user.lang]:
        send_personal_national_humo_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.personal_internation_card)
def personal_card_internation_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_card_currency(message.chat.id, user.lang)
    elif message.text == const.MASTERCARD_STANDART_CARD[user.lang]:
        send_personal_internation_mastercard_standart_message(
            message.chat.id, user.lang)
    elif message.text == const.MASTERCARD_GOLD_CARD[user.lang]:
        send_personal_internation_mastercard_gold_message(
            message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.contributions)
def contributions_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_personal_message(message.chat.id, user.lang)
    elif message.text == const.VIA_BANK[user.lang]:
        send_contrib_via_bank_message(message.chat.id, user.lang)
    elif message.text == const.VIA_MOBILE[user.lang]:
        send_contrib_via_mobile_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


# via bank handler
@bot.message_handler(state=UserState.contributions_via_bank)
def contributions_via_bank_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_contrib_message(message.chat.id, user.lang)
    elif message.text == const.NATIONAL_CURRENCY[user.lang]:
        send_contrib_via_national_currency_message(message.chat.id, user.lang)
    elif message.text == const.INTERNATION_CURRENCY[user.lang]:
        send_contrib_via_internation_currency_message(
            message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


# via mobile handler
@bot.message_handler(state=UserState.contributions_via_mobile)
def contributions_via_mobile_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_contrib_message(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.corporate)
def corporate_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.CREDIT_BUSINESS[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.CORPORATE_CARDS[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.DEPOSITS[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.CASH_SERVICES[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.entrepreneur)
def entrepreneur_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.LEASING[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.SMALL_BUSINESS_CREDIT[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.BANK_GUARANTEES[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.CORPORATE_BANK_CARDS[user.lang]:
        send_no_content(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.regions)
def regions_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const:
        send_change_language(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.branches)
def branches_handler(message):
    user = db_utils.get_user(message.chat.id)
    get_branches_messages(message, message.chat.id)
    # for branch in branches_list:
    #     # print(branch)
    #     if branch['title'] == message.text:
    #         text = f"{branch['address']}, {branch['id']}"
    #         bot.send_message(user.chat_id, text)
    #         bot.send_location(user.chat_id, branch['lng'], branch['lat'])
    if not user:
        send_error(message.chat)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    elif not message:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.settings)
def settings_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.CHANGE_LANGUAGE[user.lang]:
        send_change_language(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        bot.send_message(message.chat.id, message.text)


@bot.message_handler(state=UserState.branches_tashkent)
def branches_tashkent_handler(message):
    user = db_utils.get_user(message.chat.id)
    for branch in branches_list:
        print(branch)
        if branch['title'] == message.text:
            text = f"{branch['address']}, {branch['id']}"
            bot.send_message(user.chat_id, text)
            bot.send_location(user.chat_id, branch['lng'], branch['lat'])


@bot.message_handler(state=UserState.change_language)
def change_language_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.UZBEK:
        db_utils.set_user_lang(user, UZ)
        send_settings(message.chat.id, user.lang)
    elif message.text == const.RUSSIAN:
        db_utils.set_user_lang(user, RU)
        send_settings(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.contact_us)
def contact_us_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.CALL_BANK[user.lang]:
        send_call_bank_message(message.chat.id, user.lang)
    elif message.text == const.WRITE_CONSULTANT[user.lang]:
        send_write_consultant(message.chat.id, user.lang)
    elif message.text == const.BACK[user.lang]:
        send_main_menu(user)
    else:
        send_error_choice(message.chat.id, user.lang)


@bot.message_handler(state=UserState.write_consultant)
def write_consultant_handler(message):
    user = db_utils.get_user(message.chat.id)
    if not user:
        send_error(message.chat)
    elif message.text == const.SEND_BTN[user.lang]:
        send_description_message(message, user)
    elif message.text == const.SKIP_BTN[user.lang]:
        send_main_menu(user)
    elif message.text == const.BACK[user.lang]:
        send_contact_us(message.chat.id, user.lang)
    else:
        send_error_choice(message.chat.id, user.lang)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.enable_saving_states()
