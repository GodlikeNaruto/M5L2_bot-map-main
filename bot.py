import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)
comands = ['/start', '/help', '/show_city', '/remember_city', '/show_my_cities']
color = 'blue'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """Доступные команды:  """)
    # Допиши команды бота
    for x in comands:
        bot.send_message(message.chat.id, x)


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    try :
        global color 
        city_name = message.text.split()[-1]
        manager.create_graph(f'{city_name}.png', city_name, color)
        bot.send_photo(message.chat.id, open (f'img/{city_name}.png', 'rb'))
    except:
        bot.send_message(message.chat.id, 'You need to type name of the city like: /show_city Moscow')
    

@bot.message_handler(commands=['color'])
def change_color(message):
    try :
        global color 
        color = message.text.split()[-1]
        bot.send_message(message.chat.id, f'Цвет маркера успешно заменен на {color}')
    except:
        bot.send_message(message.chat.id, 'You need to type name of the color like: /color blue')


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    try:
        user_id = message.chat.id
        city_name = message.text.split()[-1]
        if manager.add_city(user_id, city_name):
            bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
        else:
            bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')
    except:
        bot.send_message(message.chat.id, 'You need to type name of the city like: /remember_city Moscow')


@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    for city in cities:
        manager.create_graph(f'{city}.png', city)
        bot.send_photo(message.chat.id, open (f'img/{city}.png', 'rb'))
    

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
