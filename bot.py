from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from helpers import write_pid
from input_processor import process_verb_query, process_links_query, process_missing_words_query
from tkn import TOKEN


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Get Gr-En reference")


def send_minimalistic_verb(update, context):
    process_verb_query(update, context, minimalistic=True)


def send_verb_paradigm(update, context):
    process_verb_query(update, context, minimalistic=False)


def send_missing_words(update, context):
    process_missing_words_query(update, context)


def send_links(update, context):
    process_links_query(update)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    verb_handler = CommandHandler('v', send_minimalistic_verb)
    conjug_handler = CommandHandler('conj', send_verb_paradigm)
    missing_words_handler = CommandHandler('mw', send_missing_words)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(verb_handler)
    dispatcher.add_handler(conjug_handler)
    dispatcher.add_handler(missing_words_handler)

    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_links))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
