import telebot
import config
from telebot import types
from string import Template
bot=telebot.TeleBot(config.TG_TOKEN)


user_data={}
class User:
	def __init__(self,name):
		self.name=name
		self.msg=None
		self.phone=None



@bot.message_handler(commands=['start', 'help'])
def echo_all(message):
	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn_rasp = types.KeyboardButton("📋 Reyslar jadvali", )
	btn_message = types.KeyboardButton("✉️ Murojat qoldirish")
	btn_phone=types.KeyboardButton("☎ Malumot uchun telefonlar")
	btn_site=types.KeyboardButton("🌐 Aeroport web sayti")
	markup.add(btn_rasp,btn_message,btn_phone,btn_site)
	bot.send_message(message.chat.id, "Assalomu aleykum, Farg'ona xalqaro aeroportining rasmiy botiga xush kelibsiz!",
					 reply_markup=markup)


@bot.message_handler(content_types=['text'])
def first_step(message):
	if message.text=="✉️ Murojat qoldirish":
		markup=types.ReplyKeyboardRemove(selective=False)
		msg=bot.send_message(message.chat.id, "Ismingiz?", reply_markup=markup)
		bot.register_next_step_handler(msg,second_step)

	elif message.text=="📋 Reyslar jadvali":
		#photo=open('img/rasp.jpg', 'rb')
		bot.send_message(message.chat.id,'Reyslar vaqtincha bekor qilingan!')

	elif message.text=="🛫 ️Bosh Sahifa":
		echo_all(message)

	elif message.text=="☎ Malumot uchun telefonlar":
		bot.send_message(message.chat.id, "Malumot uchun telefon: +998 73 241-60-04")
	elif message.text == "🌐 Aeroport web sayti":
		markup=types.InlineKeyboardMarkup(row_width=2)
		btn_site = types.InlineKeyboardButton(text="ferganaairport.uz", url="https://ferganaairport.uz/")
		markup.add(btn_site)
		bot.send_message(message.chat.id, "Web saytni ochish uchun quyidagi tugmani bosing! 👇", reply_markup=markup)
	else:
		bot.reply_to(message,"Bunday buyruq mavjud emas...")

def second_step(message):
	try:
		chat_id=message.chat.id
		user_data[chat_id]=User(message.text)
		msg=bot.send_message(message.chat.id, "Raqamingiz? ")
		bot.register_next_step_handler(msg,third_step)
	except Exception as e:
		bot.reply_to(message, e)


def third_step(message):
	try:
		int(message.text)
		user=user_data[message.chat.id]
		user.phone=message.text
		msg=bot.send_message(message.chat.id, "Murojatingiz ? ")
		bot.register_next_step_handler(msg,last_step)
	except Exception as e:
		msg=bot.reply_to(message,"Iltimos raqamingizni to'g'ri kiriting!")
		bot.register_next_step_handler(msg, third_step)

def last_step(message):
	try:
		user=user_data[message.chat.id]
		user.msg=message.text
		markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn_home = types.KeyboardButton("🛫 ️Bosh Sahifa")
		markup.add(btn_home)
		bot.send_message(message.chat.id, "Rahmat. Murojatingizni yaqin daqiqalar ichida ko'rib chiqamiz...",
							 reply_markup=markup)
		bot.send_message(-1001428850814, reg_data(user,message.from_user.username), parse_mode="Markdown")

	except Exception as e:
		bot.send_message(message.chat.id, e)

def reg_data(user, fromuser):
	t=Template("Murojat qoldirgan foydalanuvchi: *$fromuser* \n Ismi: *$name* \nTelefoni: *$phone* \nMurojat matni: *$msg*")
	return t.substitute({
		'fromuser':'@'+str(fromuser),
		'name':user.name,
		'phone':user.phone,
		'msg':user.msg,
	})

bot.polling(none_stop=True)