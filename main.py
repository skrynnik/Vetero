'''
Telegram app weather bot on API
'''
import os

import telebot
import pyowm


TelebotToken = os.environ['TelebotToken']

bot = telebot.TeleBot(TelebotToken)

OWMToken = os.environ['OWMToken']
owm = pyowm.OWM(OWMToken)
owm.set_language('ru')


@bot.message_handler(commands=['start'])
def start(message):
    '''
    Reaction on the start command
    '''
    bot.send_message(message.chat.id, 'Введите название города')


@bot.message_handler(content_types=['text'])
def show_weather(message):
    '''
    Shows weather
    '''
    try:
        owm.weather_at_place(message.text)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, 'Такого города не существует')
        return

    weather = owm.weather_at_place(message.text).get_weather()
    detailed_status = weather.get_detailed_status()
    res = 'В городе ' + message.text + ' сейчас ' + detailed_status + '\n'

    temp = weather.get_temperature('celsius')
    temp.pop('temp_kf')
    temp = {elem: str(round(temp[elem] / 5, 1) * 5) for elem in temp}
    res += 'Средняя температура: ' + temp['temp'] + '°C'
    if temp['temp_max'] != temp['temp']:
        res += '\n' + 'Максимальная температура: ' + temp['temp_max'] + '°C'
    if temp['temp_min'] != temp['temp']:
        res += '\n' + 'Минимальная температура: ' + temp['temp_min'] + '°C'

    bot.send_message(message.chat.id, res)


bot.polling(none_stop=True)
