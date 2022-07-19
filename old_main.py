
from typing import Dict
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import BotCommand, CallbackQuery, KeyboardButton, MenuButton, ReplyKeyboardMarkup
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram_bot_pagination import InlineKeyboardPaginator
WELCOME_MESSAGE = "תודה שהצטרפת לשירות!\n" \
    "בנוסף אנחנו נזכיר לך פעם ביום בשעה %s לכתוב לנו מה חדש"
CONTINUE_MESSAGE = "ניתן לשלוח לי בכל רגע מה חדש אצלך בעסק ותמונות מהעסק שלך."
COMMANDS_MENU = """
    /start - להתחבר לשירות
    /help - להציג את הדרכה לשימוש בשירות
    /change_time - לשנות את השעה להתראה"""
updater = Updater("fff",
                  use_context=True)
bot = updater.bot
registered_users = []

def start(update: Update, context: CallbackContext):
    # if the user is not yet registered, show him a webcome message and add him to the list of registered users
    if update.effective_user.id not in registered_users:
        update.message.reply_text(WELCOME_MESSAGE % "18:00")
        registered_users.append(update.effective_user.id)
    # add keyboard with 2 buttons: "עדכן על מה חדש" and "שנה שעת התראה"
    
    # custom_keyboard = [['עדכן על מה חדש', 'שנה שעת התראה'], ['עזרה']]
    # custom_keyboard = [[KeyboardButton(text="עדכן על מה חדש", )]]
    
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    # set commands to the buttons
    # updater.bot.set_chat_menu_button(update.effective_chat.id,MenuButton(text="עדכן על מה חדש", command="update_news", type=MenuButton.COMMANDS))
    # updater.bot.set_chat_menu_button(update.effective_chat.id,MenuButton(text="שנה שעת התראה", command="change_time", type=MenuButton.COMMANDS))
    update.message.reply_text(CONTINUE_MESSAGE + COMMANDS_MENU, reply_markup=ReplyKeyboardMarkup(\
        [
            [
                KeyboardButton(text="שנה שעת התראה"),
                KeyboardButton(text="עזרה"),
            ],
        ]
    ))

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""
    הדברים הזמינים בשירות:
    """ + COMMANDS_MENU)
ADMIN_GROUP_ID = '-748011803'
def handle_news_update(update: Update, context: CallbackContext):
    # forword the message to the admin group
    updater.bot.forward_message(chat_id=ADMIN_GROUP_ID, from_chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

def update_news(update: Update, context: CallbackContext):
    message_text = update.message.text
    if(message_text == "עזרה"):
        help(update, context)
        return
    # elif(message_text == "שנה שעת התראה"):
    #     change_time(update, context)
    #     return
    else:
        handle_news_update(update, context)
    # print('update_news', update.effective_user.id, update.effective_chat.id, update.effective_message.text)
    # update.message.reply_text("""
    # ניתן לשלוח אליי טקסט או תמונות מהעסק שלך.
    # """)
from datetime import datetime
# def change_time(update: Update, context: CallbackContext, page=1):
#     page_count = 3
#     #page = 1
#     paginator = InlineKeyboardPaginator(
#         page_count,
#         current_page=page,
#         data_pattern='time_page#{page}'
#     )
#     if(page != 1):
#         update.message.edit_text(f'hey {page}', reply_markup=paginator.markup)
#     else:
#         update.message.reply_text("""
#         ניתן לשנות את השעה להתראה על מה חדש בשירות.
#         """,reply_markup=paginator.markup,)
    
def callback_query_handler(update, context):
    print('callback_query_handler', update)
    cqd = update.callback_query.data
    # if cqd.startswith('time_page'):
    #     page = int(cqd.split('#')[1])
    #     change_time(update.callback_query, context, page)
    #     return
    # elif cqd == ... ### for other buttons


updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('change_time', change_time))
updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler("עדכן על מה חדש", update_news))
# updater.dispatcher.add_handler(CommandHandler("שנה שעת התראה", change_time))
# updater.dispatcher.add_handler(CommandHandler("עזרה", help))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.document, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.sticker, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.video, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.location, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, update_news))
updater.dispatcher.add_handler(MessageHandler(Filters.audio, update_news))

# set bot commands:
langs_with_commands = {
    'en':{
            'start': 'Start bot 🚀',
            'help': 'Get bot instractions 📖',
        },
    'he':{
            'start': 'התחל את הבוט 🚀',
            'help': 'קבל הדרכה 📖',
    }
}

bot.delete_my_commands()
for language_code in langs_with_commands:
    bot.set_my_commands(
        language_code=language_code,
        commands=[
            BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
        ]
    )

# print(updater.bot.set_my_commands(commands=[
#                 BotCommand(command, description) for command, description in my_commands.items()
#             ]))

print('Starting bot...')
updater.start_polling()
print('Bot started')