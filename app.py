import telebot
import configparser
from telebot import formatting,custom_filters
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

    idvaga = ""
    telefone=""
    email=""

    texto = "Para se cadastrar na vaga digite o codigo da vaga disponivel em /vagas."
    bot.send_message(mensagem.chat.id, formatting.format_text(formatting.mbold(texto)), parse_mode='MarkdownV2')

    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand('name1', 'description for name1'),
            telebot.types.BotCommand('name2', 'description for name2'),
            telebot.types.BotCommand('name3', 'description for name3')
        ],
        scope=telebot.types.BotCommandScopeChat(mensagem.chat.id))





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