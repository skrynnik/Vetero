import telebot
import pyowm

bot = telebot.TeleBot('Your token')

owm = pyowm.OWM('Your token')
owm.set_language('ru')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите название города')

@bot.message_handler(content_types = ['text'])
def weather(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')
        res = (
            'В городе ' + message.text + ' сейчас ' + w.get_detailed_status() + '\n' + 
            'Средняя температура ' + str(temp['temp']) + '\n' + 
            'Максимальная температура ' + str(temp['temp_max']) + '\n' + 
            'Минимальная температура ' + str(temp['temp_min'])
        )
        bot.send_message(message.chat.id, res)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, 'Такого города не существует')

bot.polling(interval = 5)
