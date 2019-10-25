from telegram import ParseMode
from global_vars import NO_VERB, NOT_FOUND
from helpers import log_missing
from output_processor import get_verb, get_missing_words
from query_generator import look_up_verb


def process_start_query(update, context):
    text = "<b>Gr-En reference</b>\n\n" \
           "for all info contact @sologuboved\n\n" \
           "https://github.com/sologuboved/greek_morphology"
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


def process_help_query(update, context):
    text = "Key in\n" \
           "<i>verb</i>\nto get links to Wordreference, Βικιλεξικό, and Wiktionary (no guarantee they won't 404)\n" \
           "/v <i>verb</i>\n(Modern Greek) if you wish to see its basic forms (praesens, futurum, aoristus)\n" \
           "/conj <i>verb</i>\nif you want its complete paradigm\n" \
           "/mw\n<i>optional number</i> to see (the optional number of items from) the list of previously " \
           "logged missing verbs"
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


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
