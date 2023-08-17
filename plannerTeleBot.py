import telebot
from telebot import types
from plannerBotConfig import API_KEY

bot = telebot.TeleBot(API_KEY)

tasks = []
task_status = []
user_states = {}
user_chat_ids = []


@bot.message_handler(commands=['start'])
def start_command(message):
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text='Add Note✍️')
    btn2 = types.KeyboardButton(text='Mark as complete✔️')
    btn3 = types.KeyboardButton(text='Delete the notes❌')
    btn4 = types.KeyboardButton(text='See all notes📔')
    keybord.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, 'Hello! I am a bot which can help you plan your day⏰', reply_markup=keybord)
    if message.chat.id not in user_chat_ids:
        user_chat_ids.append(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Add Note✍️')
def add_note_handler(message):
    user_states[message.chat.id] = 'add_note'
    bot.send_message(message.chat.id, 'Write your note:')


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'add_note')
def process_note(message):
    note = message.text
    tasks.append(note)
    task_status.append(False)
    user_states[message.chat.id] = None
    bot.send_message(message.chat.id, 'Note added successfully!')


@bot.message_handler(func=lambda message: message.text == 'Mark as complete✔️')
def mark_note_handler(message):
    if not tasks:
        bot.send_message(message.chat.id, 'Here is empty yet')
    else:
        for index, task in enumerate(tasks, start=1):
            bot.send_message(message.chat.id, f'{index}. {task}')
            user_states[message.chat.id] = 'mark_complete'
        bot.send_message(message.chat.id, 'Write the number of the task you completed')


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'mark_complete')
def marking_note(message):
    user_mark_choice = message.text
    user_mark_choice = int(user_mark_choice)
    if 1 <= user_mark_choice <= len(tasks):
        task_status[user_mark_choice - 1] = True
        bot.send_message(message.chat.id, 'Note was marked as completed✔️')
        user_states[message.chat.id] = None
    else:
        bot.send_message(message.chat.id, 'Invalid task number')
        user_states[message.chat.id] = None


@bot.message_handler(func=lambda message: message.text == 'Delete the notes❌')
def see_note_handler(message):
    if not tasks:
        bot.send_message(message.chat.id, 'Here is empty yet😕')
    else:
        tasks.clear()
        task_status.clear()
        bot.send_message(message.chat.id, 'Notes have been successfully deleted👍')


@bot.message_handler(func=lambda message: message.text == 'See all notes📔')
def see_note_handler(message):
    if not tasks:
        bot.send_message(message.chat.id, 'Here is empty yet')
    else:
        for index, (task, status) in enumerate(zip(tasks, task_status), start=1):
            status_str = 'Complete' if status else 'Incomplete'
            if status_str == 'Complete':
                bot.send_message(message.chat.id, f'<s>{index}. {task} - {status_str}</s>', parse_mode='html')
            else:
                bot.send_message(message.chat.id, f'{index}. {task} - {status_str}')
                print("hello world")


bot.polling(none_stop=True)
