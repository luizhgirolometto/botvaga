import telebot
import configparser
from telebot import formatting
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


@bot.message_handler(commands=["cadastrar"])
def insert(mensagem):
    # Criar o formulário com os campos personalizados


    mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    mrkplink.add(InlineKeyboardButton("Join our group 🚀", url="http://www.google.com.br" ))  # Added Invite Link to Inline Keyboard

    msg = bot.send_message(mensagem.chat.id, "Por favor, preencha o formulário abaixo .")
    bot.register_next_step_handler(msg, get_name)

def get_name(mensagem):
    # Pedir o nome do usuário

    msg = bot.send_message(mensagem.chat.id, "Qual é o seu nome?")
    bot.register_next_step_handler(msg, get_email)


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

    name = mensagem.chat.first_name


    texto =  "Bem vindo " + name + " ao sistema de Vagas da Empresa: \n \n" \
             "Escolha uma das opções abaixo \n\n" \
             "/vagas - Listar todas as vagas \n" \
             "/cadastrar - Cadastre-se para uma vaga \n" \
             "/consulta - Status da sua candidatura"

    #envia msg de boas vindas
    bot.send_message(mensagem.chat.id, formatting.format_text(formatting.mbold(texto)),parse_mode='MarkdownV2')

    # Create database function
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