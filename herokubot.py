import logging
import os
from pprint import pprint

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

# Resolve message data to a readable name  taken from https://github.com/Whalepool/Natalia/blob/master/natalia.py

def get_name(update):
        try:
            name = update.message.from_user.first_name
        except (NameError, AttributeError):
            try:
                name = update.message.from_user.username
            except (NameError, AttributeError):
                logger.info("No username or first name.. wtf")
                return  ""
        return name

def start(bot, update):
    update.effective_message.reply_text("Hi!")


# def echo(bot, update):
#     update.effective_message.reply_text(update.effective_message.text)

def errors(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (str(update), error))

def clear_joins(bot, update):
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    chat_name = update.message.chat.title

    bot.delete_message(chat_id=chat_id, message_id=message_id)

# def new_post_rules(bot, update):
#     user_id = update.message.from_user.id
#     message_id = update.message.message_id
#     chat_id = update.message.chat.id
#     chat_name = update.message.chat.title
#     name = get_name(update)
#     new_chat_mem = update.message.new_chat_members

#     BOT_NAME = bot.username

#     for member in new_chat_mem:
#         new_member = member.username
#         if new_member == BOT_NAME:
#             return False
#         else:
#             logger.info("welcoming = "+name)
#             msg = ("Welcome to "+ str(chat_name) + " %s" % (member.name))+ '' + str(rules_list)
#             message = bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='MARKDOWN')
    
#     bot.delete_message(chat_id=chat_id, message_id=message_id)

#     pprint('Room: '+str(chat_name))
#     pprint('Chat_id: '+str(chat_id))

# def post_rules(bot, update):
#     user_id = update.message.from_user.id
#     message_id = update.message.message_id
#     chat_id = update.message.chat.id
#     chat_name = update.message.chat.title
#     name = get_name(update)
#     new_chat_mem = update.message.new_chat_members

#     BOT_NAME = bot.username


#     logger.info("printing rules manually")
#     msg =("Welcome to "+ str(chat_name) + '\n' +  str(rules_list))
#     bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='MARKDOWN')

#     pprint('Room: '+str(chat_name))
#     pprint('Chat_id: '+str(chat_id))




if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = str(os.getenv('BOT_TOKEN'))
    NAME = str(os.getenv('BOT_H_NAME'))

    ### SET RULES HERE
    rules_list ='''*This is bold*
•These are bullets
 
*More Bold*
•More bullets'''
    

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(MessageHandler(Filters.text, echo))
    #dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_post_rules))
    #dp.add_handler(CommandHandler('rules', post_rules))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, clear_joins))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, clear_joins))
    dp.add_error_handler(errors)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
