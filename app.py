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

##########################################################################################################



class User:
    def __init__(self,idvaga,tel,email):
        self.tel = tel
        self.email = email
        self.idvaga = idvaga



@bot.message_handler(commands=["candidatar"])
def insert(mensagem):
    # Criar o formulário com os campos personalizados

    msg = bot.send_message(mensagem.chat.id, "Vamos começar?, preencha o formulário abaixo \n\n"
                                             "Primeiramente digite codigo da vaga desejada")
    bot.register_next_step_handler(msg, get_vaga)

def get_vaga(mensagem):
    # Pedir o telefone
    msg = bot.send_message(mensagem.chat.id, "Qual é o seu telefone? ex: 4699990000")
    bot.register_next_step_handler(msg, get_tel)
    User.idvaga = mensagem.text

    print(User.idvaga)



def get_tel(mensagem):
    tel = mensagem.text
    # Pedir o email do usuário
    msg = bot.send_message(mensagem.chat.id, "Qual é o seu email?")
    bot.register_next_step_handler(msg, end)
    User.tel = mensagem.text
    print(User.tel)

def end(mensagem):

    # Exibir uma mensagem de agradecimento e finalizar o formulário
    bot.send_message(mensagem.chat.id, "Obrigado por preencher o formulário.")
    User.email = mensagem.text
    print(User.email)

    insert_data(mensagem)


def insert_data(mensagem):


    fullname = mensagem.chat.first_name + mensagem.chat.last_name

    vaga_id = int(User.idvaga)
    nome = fullname
    email = User.email
    telefone = User.tel

    # create the tuple with all the params interted by the user
    params = (vaga_id,nome,email,telefone)

    # Create the UPDATE query, we are updating the product with a specific id so we must put the WHERE clause
    sql_command = "INSERT INTO candidaturas VALUES (%s, %s, %s, %s);"  # the initial NULL is for the AUTOINCREMENT id inside the table
    crsr.execute(sql_command, params)  # Execute the query
    conn.commit()  # Commit the changes

    # If at least 1 row is affected by the query we send specific messages
    if crsr.rowcount < 1:
        texto = "Algo deu errado! tente novamente"
        bot.send_message(mensagem.chat.id, texto)
    else:
        texto = "Tudo certo! inserido corretamente"
        bot.send_message(mensagem.chat.id, texto)



#####################################################################################################################

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


########################################################################################################################

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
        markup.add('/vagas','/candidatar','/consulta')
        msg = bot.send_message(mensagem.chat.id,'Escolha uma das opções abaixo:',reply_markup=markup)

        print(mensagem.chat.first_name, mensagem.chat.last_name)


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