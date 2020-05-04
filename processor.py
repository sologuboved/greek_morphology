from urllib.parse import quote
from telegram import ParseMode
from global_vars import NO_VERB, NOT_FOUND, WORDREF_LINK
from helpers import log_missing
from output_processor import get_verb, get_missing_words, get_fem_nom_pl
from query_generator import look_up_verb, look_up_fem_nom_pl


def process_start_query(update, context):
    text = "<b>Gr-En reference</b>\n\n" \
           "for all info contact @sologuboved\n\n" \
           "https://github.com/sologuboved/greek_morphology"
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


def process_help_query(update, context):
    text = "<b>Key in</b>\n\n" \
           "<i>verb</i>\nto get links to Wordreference, Βικιλεξικό, and Wiktionary (no guarantee they won't 404)\n\n" \
           "/v <i>verb (Modern Greek)</i>\nif you wish to see its basic forms (praesens, aoristus, futurum)\n\n" \
           "/conj <i>verb</i>\nif you want its complete paradigm\n\n" \
           "/mw <i>optional number</i> \nto see (the optional number of items from) the list of previously " \
           "logged missing verbs"
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


def process_verb_query(update, context, minimalistic):
    try:
        query = update['message']['text'].split()[1].strip()
    except IndexError:
        reply = NO_VERB
    else:
        paradigm = look_up_verb(query)
        if paradigm is None:
            log_missing(query)
            reply = NOT_FOUND
        else:
            reply = get_verb(paradigm, minimalistic)
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
    try:
        fem_nom_pl = get_fem_nom_pl(look_up_fem_nom_pl(word))
    except Exception as e:
        print(e)
        fem_nom_pl = str()
    paradigm = look_up_verb(word)
    if paradigm is None:
        paradigm = str()
    else:
        paradigm = get_verb(paradigm, minimalistic=True, appendix=True)
    update.message.reply_text(
        "https://www.wordreference.com/gren/{word}\n\n"
        "{wordref_link}\n\n"
        "<a href='https://el.wiktionary.org/wiki/{word}'>Βικιλεξικό</a> | "
        "<a href='https://en.wiktionary.org/wiki/{word}'>Wiktionary</a> | "
        "<a href='https://www.multitran.com/m.exe?l1=1&l2=38&s={word}'>Multitran</a> | "
        "<a href='https://translate.google.com/#view=home&op=translate&sl=el&tl=en&text={encoded_word}'>"
        "Google Translate</a>"
        "{fem_nom_pl}"
        "{paradigm}".format(
            word=word, wordref_link=WORDREF_LINK.format(word=word), encoded_word=quote(word), fem_nom_pl=fem_nom_pl, paradigm=paradigm
        ), disable_web_page_preview=True, parse_mode=ParseMode.HTML
    )
