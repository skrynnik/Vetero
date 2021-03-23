import telebot
import pyowm
import os

# Set Telebot token with os.environ
TelebotToken = os.environ['TelebotToken']
bot = telebot.TeleBot(TelebotToken)

# Set OpenWeatherMap token with os.environ and russian language
OWMToken = os.environ['OWMToken']
owm = pyowm.OWM(OWMToken)
owm.set_language('ru')

# Set start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите название города')

# Weather command
@bot.message_handler(content_types=['text'])
def weather(message):

    # Check if the city even exists
    try:
        owm.weather_at_place(message.text)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, 'Такого города не существует')
        return

    # Get weather and detailed status
    weather = owm.weather_at_place(message.text).get_weather()
    detailed_status = weather.get_detailed_status()
    res = 'В городе ' + message.text + ' сейчас ' + detailed_status + '\n'

    # Get temperature
    temp = weather.get_temperature('celsius')
    temp = {round(float(str(temp[i]))) for i in temp}
    res += 'Средняя температура ' + str(temp['temp']) + '°C\n'
    if temp['temp_max'] != temp['temp']:
        res += 'Максимальная температура ' + str(temp['temp_max']) + '°C\n'
    if temp['temp_min'] != temp['temp']:
        res += 'Минимальная температур ' + str(temp['temp_min']) + '°C\n'

    # Send results
    bot.send_message(message.chat.id, res)

# Set nonstop polling
bot.polling(none_stop=True)
