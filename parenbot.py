#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A telegram bot that hates unmatched parentheses.

TOKEN=""

from telegram.ext import Updater
import logging

from telegram import Update
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters

logging.basicConfig(
        format='[%(levelname)s] %(asctime)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def log(bot, update):
	c = update.message.chat
	if "private" not in update.message.chat.type:
		logger.info('<%s %s (%s@%s)> %s' % (c.first_name, c.last_name, c.username, c.title, c.text))
	else:
		logger.info('<%s %s (%s)> %s' % (c.first_name, c.last_name, c.username, c.text))

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def str_make (str_, length):
	return str_ * length

def balance(update: Update, context: CallbackContext):
	#log (bot, update)
	openbrckt = ('<([{（［｛⦅〚⦃“‘‹«「〈《【〔⦗『〖〘｢⟦⟨⟪⟮⟬⌈⌊⦇⦉❛❝❨❪❴❬❮❰❲'
		     '⏜⎴⏞〝︵⏠﹁﹃︹︻︗︿︽﹇︷〈⦑⧼﹙﹛﹝⁽₍⦋⦍⦏⁅⸢⸤⟅⦓⦕⸦⸨｟⧘⧚⸜⸌⸂⸄⸉᚛༺༼')
	clozbrckt = ('>)]}）］｝⦆〛⦄”’›»」〉》】〕⦘』〗〙｣⟧⟩⟫⟯⟭⌉⌋⦈⦊❜❞❩❫❵❭❯❱❳'
		     '⏝⎵⏟〞︶⏡﹂﹄︺︼︘﹀︾﹈︸〉⦒⧽﹚﹜﹞⁾₎⦌⦎⦐⁆⸣⸥⟆⦔⦖⸧⸩｠⧙⧛⸝⸍⸃⸅⸊᚜༻༽')
	parenmap  = dict(zip(openbrckt,clozbrckt))
	stack = []
	bad = False

	for ch in update.effective_message.text:
		if ch in parenmap:
			stack.append(ch)
		elif ch in parenmap.values():
			if not stack or stack[-1] != parenmap[ch]:
					bad = True
			else:
				stack.pop()
	close = ''.join(map(parenmap.__getitem__, reversed(stack)))
	if close:
		update.effective_message.reply_text(f"(╯°□°）╯ {close}" if bad else f"{close} ○(￣□￣○)")

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.text & (~Filters.command), balance))
	dp.add_error_handler(error)

	updater.idle()
	
if __name__ == '__main__':
	main()
