import telebot  
from config import token  

bot = telebot.TeleBot(token)  

@bot.message_handler(commands=['start']) 
def start(message): 
    bot.reply_to(message, "Привет! Я бот для управления чатом.") 

@bot.message_handler(commands=['ban']) 
def ban_user(message): 
    if message.reply_to_message:  
        chat_id = message.chat.id  
        user_id = message.reply_to_message.from_user.id 
        user_status = bot.get_chat_member(chat_id, user_id).status  
          
        if user_status in ['administrator', 'creator']: 
            bot.reply_to(message, "Невозможно забанить администратора.") 
        else: 
            bot.kick_chat_member(chat_id, user_id)  
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.") 
    else: 
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.") 

@bot.message_handler(func=lambda message: True) 
def check_for_link(message): 
    if 'http' in message.text or 'www' in message.text:   
        chat_id = message.chat.id 
        user_id = message.from_user.id 
        user_status = bot.get_chat_member(chat_id, user_id).status 
        if user_status in ['administrator', 'creator']: 
            bot.reply_to(message, "Невозможно забанить администратора.") 
        else: 
            bot.kick_chat_member(chat_id, user_id) 
            bot.reply_to(message, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.") 

@bot.message_handler(content_types=['new_chat_members']) 
def make_some(message): 
    bot.send_message(message.chat.id, 'Привет! Я принял нового пользователя!') 
    bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=True)

bot.infinity_polling(none_stop=True)
