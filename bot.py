import telebot as tb
import parse as p

# TODO: telebot для color palettes
# (бот сможет отправлять картинку с палитрой по запросу)

# token, полученный от BotFather, нельзя никому показывать!!!
token = "XXX:YYY"
bot = tb.TeleBot(token=token)


@bot.message_handler(commands=["start"])
def start(message):
    markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = tb.types.KeyboardButton("Вечер в хату")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "И тебе не хворать!", reply_markup=markup)

message_commands = [
    "Рандом!", 
    "Теплые цвета", 
    "Холодные цвета", 
    "Пастельные цвета", 
    "Яркие цвета"
]
commands = [
    None, 
    "warm-colors", 
    "cool-colors", 
    "pastel-color", 
    "contrasting-color"
]

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    txt = message.text
    if txt == "Вечер в хату":
        markup = tb.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = tb.types.KeyboardButton("Рандом!")
        btn2 = tb.types.KeyboardButton("Теплые цвета")
        btn3 = tb.types.KeyboardButton("Холодные цвета")
        btn4 = tb.types.KeyboardButton("Пастельные цвета")
        btn5 = tb.types.KeyboardButton("Яркие цвета")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, "Выберите категорию!", reply_markup=markup)
    elif txt in message_commands:
        command = commands[message_commands.index(txt)]
        msg = p.get_random(command)
        with open("tmp.jpg", "rb") as file:
            bot.send_photo(message.from_user.id, file, msg)
    elif txt == "Назад":
        get_text_messages()
    else:
        bot.send_message(message.from_user.id , "Не понял")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть