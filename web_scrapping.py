#Importa requests para realizar abertura da página com resoluções capturadas
import requests
#Importa os para manipulação de arquivos e tabelas de dados
import os
#Importa date para verificar, e manipular, datetype(timestamp)
from datetime import *
#Importar time para verificar tempo de resposta de uma página
import time

#Função que faz o programa esperar pelo código de requisição 200 para qualquer
# get da página
def waitForSiteResponse(response, time, timewait):
    timer = 0
    while response.status_code != 200:
        time.sleep(timewait)
        timer += timewait
        if timer >= timeout and response.status_code != 200:
            print("Site não responsivo...\n"
                    "Fechando o programa")
            exit()
        if response.status_code == 200:
            return 200
    return

#Cria diretório para armazenamento de link da página e tabela com dados
def pagina():
    #A função criará diretório novo para arquivos se ele não existir;
    #caso contrário, utilizará diretório para data atua
    #--------------------------------------------------------------
    #concatena diretórios com a data do dia no qual a pesquisa
    #foi realizada
    folder_name = str(f"{datetime.now():%Y_%m_%d}") + "_query"
    #Concatena o diretório local e o nome da pasta
    path = os.path.join(os.getcwd(), folder_name)
    if os.path.isdir(path) == False:
        os.mkdir(path)

    print(path)
    #Abre a página de busca das resoluções para evitar a cópia de qualquer página
    request = requests.get('https://www.in.gov.br/leiturajornal')
    try:
        #Verifica se o site está aceitando conexões para query
        if request.status_code != 200 and int(request.status_code)/100 == 2:
            print("Resposta do tipo " + str(request.status_code) +
            + "\nIniciando tentativas de conexão com o site...")
            waitForSiteResponse(request.status_code)
        else:
            return "Erro: tipo de resposta inesperada recebida pelo site".format(request)

    except requests.execeptions.RequestExecption as e:
        # Para qualquer outro tipo de resposta que não tenha retorno para get
        # O programa retornará o tipo de erro emitido pelo Site
        return "Erro: {}".format(e)




pagina()
