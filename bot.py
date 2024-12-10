import telebot
import fox
import ai
import re
import threading
import time

VERSION = '0.1.1'
LAST_PUBLIC_UPDATE = '10.12.24'
UPDATES = ['<strong>0.1</strong> - Создание бота, добавлены команды <strong>/sport</strong>,<strong>/commands</strong> , <strong>/send</strong> и <strong>/whats_new</strong>.']

NOT_VERIF_TEXT = f"Я не могу найти тебя в моей базе, отправь запрос на <strong>добавление</strong> с помощью команды /verif."

API_TOKEN = '7986878035:AAFLAcjK4G9sa428TNdLcx12iYn7wqGaD5A'  # Load token from environment variable


bot = telebot.TeleBot(API_TOKEN)

# Use user_id as the key to ensure uniqueness and presence
state = {}

def check_permission(message):
	user_id = message.chat.id
	
	with open("users.txt", 'r') as f:
		users = f.read()
	users.split("\n")
	
	if str(user_id) not in users:
		return 0

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
    welcome_text = (
        f"Привет, <strong>{message.from_user.first_name}</strong>.\n"
        f"Здесь ты можешь управлять самокатами, впрочем, тоже самое что и в Атоме.\n"
        f"Fox bot ver. {VERSION} | Fox api ver. {fox.VERSION} | Ai ver. {ai.VERSION} | {LAST_PUBLIC_UPDATE}"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

@bot.message_handler(commands=['verif'])
def verif(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Запрос отправлен! Ожидай одобрения.')
    bot.send_message(1729435753, f'Запрос на верефикицаю от пользователя:\n{message.from_user.first_name} {message.from_user.last_name}\n@{message.from_user.username} | <code>{message.from_user.id}</code>\n(одобрить можно через /verif_bot)', parse_mode='HTML')

@bot.message_handler(commands=['verif_user'])
def verif_user(message: telebot.types.Message):
    id = int(message.text.replace('/verif_user ', ''))
    with open("users.txt", 'w+') as f:
        ff = f.read()
        ff += f'\n{id}'
        f.write(ff)
    bot.send_message(message.chat.id, 'Успешно одобрено!')
    bot.send_message(id, 'Твой запрос успешно одобрили!') 

@bot.message_handler(commands=['id'])
def id(message: telebot.types.Message):
	bot.send_message(message.chat.id, f'{str(message.from_user.id)}\nchat-id: {str(message.chat.id)}')

@bot.message_handler(commands=['whats_new'])
def whats_new(message: telebot.types.Message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
	
    text = ''
    for line in UPDATES:
        text += f'{line}\n'
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['cancel'])
def cancel(message: telebot.types.Message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
    global state
    user_id = message.from_user.id

    if user_id in state:
        state.pop(user_id)
        bot.reply_to(message, 'Действие успешно отменено.')
    else:
        bot.reply_to(message, 'Не удалось отменить действие, так как его не существует.')

@bot.message_handler(commands=['sport'])
def sport(message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
    user_id = message.from_user.id
    welcome_text = (
        f"<strong>{message.from_user.first_name}</strong>, на какой самокат пиздануть спорт режим? (F0XXX)\n(Отправьте /cancel чтобы отменить.)"
    )
    bmsg = bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')
    print(bmsg)  

    state[user_id] = {
        "type": "sport",
        "msg_id": bmsg.message_id 
    }

@bot.message_handler(commands=['send'])
def send(message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
    user_id = message.from_user.id
    welcome_text = (
        f"<strong>{message.from_user.first_name}</strong>, на какой самокат отправить команду? (F0XXX)\n(Отправьте /cancel чтобы отменить.)"
    )
    bmsg = bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')
    print(bmsg)  

    state[user_id] = {
        "type": "command_scooter",
        "msg_id": bmsg.message_id 
    }

@bot.message_handler(commands=['commands'])
def comm(message: telebot.types.Message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
		
    text = 'Доступные команды:\n'
    for index, command in enumerate(fox.COMMANDS):
        text += f'<strong>{index}</strong>. <code>{command}</code>.\n'
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message:telebot.types.Message):
    result = check_permission(message)
    if result == 0:
        bot.send_message(message.chat.id, f"Привет, <strong>{message.from_user.first_name}</strong>.\n{NOT_VERIF_TEXT}", parse_mode='HTML')
        return
    
		
    global state
    user_id = message.from_user.id
    user_state = state.get(user_id)

    if user_state and user_state.get("type") == "sport":
        if 'f0' in message.text.lower() and int(message.text.lower().replace('f', '')) >= 1 and int(message.text.lower().replace('f', '')) <= 601:
            try:
                bot.delete_message(message.chat.id, message.id)
                bot.edit_message_text(
                    "<strong>Думаю</strong>...",
                    chat_id=message.chat.id,
                    message_id=user_state["msg_id"],
                    parse_mode="HTML"
                )
                bot.send_chat_action(message.chat.id, 'typing')
                state.pop(user_id)

                fox.send_command(message.text, 'MODE_SPORT', 0, 5)
                fox.send_command(message.text, 'MAX_SPEED_LIMIT_FROM_0_TO_63_KM/H', 63, 5)

                bot.edit_message_text(
                    "Готово!",
                    chat_id=message.chat.id,
                    message_id=user_state["msg_id"],
                    parse_mode="HTML"
                )

            except Exception as ex:
                bot.send_message(message.chat.id, f'ашипка!!!!\n{ex}')
    if user_state and user_state.get("type") == "command_scooter":
        if 'f0' in message.text.lower() and int(message.text.lower().replace('f', '')) >= 1 and int(message.text.lower().replace('f', '')) <= 601:
            try:
                bot.delete_message(message.chat.id, message.id)
                bot.edit_message_text(
                    "<strong>Думаю</strong>...",
                    chat_id=message.chat.id,
                    message_id=user_state["msg_id"],
                    parse_mode="HTML"
                )
                bot.send_chat_action(message.chat.id, 'typing')

                state[user_id]["type"] = 'command_code'
                state[user_id]["code"] = message.text.lower()

                bot.edit_message_text(
                    f"Теперь отправь мне команду, которую ты хочешь отправить на самокат (F{message.text.lower().replace('f', '')}).",
                    chat_id=message.chat.id,
                    message_id=user_state["msg_id"],
                    parse_mode="HTML"
                )

            except Exception as ex:
                bot.send_message(message.chat.id, f'ашипка!!!!\n{ex}')
    elif user_state and user_state.get("type") == "command_code":
                bot.delete_message(message.chat.id, message.id)
                bot.edit_message_text(
                    "<strong>Думаю</strong>...",
                    chat_id=message.chat.id,
                    message_id=user_state["msg_id"],
                    parse_mode="HTML"
                )
                bot.send_chat_action(message.chat.id, 'typing')
                
                if re.search(r'[a-zA-Z]', message.text):
                    scooter = user_state['code']

                    fox.send_command(scooter, message.text, 0, 2)
                    bot.delete_message(message.chat.id, user_state['msg_id'])
                    bot.send_message(message.chat.id, f'<strong>{message.from_user.first_name}</strong>, команда {message.text} была успешно отправлена на {scooter}!', parse_mode='HTML')
                elif re.search(r'[а-яА-Я]', message.text):
                    scooter = user_state['code']
                    key, command, conf = ai.find(message.text.lower(), fox.COMMANDS_RU)
                    if conf >= ai.threshold:
                        bot.edit_message_text(
                            f"<strong>Нейросеть</strong> определила команду {command} с уверенностью в {conf:.2f}, отправляю запрос в атом...",
                            chat_id=message.chat.id,
                            message_id=user_state["msg_id"],
                            parse_mode="HTML"
                        )   
                        background_thread = threading.Thread(target=fox.send_command, args=(scooter, command, 0, 2))
                        background_thread.start()

                        percent = 0.00
                        for i in range(13):
                            percent += 7.69
                            bot.edit_message_text(
                                f"<strong>Нейросеть</strong> определила команду {command} с уверенностью в {conf:.2f}, отправляю запрос в атом... ({percent:.1f}%)",
                                chat_id=message.chat.id,
                                message_id=user_state["msg_id"],
                                parse_mode="HTML"
                            ) 
                            time.sleep(0.5)

                        bot.delete_message(message.chat.id, user_state['msg_id'])
                        bot.send_message(message.chat.id, f'<strong>{message.from_user.first_name}</strong>, команда {command} была успешно отправлена на {scooter}!', parse_mode='HTML')
                    else:
                        bot.send_message(message.chat.id, f'К сожалению, я <strong>не</strong> нашел команду {message.text}, попробуй еще раз.\n(команды можно узнать в /commands)', parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, f'К сожалению, я <strong>не</strong> нашел команду {message.text}, попробуй еще раз.\n(команды можно узнать в /commands)', parse_mode="HTML")

if __name__ == '__main__':
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
    except Exception as e:
        print(f"Возникла ошибка: {e}")