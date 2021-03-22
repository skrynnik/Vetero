import telebot
import pyowm

# Set Telebot token

bot = telebot.TeleBot('1767474938:AAEuXh-O6gHKuCBD2jJrosoA1RxB2FWYri0')

# Set OpenWeatherMap token, russian language

owm = pyowm.OWM('37604f123c985275529e2945d613d23f')
owm.set_language('ru')

# Set start command

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите название города')

# Weather command

@bot.message_handler(content_types = ['text'])
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

    res += 'Средняя температура ' + str(temp['temp']) + '\n'

    if temp['temp_max'] != temp['temp']:
        res += 'Максимальная температура ' + str(temp['temp_max']) + '\n'
    if temp['temp_min'] != temp['temp']:
        res += 'Минимальная температур ' + str(temp['temp_min']) + '\n'

    bot.send_message(message.chat.id, res)

    return

bot.polling(none_stop=True)