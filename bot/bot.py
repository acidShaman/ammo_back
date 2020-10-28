import telegram

try:
    bot = telegram.Bot('1298284330:AAFfK-PbssGsSVKHo9myaJl4NNOUHevg9M0')
    # print(bot.get_me())
    chat_id = bot.get_updates()[-1].message.chat_id
except telegram.error.TimedOut as err:
    print(err)


def send_message(text):
    bot.send_message(chat_id=chat_id, text=text)