#!/usr/bin/python3
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
############################### Bot ############################################

TOKEN = "857469894:AAETNSFvvX_8L8gqtqYGFJ133ov_AXt24zg"
POSTAL_CODE = []
# POSTAL_CODE = '111111'
# bot = telegram.Bot(token=TOKEN)

schedule = {'NK': {
    '12:00': 16.99,
    '12:30': 1.22,
    '13:00': 7.18,
    '13:30': 16.35,
    '14:00': 20.69,
    '14:30': 10.18,
    '15:00': 4.91,
    '15:30': 5.69,
    '16:00': 19.50,
    '16:30': 3.21,
    '17:00': 20.81,
    '17:30': 1.77,
    '18:00': 17.5,
    '18:30': 4.67,
    '19:00': 0.00,
    '19:30': 9.41
}, 'FFL': {
    '12:00': 14.29,
    '12:30': 11.27,
    '13:00': 0.00,
    '13:30': 13.33,
    '14:00': 6.56,
    '14:30': 14.69,
    '15:00': 12.93,
    '15:30': 8.95,
    '16:00': 4.25,
    '16:30': 13.45,
    '17:00': 2.3,
    '17:30': 19.79,
    '18:00': 7.70,
    '18:30': 18.60,
    '19:00': 12.4,
    '19:30': 15.83
}, 'AM': {
    '12:00': 4,
    '12:30': 5,
    '13:00': 6,
    '13:30': 7,
    '14:00': 9,
    '14:30': 1,
    '15:00': 0,
    '15:30': 2,
    '16:00': 3,
    '16:30': 4,
    '17:00': 5,
    '17:30': 7,
    '18:00': 20,
    '18:30': 11,
    '19:00': 12,
    '19:30': 9
}}

food = {'NK': {
    'green curry rice': 20,
    'pad thai': 20
}, 'FFL': {
    'Yoghurt': 7,
    'milkshake': 10
}, 'AM': {
    'pattaya' : 12,
    'mee goreng' : 10
}}


####### SETTLE POSTAL CODE #######
def register(bot, update):
    bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,text='Enter the postal code of your collection location:')

def saveuserDetails(bot, update):
    bot.send_chat_action(chat_id=update.effective_user.id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,text='Received your location details!')
    user_id=update.message.from_user.id
    # customer_name,address,phone_number=update.message.text.split(',')
    # POSTAL_CODE = update.message.text
    POSTAL_CODE.append(update.message.text)
    start(bot, update)



####### USING BOT FOR ORDERING #######
def start(bot, update):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())


def merchant_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=first_menu_message(),
                          reply_markup=merchants_keyboard())

# def food_menu(bot, update):
#     query = update.callback_query
#     bot.edit_message_text(chat_id=query.message.chat_id,
#                           message_id=query.message.message_id,
#                           text=first_menu_message(),
#                           reply_markup=food_keyboard(query['data']))

def schedule_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=second_menu_message(query['data']),
                          reply_markup=schedule_keyboard(query['data']))

def food_menu(bot, update):
    query = update.callback_query
    print('Foodmenu:', query)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text="Please select your food items:",
                          reply_markup=food_keyboard())

def final_menu(bot, update):
    query = update.callback_query
    print('finalmenu:', query)
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text="Your final cost is: $20.13. Collection location is {}".format(POSTAL_CODE[-1]),
                          reply_markup=final_keyboard())

# and so on for every callback_data option


def first_submenu(bot, update):
    pass


def second_submenu(bot, update):
    pass

############################ Keyboards #########################################


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('I\'m Hungry!', callback_data='locations')],
                [InlineKeyboardButton('I want....', callback_data='new')]]
    return InlineKeyboardMarkup(keyboard)


def merchants_keyboard():
    keyboard = [[InlineKeyboardButton('Fresh Fruits Labs', callback_data='FFL')],
                [InlineKeyboardButton('Ameen\'s', callback_data='AM')],
                [InlineKeyboardButton('Nakhon', callback_data='NK')]]
    return InlineKeyboardMarkup(keyboard)


def schedule_keyboard(merchant):
    if merchant == 'FFL':
        keyboard = list(
            map(lambda x: [InlineKeyboardButton(str(x) + '@ $' + str(schedule[merchant][x]), callback_data='cfm')], schedule[merchant]))
    elif merchant == 'AM':
        keyboard = list(
            map(lambda x: [InlineKeyboardButton(str(x) + ' with {} people ordering'.format(str(schedule[merchant][x])), callback_data='cfm')], schedule[merchant]))
    
    # keyboard = list(
    #     map(lambda x: [InlineKeyboardButton(str(x) + '@ $' + str(schedule[merchant][x]), callback_data='cfm')], schedule[merchant]))
    return InlineKeyboardMarkup(keyboard)

def food_keyboard():
    # if merchant == 'FFLcfm':
    #     keyboard = [[InlineKeyboardButton('Gin and Tonic (Hendricks) -- $9', callback_data='FFLcfm')],
    #                 [InlineKeyboardButton('Gin and Tonic (Bombay) -- $10', callback_data='FFLcfm')],
    #                 [InlineKeyboardButton('Housepour -- $11', callback_data='FFLcfm')]]
    # elif merchant == 'AMcfm':
    #     keyboard = [[InlineKeyboardButton('Roti Prata -- $5', callback_data='AMcfm')],
    #                 [InlineKeyboardButton('Murtabak -- $9', callback_data='AMcfm')],
    #                 [InlineKeyboardButton('Milo Dinosaur -- $20', callback_data='AMcfm')]]
    # elif merchant == 'NKcfm':
    #     keyboard = [[InlineKeyboardButton('Pineapple Fried Rice -- $30', callback_data='NKcfm')],
    #                 [InlineKeyboardButton('Green Curry and Chicken -- $50', callback_data='NKcfm')],
    #                 [InlineKeyboardButton('Hor Fun -- $99', callback_data='NKcfm')]]
    keyboard = [[InlineKeyboardButton('Watermelon Juice -- $9', callback_data='receipt')],
                [InlineKeyboardButton('Apple Juice -- $10', callback_data='receipt')],
                [InlineKeyboardButton('Mother\'s Day Chocolates -- $11', callback_data='receipt')]]
    return InlineKeyboardMarkup(keyboard)

def final_keyboard():
    keyboard = [[InlineKeyboardButton('Back to Main', callback_data = 'back_to_main')]]
    return InlineKeyboardMarkup(keyboard)


def cfm_keyboard():
    keyboard = []
    return InlineKeyboardMarkup(keyboard)


"""
def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
"""

############################# Messages #########################################


def main_menu_message():
    return 'Choose the option in main menu:'


def first_menu_message():
    return 'Choose your merchant'
    

def second_menu_message(merchant):
    if merchant == 'AM':
        return 'No discount. $4 delivery charge.'
    elif merchant == 'FFL':
        return '20 percent discount upon $50 total receipt'


############################# Handlers #########################################
updater = Updater(TOKEN)

# getting postal code from user
updater.dispatcher.add_handler(MessageHandler([Filters.text], saveuserDetails))
# registering the postal code of collection location 
updater.dispatcher.add_handler(CommandHandler('register',register))

# initiating the chatbot
updater.dispatcher.add_handler(CommandHandler('start', start))
# main menu
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
# menu for merchants, display locations which lead to available timings
updater.dispatcher.add_handler(
    CallbackQueryHandler(merchant_menu, pattern='locations'))
# provides menu for existing schedule
for key, value in schedule.items():
    updater.dispatcher.add_handler(CallbackQueryHandler(schedule_menu, pattern=key))
    # updater.dispatcher.add_handler(CallbackQueryHandler(food_menu, pattern=key+'cfm'))

updater.dispatcher.add_handler(CallbackQueryHandler(food_menu, pattern='cfm'))
updater.dispatcher.add_handler(CallbackQueryHandler(final_menu, pattern='receipt'))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='back_to_main'))


updater.start_polling()
################################################################################
updater.idle()
