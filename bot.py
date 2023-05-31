from telegram.ext import Application, CommandHandler, MessageHandler, filters

from helpers import write_pid
from query_processor import process_help_query, process_links_query, process_start_query, process_verb_query
from userinfo import TOKEN


"""
help -  
p - paradigm
"""


async def start(update, context):
    await process_start_query(update, context)


async def send_ref(update, context):
    await process_help_query(update, context)


async def send_verb_paradigm(update, context):
    await process_verb_query(update, context, minimalistic=False)


async def send_links(update, context):
    await process_links_query(update, context)


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', send_ref))
    application.add_handler(CommandHandler('p', send_verb_paradigm))
    application.add_handler(MessageHandler(filters=filters.TEXT, callback=send_links))
    application.run_polling()


if __name__ == '__main__':
    write_pid()
    main()
