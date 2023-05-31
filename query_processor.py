from urllib.parse import quote

from telegram.constants import ParseMode

from global_vars import NO_VERB, NOT_FOUND, WORDREF_LINK
from helpers import log_missing
from special_forms_processor import get_fem_nom_pl, get_verb
from special_forms_obtainer import look_up_fem_nom_pl, look_up_verb


async def process_start_query(update, context):
    text = """<b>Gr-En reference</b>
    

"for all info contact @sologuboved


"https://github.com/sologuboved/greek_morphology
"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


async def process_help_query(update, context):
    text = """<b>Key in</b>
    
<i>{word in any form}</i>
to get links to Wordreference, Lexigram, Βικιλεξικό, Wiktionary, Multitran & Google Translate 
(no guarantee they won't 404), and some basic forms (if available)

/p <i>{verb in any form}</i>
if you want its paradigm
"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.HTML)


async def process_verb_query(update, context, minimalistic):
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
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.HTML)


async def process_links_query(update, context):
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
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="""{wordref_link}
    
    
https://www.lexigram.gr/lex/newg/{word}

<a href='https://el.wiktionary.org/wiki/{word}'>Βικιλεξικό</a> |
<a href='https://en.wiktionary.org/wiki/{word}'>Wiktionary</a> |
<a href='https://www.multitran.com/m.exe?l1=1&l2=38&s={word}'>Multitran</a> |
<a href='https://translate.google.com/#view=home&op=translate&sl=el&tl=en&text={encoded_word}'>
Google Translate</a>
{fem_nom_pl}
{paradigm}
""".format(
            wordref_link=WORDREF_LINK.format(word=word),
            word=word,
            encoded_word=quote(word),
            fem_nom_pl=fem_nom_pl,
            paradigm=paradigm,
        ),
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )
