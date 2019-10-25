from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from helpers import write_pid
from input_processor import process_verb_query
from output_processor import get_links
from tkn import TOKEN


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Get Gr-En reference")


def send_minimalistic_verb(update, context):
    query = update['message']['text'].split()
    process_verb_query(context.bot, update, query, minimalistic=True)


def send_verb_paradigm(update, context):
    query = update['message']['text'].split()
    process_verb_query(context.bot, update, query, minimalistic=False)


def send_links(update, context):
    word = update.message.text
    update.message.reply_text(get_links(word))


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    verb_handler = CommandHandler('v', send_minimalistic_verb)
    conjug_handler = CommandHandler('conjug', send_verb_paradigm)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(verb_handler)
    dispatcher.add_handler(conjug_handler)

    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_links))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
