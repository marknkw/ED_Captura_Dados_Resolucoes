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
from bs4 import BeautifulSoup
#Importar json para conversão de html para JSON
import json
#importar Todos os dados usando selenium, pois requests não funciona para abrir conteúdo
#carregado com javascript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#Define path para webdriver chrome
from webdriver_manager.chrome import ChromeDriverManager
#Ignorar avisos de funções antigas, mas funcionais
import warnings

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
    #headers = {
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
    #}
    #page = requests.get(lerResolucoes(), headers = headers, timeout=(5, 30))
    #s = BeautifulSoup(page.content, 'html.parser')
    #links = etree.HTML(str(s))
    #print(links.xpath('//*[@id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content"]/div[1]'))

    #website = html.fromstring(page.content)
    #tree = website.xpath('//div[@id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_hierarchy_content"]//a/@href')
    #print(len(tree))

    #Abre driver automatizado Selenium com Chrome como WebDriver
    #Força a inicialização de um path momentâneo para o WebDriver
    motorweb = webdriver.Chrome(ChromeDriverManager().install())
    motorweb.get(lerResolucoes())
    #Espera o site carregar
    time.sleep(7)
    #Define o tipo de dado recolhido como html e a fonte dos dados os dados
    #alocados na memória do objeto motorweb
    s = BeautifulSoup(motorweb.page_source, 'html.parser')
    #Encontra todos os elementos com a tag do tipo "a", ou seja, como um elemento
    #do código HTML
    links = motorweb.find_elements(By.TAG_NAME, "a")
    #Cria arquivo para abrir os links das resolucoes ativas
    file = open("resolucoes.txt", 'w+')
    #Percorre todos os elementos com tag do tipo "a" atreladas à lista links
    for i in links:
        #Verifica se existe algum elemento com tag do tipo "a" que também
        #é uma referência para um link externo - i.e. endereço para outra página
        #e escreve em um arquivo para ser acessado
        if "https://www.in.gov.br/web/dou/-/" in str(i.get_attribute("href")):
            file.write(str(i.get_attribute("href")))
            file.write("\n")
    #Fecha o arquivo com os links para as resoluções
    file.close()


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

#Ignora avisos dos modulos
warnings.simplefilter("ignore")

#Cria diretório para pesquisa com a data do query a ser realizado
criarDiretorio()

#Abre a página de busca das resoluções para verificar acessibilidade da página
page = siteAcessivel(lerResolucoes())
