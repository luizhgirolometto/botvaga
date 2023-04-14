import telebot
from telebot import formatting

def createquery(ans):
    texto = ""
    for i in ans:
        id = i[0]
        titulo = i[1]
        descricao = i[2]
        data_publicacao = i[3]
        texto += "Código " + str(id) + " | " +  str(titulo) + " | " +  str(descricao) + " | " + str(data_publicacao) + "\n\n"
        message = "Recebido 📖 informações sobre as vagas:\n\n" + texto

    return message
