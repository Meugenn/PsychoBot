#coding=utf-8

import telebot
import config
import Psychojson
import json
import os
from flask import Flask, request
import logging
	

questions={}
killing={}
agressive={}

# with open('questions.json','r') as file:
# 	questions=json.loads(file.read())

# with open('killing.json','r') as file:
# 	killing = json.loads(file.read())
# with open('agressive.json','r') as file:
# 	agressive = json.loads(file.read())
markup = telebot.types.ReplyKeyboardMarkup()
markup.row('Да','Нет')

bot = telebot.TeleBot(config.token)




# def write_json(info,filename):
# 	try:
# 		data=json.load(open(filename))
# 	except:
# 		data = []

# 	data.append(info)
# 	with open(filename,'w') as file:
# 		json.dump(data, file, indent=2, ensure_ascii=False)

if "HEROKU" in list(os.environ.keys()):
	logger = telebot.logger
	telebot.logger.setLevel(logging.INFO)

	server = Flask(__name__)
	@bot.message_handler(commands=['start','help'])
	def bass_darci_about(message):
		markup_remove=telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.chat.id, '*Описание*', parse_mode= 'Markdown', reply_markup=markup_remove )
		bot.send_message(message.chat.id, 'Конструируя опросник, Басс вначале провел разграничения между враждебностью и агрессией. Враждебность была определена им как реакция отношения, скрытно-вербальная реакция, которой сопутствуют негативные чувства и негативная оценка людей и событий. Агрессию он определил, как ответ, содержащий стимулы, способные причинить вред другому существу. Дальнейшая дифференциация проводилась в направлении выделения подклассов внутри враждебности и агрессии. В результате Басс и Дарки выделили два вида враждебности (обида и подозрительность) и пять видов агрессии (физическая агрессия, косвенная агрессия, раздражение, негативизм и вербальная агрессия).' )
		bot.send_message(message.chat.id, '*Инструкция*',parse_mode= 'Markdown' )
		bot.send_message(message.chat.id, 'Опросник состоит из 75 утверждений, на которые Вам необходимо ответить "да" или "нет".' )



	@bot.message_handler(commands=['test_start'])
	def test_start(message):
		bot.send_message(message.chat.id, 'Начинаем тест')
		questions[message.chat.id]=0
		killing[message.chat.id]=0
		agressive[message.chat.id]=0
		test(message)


	@bot.message_handler(regexp='Да')
	def response_writer(message):
		try:

			if int(questions[message.chat.id])<75:
				a = Psychojson.l[questions[message.chat.id]]["Key"]

				if a== "Физическая агрессия":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Раздражение":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Вербальная агрессия":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])

				if a == "Обида":
					killing[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Подозрительность":
					killing[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])

				questions[message.chat.id]+=1
					
				try:
					test(message)
				except IndexError:
					result_agr(message)
			else:
				result_agr(message)
		except KeyError:
			bot.send_message(message.chat.id, 'Извините, программист-раздолбай перезапустил бота.\n Пожалуйста, начните тест заново коммандой /test_start')

	@bot.message_handler(regexp='Нет')
	def response_writer(message):
		try:
			if int(questions[message.chat.id])<75:
				a = Psychojson.l[questions[message.chat.id]]["Key"]

				if a== "Физическая агрессия":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Раздражение":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Вербальная агрессия":
					agressive[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])

				if a == "Обида":
					killing[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])
				if a =="Подозрительность":
					killing[message.chat.id]+=int(Psychojson.l[questions[message.chat.id]][message.text])

				questions[message.chat.id]+=1
					
				try:
					test(message)
				except IndexError:
					result_agr(message)
			else:
				result_agr(message)
		except KeyError:
			bot.send_message(message.chat.id, 'Извините, программист-раздолбай перезапустил бота.\n Пожалуйста, начните тест заново коммандой /test_start')





	def test(message):
		bot.send_message(message.chat.id, Psychojson.l[questions[message.chat.id]]['Question'],reply_markup=markup)



	def result_agr(message):
		markup_remove=telebot.types.ReplyKeyboardRemove()
		bot.send_message(message.chat.id, 'Тест закончен', reply_markup=markup_remove)
		bot.send_message(message.chat.id, '*Интерпретация результатов теста*:',parse_mode= 'Markdown')
		bot.send_message(message.chat.id,'Нормой агрессивности является величина ее индекса, равная 21 ± 4, а враждебности – 6-7 ± 3.')
		bot.send_message(message.chat.id,'*Ваш результат*:',parse_mode= 'Markdown')
		bot.send_message(message.chat.id,'Агрессивность: {}'.format((agressive[message.chat.id])))
		bot.send_message(message.chat.id,'Враждебность: {}'.format((killing[message.chat.id])))

	@server.route('/' + token, methods=['POST'])
	def getMessage():
		bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
		return "!", 200
	@server.route("/")
	def webhook():
	   bot.remove_webhook()
		bot.set_webhook(url='https://your_heroku_project.com/' + TOKEN)
		return "!", 200
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
else:
	# если переменной окружения HEROKU нету, значит это запуск с машины разработчика.  
	# Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
	bot.remove_webhook()
	bot.polling(none_stop=True)
