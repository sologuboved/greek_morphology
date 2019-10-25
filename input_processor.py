from telegram import ParseMode
from global_vars import NO_VERB, NOT_FOUND
from helpers import log_missing
from output_processor import get_verb, get_missing_words
from query_generator import look_up_verb


def process_verb_query(update, context, minimalistic):
    try:
        query = update['message']['text'].split()[1].strip()
    except IndexError:
        reply = NO_VERB
    else:
        res = look_up_verb(query, minimalistic=minimalistic)
        if res is None:
            log_missing(query)
            reply = NOT_FOUND
        else:
            reply = get_verb(res, minimalistic)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.HTML)


def process_missing_words_query(update, context):
    query = update['message']['text'].split()
    try:
        query = query[1]
    except IndexError:
        query = str()
    reply = get_missing_words(query)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)


def process_links_query(update):
    word = update.message.text
    update.message.reply_text('https://www.wordreference.com/gren/{}\n\n'
                              'https://el.wiktionary.org/wiki/{}\n\n'
                              'https://en.wiktionary.org/wiki/{}'.format(*[word] * 3))
