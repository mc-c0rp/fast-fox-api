import telebot
import fox
import ai
import re
 
VERSION = '0.1'
LAST_PUBLIC_UPDATE = '09.12.24'
UPDATES = ['<strong>0.1</strong> - Создание бота, добавлены команды <strong>/sport</strong>, <strong>/send</strong> и <strong>/whats_new</strong>.']

API_TOKEN = '7986878035:AAFLAcjK4G9sa428TNdLcx12iYn7wqGaD5A'  # Load token from environment variable


bot = telebot.TeleBot(API_TOKEN)

# Use user_id as the key to ensure uniqueness and presence
state = {}

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        f"Привет, <strong>{message.from_user.first_name}</strong>.\n"
        f"Здесь ты можешь управлять самокатами, впрочем, тоже самое что и в Атоме.\n"
        f"Fox bot ver. {VERSION} | Fox api ver. {fox.VERSION} | Ai ver. {ai.VERSION} | {LAST_PUBLIC_UPDATE}"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

@bot.message_handler(commands=['whats_new'])
def whats_new(message: telebot.types.Message):
    text = ''
    for line in UPDATES:
        text += f'{line}\n'
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['cancel'])
def cancel(message: telebot.types.Message):
    global state
    user_id = message.from_user.id

    if user_id in state:
        state.pop(user_id)
        bot.reply_to(message, 'Действие успешно отменено.')
    else:
        bot.reply_to(message, 'Не удалось отменить действие, так как его не существует.')

@bot.message_handler(commands=['sport'])
def sport(message):
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
    text = 'Доступные команды:\n'
    for index, command in enumerate(fox.COMMANDS):
        text += f'<strong>{index}</strong>. <code>{command}</code>.\n'
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def handle_message(message:telebot.types.Message):
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

                        fox.send_command(scooter, command, 0, 2)
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