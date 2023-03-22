import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pfm

# Start bot

TOKEN = "5948666656:AAFN18bT4t3AzpuY1JikmEf7v8QzAHcdAU4"
DEBUG_TOKEN = "5817633243:AAG_f7rwh3anUqnU5VgMLWXb4oB_OPaIqsE"

bot = telebot.TeleBot(DEBUG_TOKEN, parse_mode=None)

# Global variable e funcion

message_list = []

def clear_markup():
     if len(message_list) != 0:
          for mes in message_list:
               bot.edit_message_reply_markup(chat_id = mes.chat.id, message_id = mes.message_id)
               message_list.remove(mes)

def gen_markup(dict, n):
     markup = InlineKeyboardMarkup()
     markup.row_width = n
     for key in dict:
        markup.add(InlineKeyboardButton(key, callback_data=dict[key]))
     return markup

# Callback handler

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
     if call.data == "add_b":
          clear_markup()
          add_balance(call.message)

     elif call.data == "reg":
          clear_markup()
          registering(call.message)

     elif call.data == "bal":
          clear_markup()
          send_balances(call.message)

     elif call.data == "add_e":
          clear_markup()
          add_expense(call.message)

     elif call.data == "add_p":
          clear_markup()
          add_pm(call.message)

     elif call.data == "rem_e":
          clear_markup()
          remove_expense(call.message)

     else: 
          clear_markup()

# Start command

@bot.message_handler(commands=['start']) 
def send_welcome(message):

     clear_markup()

     users = pfm.get_users()

     if message.chat.id in users:
          string = "Bentornato " + message.chat.first_name + "!\n\nCosa vuoi fare?\n"
          markup = gen_markup({"Visualizza bilanci": "bal", "Aggiungi spesa": "add_e", "Rimuovi spesa": "rem_e"}, 3)

     else: 
          string = "Benvenuto " + message.chat.first_name + "!\n\n È la tua prima volta qui..."
          markup = gen_markup({"Registati": "reg"}, 1)

     Message = bot.send_message(message.chat.id, string, reply_markup=markup)
     message_list.append(Message)

# Registering command (hidden)

@bot.message_handler(commands=['reg']) 
def registering(message):
     users = pfm.get_users()
     if message.chat.id in users:
          bot.send_media_group(message.chat.id, "Utente già registrato")
          return
     
     bot.send_message(message.chat.id, "Inserisci nome bilancio:")

     @bot.message_handler(func=lambda m: True)
     def add_user(message):
          pfm.add_user(message.chat.id)
          pfm.add_balances(message.chat.id, message.text.lower())
          bot.send_message(message.chat.id, "Aggiunto!")

          bot.send_message(message.chat.id, "Inserisci metodo di pagamento:")

          @bot.message_handler(func=lambda m: True)
          def add_user2(message):
               pfm.add_pm(message.chat.id, message.text.lower())
               bot.send_message(message.chat.id, "Aggiunto!")
          bot.register_next_step_handler(message, add_user2)

     bot.register_next_step_handler(message, add_user)


# Balances command

@bot.message_handler(commands=['balances'])
def send_balances(message):
    
     clear_markup()

     balances_names = pfm.get_balances(message.chat.id)
     balances = pfm.calculate_balances(message.chat.id)
     pm_names = pfm.get_pm(message.chat.id)
     pm = pfm.calculate_pm(message.chat.id)

     string = "I tuoi bilanci:\n"
     for name in balances_names:
        balance = balances[name]
        string += pfm.add_capital_letter(str(name)) + ": " + "{:.2f}".format(balance) + "€" + "\n"
     
     string += "\n"

     string += "I tuoi metodi di pagamento:\n"
     for name in pm_names:
        el = pm[name]
        string += pfm.add_capital_letter(str(name)) + ": " + "{:.2f}".format(el) + "€" + "\n"

     markup = gen_markup({"Aggiungi bilancio": "add_b", "Aggiungi metodo": "add_p"}, 2)
    
     Message = bot.send_message(message.chat.id, string, reply_markup=markup)
     message_list.append(Message)

# Add balances command (hidden)

@bot.message_handler(commands=['add_b'])
def add_balance(message):
     bot.send_message(message.chat.id, "Inserisci nome bilancio:")
     balances = pfm.get_balances(message.chat.id)

     @bot.message_handler(func=lambda m: True)
     def add_balance_i(message):
          balance = message.text.split()[0].lower()
          if balance not in balances:
               pfm.add_balances(message.chat.id, balance)
               bot.send_message(message.chat.id, "Aggiunto!")
          else:
               bot.send_message(message.chat.id, "Bilancio già esistente")
     bot.register_next_step_handler(message, add_balance_i)

# Add pm command (hidden)

@bot.message_handler(commands=['add_p'])
def add_pm(message):
     bot.send_message(message.chat.id, "Inserisci metodo di magamento:")
     pm = pfm.get_balances(message.chat.id)

     @bot.message_handler(func=lambda m: True)
     def add_pm_i(message):
          el = message.text.split()[0].lower()
          if el not in pm:
               pfm.add_pm(message.chat.id, el)
               bot.send_message(message.chat.id, "Aggiunto!")
          else:
               bot.send_message(message.chat.id, "Bilancio già esistente")
     bot.register_next_step_handler(message, add_pm_i)

# Add command

@bot.message_handler(commands=['add'])
def add_expense(message):
    
     clear_markup()

     balances_names = pfm.get_balances(message.chat.id)
     pa_names = pfm.get_pm(message.chat.id)

     bot.send_message(message.chat.id, "Inserisci spesa:")

     @bot.message_handler(func=lambda m: True)
     def add(message):

          if(len(message.text.split()) <=5):
               return

          balance = message.text.split()[0].lower()
          payment_method = message.text.split()[1].lower()
          amount = message.text.split()[2]
          date = message.text.split()[3]
          category = message.text.split()[4].lower()
          description = message.text.split()[5].lower()

          if balance not in balances_names:
               bot.send_message(message.chat.id, "Nome bilancio non trovato")
               return

          if payment_method not in pa_names:
               bot.send_message(message.chat.id, "Metodo di pagamento non trovato")
               return

          pfm.add_expense([str(message.chat.id), balance, payment_method, amount, date, category, description])

          bot.send_message(message.chat.id, "Aggiunta!")

     bot.register_next_step_handler(message, add) 


@bot.message_handler(commands=['remove'])
def remove_expense(message):

    bot.send_message(message.chat.id, "Inserisci spesa da eliminare:")

    @bot.message_handler(func=lambda m: True)
    def remove(message):

          balance = message.text.split()[0].lower()
          payment_method = message.text.split()[1].lower()
          amount = message.text.split()[2]
          date = message.text.split()[3]
          category = message.text.split()[4].lower()
          description = message.text.split()[5].lower()

          flag = pfm.remove_expense([str(message.chat.id), balance, payment_method, amount, date, category, description])
          if(flag == True):
               bot.send_message(message.chat.id, "Rimossa!")
          else:
               bot.send_message(message.chat.id, "Spesa non trovata!")

    bot.register_next_step_handler(message, remove)
     
# Unknown command

@bot.message_handler(func=lambda message: True)
def unknown(message):
    
    clear_markup()

    bot.send_message(message.chat.id, "Sorry, I didn't understand that command.")
bot.infinity_polling()