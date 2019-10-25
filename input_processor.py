from telegram import ParseMode
from global_vars import NO_VERB, NOT_FOUND
from helpers import log_missing
from output_processor import process_verb_output
from query_generator import look_up_verb


def process_verb_query(bot, update, query, minimalistic):
    try:
        query = query[1].strip()
    except IndexError:
        reply = NO_VERB
    else:
        res = look_up_verb(query, minimalistic=minimalistic)
        if res is None:
            log_missing(query)
            reply = NOT_FOUND
        else:
            reply = process_verb_output(res, minimalistic)
    bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.HTML)
