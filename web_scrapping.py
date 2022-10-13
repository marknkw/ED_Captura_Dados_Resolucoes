# Importa requests para realizar abertura da página com resoluções capturadas
import requests
# Importa os para manipulação de arquivos e tabelas de dados
import os
# Importa date para verificar, e manipular, datetype(timestamp)
from datetime import *
# Importar time para verificar tempo de resposta de uma página
import time
# Adiciona barra de progresso às requisições e webscrappings
from progress.bar import ShadyBar
#Import requests-html para lidar com requests em javascript
from requests_html import HTMLSession

# Função para limpar a tela do terminal


def limparTela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

# Função que verifica se o site está acessível


def siteAcessivel(name) -> str:  # type: ignore
    request = requests.get(str(name))
    try:
        if request.status_code == 200:
            # Limpa tela do terminal
            limparTela()
            print("Resposta do tipo: ", request.status_code)
            print("\nIniciando tentativas de conexão com o site...")
            time.sleep(1)  # type: ignore
            return lerResolucoes()
        elif int(request.status_code) == 200:
            esperarRespostadDoSite(request.status_code, 100, 10)
            print("Resposta do tipo ", request.status_code)
            print("\nIniciando tentativas de conexão com o site...")

        else:
            return "Erro: tipo de resposta inesperada recebida pelo site".format(
                request)

    except requests.exceptions.RequestException as e:
        # Para qualquer outro tipo de resposta que não tenha retorno para get
        # O programa retornará o tipo de erro emitido pelo Site
        return f"Erro: {e}"

# Função de download dos links para acesso às resoluções isoladas


def downloadDoLinkDaPagina() -> None:
    # Limpa a tela do terminal
    limparTela()
    #Atribui à assession uma sessão html assíncrona para carregar todos os dados em javascript
    ssession = HTMLSession()
    s = ssession.get(lerResolucoes())
    s.html.render()  # type: ignore

    #Abre a página e espera as informações serem renderizadas
    #Em sua primeira utilização, o método arender() baixará o webdriver chromium
    #no diretório local para acesso assíncrono ao carregamento dos snippets em javascript
    # Recolhe todos os links carregador pela página
    links = list(s.html.links)  # type: ignore
    bar = ShadyBar('Processando os dados:', max=len(links))
    with open("resolucoes.txt", 'w+') as file:
        # Percorre todos os elementos com tag do tipo "a" atreladas à lista links
        # Atribui barra de progresso a uma variável
        for i in links:
            # Verifica se existe algum elemento com tag do tipo "a" que também
            # é uma referência para um link externo - i.e. endereço para outra página
            # e escreve em um arquivo para ser acessado
            if "/web/dou/-/" in str(i).strip("'"):
                file.write(f"https://www.in.gov.br/{str(i)}" + "\n")
            bar.next()
    bar.finish()

# Função que faz o programa esperar pelo código de requisição 200 para qualquer
# get da página


def esperarRespostadDoSite(response, time, timewait) -> None:
    timer = 0

    while response.status_code != 200:
        time.sleep(timewait)
        timer += timewait
        if timer >= time and response.status_code != 200:
            print("Site não responsivo...\n"
                  "Fechando o programa")
            # Sai do programa
            exit()
        if response.status_code == 200:
            break
    return

# Cria diretório para armazenamento de link da página e tabela com dados


def criarDiretorio() -> str:
    # A função criará diretório novo para arquivos se ele não existir;
    # caso contrário, utilizará diretório para data atua
    # --------------------------------------------------------------
    # concatena diretórios com a data do dia no qual a pesquisa
    # foi realizada
    folder_name = f'{str(f"{datetime.now():%Y_%m_%d}")}_query'
    # Concatena o diretório local e o nome da pasta
    path = os.path.join(os.getcwd(), folder_name)
    if os.path.isdir(path) == False:
        os.mkdir(path)
    return path

# Cria função para leitura de página de pesquisa das resoluções


def lerResolucoes() -> str:
    with open('site.txt', 'r') as file:
        # Grava nome do site de pesquisa das resoluções em variável
        page = file.readline().strip('\n')
    return page

#Função para abrir arquivos e retornar o link de cada uma das
#páginas contendo as resoluções


def listaDePaginas() -> list:  # sourcery skip: avoid-builtin-shadow
    #Abre o arquivo com as resoluções e executa o teste de conexão para cada página
    with open('resolucoes.txt', 'r', encoding='UTF-8') as file:
        #uso do operador walrus ':=' implementado na versão 3.8 do python
        #uso re rstrip() para retirada de newlines e espaços indesejados
        list = []
        while (i := file.readline().rstrip()):
            list.append(i)
    return list
