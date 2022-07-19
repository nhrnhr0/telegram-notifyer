from typing import Dict
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import BotCommand, CallbackQuery, KeyboardButton, MenuButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram_bot_pagination import InlineKeyboardPaginator

from proj.secrects import *

class TelegramController:
    
    WELCOME_MESSAGE = "תודה שהצטרפת לשירות!\n" \
        "בנוסף אנחנו נזכיר לך פעם ביום בשעה %s לכתוב לנו מה חדש"
    CONTINUE_MESSAGE = "ניתן לשלוח לי בכל רגע מה חדש אצלך בעסק ותמונות מהעסק שלך."
    COMMANDS_MENU = """
        /start - להתחבר לשירות
        /help - להציג את הדרכה לשימוש בשירות
        /change_time - לשנות את השעה להתראה"""
    NOT_REGISTERED_USER_MESSAGE = "עליך להירשם לשירות לפני שתוכל לשלוח לי מה חדש אצלך בעסק ותמונות מהעסק שלך."
    updater = Updater(TELEGRAM_TOKEN,
                    use_context=True)
    bot = updater.bot
    registered_users = []
    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id, text=text)

    def start(self, update: Update, context: CallbackContext):
        from core.models import RegisteredUser, UnregisteredUser

        # if the user is not yet registered, show him a webcome message and add him to the list of registered users
        user = RegisteredUser.objects.filter(telegramId=update.effective_user.id)
        if user.count() == 0:
            UnregisteredUser.objects.get_or_create(telegramId=update.effective_user.id, defaults={'username':update.effective_user.username})
            update.message.reply_text(self.NOT_REGISTERED_USER_MESSAGE)
        else:
            user = user.first()
            notification_time = user.preferedNotificationTime
            update.message.reply_text(self.WELCOME_MESSAGE % notification_time)
            update.message.reply_text(self.CONTINUE_MESSAGE + self.COMMANDS_MENU, reply_markup=ReplyKeyboardRemove())
        # add keyboard with 2 buttons: "עדכן על מה חדש" and "שנה שעת התראה"
        
        # custom_keyboard = [['עדכן על מה חדש', 'שנה שעת התראה'], ['עזרה']]
        # custom_keyboard = [[KeyboardButton(text="עדכן על מה חדש", )]]
        
        # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        # set commands to the buttons
        # updater.bot.set_chat_menu_button(update.effective_chat.id,MenuButton(text="עדכן על מה חדש", command="update_news", type=MenuButton.COMMANDS))
        # updater.bot.set_chat_menu_button(update.effective_chat.id,MenuButton(text="שנה שעת התראה", command="change_time", type=MenuButton.COMMANDS))
            

    def help(self,update: Update, context: CallbackContext):
        update.message.reply_text("""
        הדברים הזמינים בשירות:
        """ + self.COMMANDS_MENU)
    ADMIN_GROUP_ID = '-748011803'
    def handle_news_update(self,update: Update, context: CallbackContext):
        # forword the message to the admin group
        self.updater.bot.forward_message(chat_id=self.ADMIN_GROUP_ID, from_chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    def update_news(self, update: Update, context: CallbackContext):
        message_text = update.message.text
        if(message_text == "עזרה"):
            help(update, context)
            return
        # elif(message_text == "שנה שעת התראה"):
        #     change_time(update, context)
        #     return
        else:
            self.handle_news_update(update, context)
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

    def __init__(self) -> None:
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        # updater.dispatcher.add_handler(CommandHandler('change_time', change_time))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        # updater.dispatcher.add_handler(CommandHandler("עדכן על מה חדש", update_news))
        # updater.dispatcher.add_handler(CommandHandler("שנה שעת התראה", change_time))
        # updater.dispatcher.add_handler(CommandHandler("עזרה", help))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_query_handler))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.photo, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.document, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.sticker, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.video, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.voice, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.location, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.contact, self.update_news))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.audio, self.update_news))

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

        self.bot.delete_my_commands()
        for language_code in langs_with_commands:
            self.bot.set_my_commands(
                language_code=language_code,
                commands=[
                    BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
                ]
            )

    # print(updater.bot.set_my_commands(commands=[
    #                 BotCommand(command, description) for command, description in my_commands.items()
    #             ]))
    def start_bot(self):
        print('start_bot')
        self.updater.start_polling()
        self.updater.idle()
        print('start_bot done')
        
    
tc= TelegramController()