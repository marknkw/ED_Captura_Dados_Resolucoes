#Importa requests para realizar abertura da página com resoluções capturadas
import requests
#Importa os para manipulação de arquivos e tabelas de dados
import os
#Importa date para verificar, e manipular, datetype(timestamp)
from datetime import *
#Importar time para verificar tempo de resposta de uma página
import time
#Importar lxml para lidar com requisição de links dentro de uma página html
#sem realizar o download de toda a página como arquivo a ser manipulado
from lxml import html, etree
#Importar lxml para lidar com requisição de links dentro de uma página html
#sem realizar o download de toda a página como arquivo a ser manipulado
from bs4 import BeautifulSoup
#Importar json para conversão de html para JSON
import json
#importar Todos os dados usando selenium, pois requests não funciona para abrir conteúdo
#carregado com javascript
from selenium import webdriver
#Define path para webdriver chrome
from webdriver_manager.chrome import ChromeDriverManager

#Função que verifica se o site está acessível
def siteAcessivel(name):
    request = requests.get(str(name))
    try:
        if request.status_code == 200:
            downloadDaPagina()
            return lerResolucoes()
        #Verifica se o site está aceitando conexões para query com código do tipo 2
        #mas diferentes de 200
        elif request.status_code != 200 and int(request.status_code)/100 == 2:
            print("Resposta do tipo " + str(request.status_code) +
            + "\nIniciando tentativas de conexão com o site...")
            waitForSiteResponse(request.status_code, 100, 10)

        else:
            return "Erro: tipo de resposta inesperada recebida pelo site".format(request)

    except requests.execeptions.RequestExecption as e:
        # Para qualquer outro tipo de resposta que não tenha retorno para get
        # O programa retornará o tipo de erro emitido pelo Site
        return "Erro: {}".format(e)

#Função de download dos links para acesso às resuluções isoladas
def downloadDaPagina():
    #Define o header de acesso para as requisições do siteAcessivel
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
    }
    #page = requests.get(lerResolucoes(), headers = headers, timeout=(5, 30))
    #s = BeautifulSoup(page.content, 'html.parser')
    #links = etree.HTML(str(s))
    #print(links.xpath('//*[@id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content"]/div[1]'))

    #website = html.fromstring(page.content)
    #tree = website.xpath('//div[@id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content"]//a/@href')
    #print(len(tree))

    motorweb = webdriver.Chrome(ChromeDriverManager().install())
    motorweb.get(lerResolucoes())

    s = BeautifulSoup(motorweb.page_source, 'lxml')
    links = s.xpath('//a/@href')
    for i in links:
        print(i)

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
            #Sai do programa
            exit()
        if response.status_code == 200:
            break
    return

#Cria diretório para armazenamento de link da página e tabela com dados
def criarDiretorio():
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

#Cria função para leitura de página de pesquisa das resoluções
def lerResolucoes():
    file = open("site.txt", 'r')
    #Grava nome do site de pesquisa das resoluções em variável
    page = file.readline().strip('\n')
    file.close()
    return page

#Cria diretório para pesquisa com a data do query a ser realizado
criarDiretorio()

#Abre a página de busca das resoluções para verificar acessibilidade da página
page = siteAcessivel(lerResolucoes())
