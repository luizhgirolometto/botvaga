def createquery(ans):
    texto = ""
    for i in ans:
        id = i[0]
        vaga = i[1]
        descricao = i[2]
        texto += "<b>" + str(id) + "</b> | " + "<b>" + str(vaga) + "</b> | " + "<b>" + str(
            descricao) + "</b> | " + "<b>"  "</b>\n\n "
    message = "<b>Recebido 📖 </b> informações sobre as vagas:\n\n" + texto
    return message
