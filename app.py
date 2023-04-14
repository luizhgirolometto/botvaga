import telebot
import configparser
from telebot import formatting,types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

import MySQLdb
import createquery



API_TOKEN = '6223925413:AAFfD803r7s-8uXduSqafafx5stuQKbXrDE'
bot = telebot.TeleBot(API_TOKEN)

### Initializing Configuration
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read('config.ini')

# Read values for MySQLdb
HOSTNAME = config.get('default', 'hostname')
USERNAME = config.get('default', 'username')
PASSWORD = config.get('default', 'password')
DATABASE = config.get('default', 'database')

class User:
    def __init__(self, tel):
        self.tel = tel
        self.email = None



@bot.message_handler(commands=["cadastrar"])
def insert(mensagem):
    # Criar o formulário com os campos personalizados

    msg = bot.send_message(mensagem.chat.id, "Vamos começar?, preencha o formulário abaixo \n\n"
                                             "Primeiro o seu telefone?")
    bot.register_next_step_handler(msg, get_tel)

def get_tel(mensagem):
    # Pedir o telefone
    tel = mensagem.text
    msg = bot.send_message(mensagem.chat.id, "Qual é o seu nome?")
    bot.register_next_step_handler(msg, get_email)

    print(tel)


def get_email(mensagem):
    # Pedir o email do usuário
    msg = bot.send_message(mensagem.chat.id, "Qual é o seu email?")
    bot.register_next_step_handler(msg, get_telefone)


def get_telefone(mensagem):
    # Pedir o telefone do usuário
    msg = bot.send_message(mensagem.chat.id, "Qual é o seu telefone?")
    bot.register_next_step_handler(msg, end)


def end(mensagem):
    # Exibir uma mensagem de agradecimento e finalizar o formulário
    bot.send_message(mensagem.chat.id, "Obrigado por preencher o formulário.")


@bot.message_handler(commands=["vagas"])
def vagas(mensagem):
    crsr.execute("SELECT * FROM vagas")
    res = crsr.fetchall()

    if (res):
        texto = createquery.createquery(res)
        bot.send_message(mensagem.chat.id, texto)

    else:
        texto = "Nenhuma vaga encontrada."
        bot.send_message(mensagem.chat.id, formatting.format_text(formatting.mbold(texto)),parse_mode='MarkdownV2')


#funcao que le a msg de entrada
def start(mensagem):
    return True

#msg de boas vindas e seletores
@bot.message_handler(func=start)
def responder(mensagem):

        bot.send_message(mensagem.chat.id,'Bem vindo  ao sistema de Vagas da Empresa:\n\n'
                                     'VAGAS - LISTAR AS VAGAS \n'
                                     'CADASTRO - CADASTRE-SE EM UMA VAGA \n'
                                     'CONSULTA - CONSULTE A SUA CANDIDATURA \n \n')

        chat_id = mensagem.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/vagas','/cadastrar','/consulta')
        msg = bot.send_message(mensagem.chat.id,'Escolha uma das opções abaixo:',reply_markup=markup)

def create_database(query):
    try:
        crsr_mysql.execute(query)
        print("Database created successfully")
    except Exception as e:
        print(f"WARNING: '{e}'")


##### MAIN #####
if __name__ == '__main__':
    try:
        print("Initializing Database...")
        conn_mysql = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD)
        crsr_mysql = conn_mysql.cursor()

        query = "CREATE DATABASE " + str(DATABASE)
        create_database(query)
        conn = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE)
        crsr = conn.cursor()


        sql_command = """CREATE TABLE IF NOT EXISTS orders ( 
            id INTEGER PRIMARY KEY AUTO_INCREMENT, 
            product VARCHAR(200),
            quantity INT(10), 
            LAST_EDIT VARCHAR(100));"""

        crsr.execute(sql_command)
        print("All tables are ready")
        print("Bot Started...")


    except Exception as error:
        print('Cause: {}'.format(error))


bot.infinity_polling()