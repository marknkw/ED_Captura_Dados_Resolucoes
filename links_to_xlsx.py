#Importa funções de web_scrapping
import web_scrapping
#Importa biblioteca que lida com funções de criação do xlsx
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string
#Importa requests_html para download do conteúdo da página
from requests_html import HTMLSession

#Função que salva texto da resolução em arquivo
def salvarResolu(text, path, number):
    file = open(path + '/resolucao_' + str(number) + '.txt', 'w+', encoding='utf-8')
    file.write(text)
    file.close()

#Recebe lista de páginas a serem baixadas e manipuladas
list = web_scrapping.listaDePaginas()
#Cria Diretório para armazenar arquivos das páginas
caminho = web_scrapping.criarDiretorio()
#Atribui cada resolução à uma variável
for i in range(0, len(list), 1):
    session = HTMLSession()
    link = session.get(list[i])
    #Resolve conteúdo acessível por javascript
    link.html.render()
    #Atribui todo condeúdo de elemento com dados da resolução à variável resolucoes
    resolucoes = link.html.find("#materia > div > div.texto-dou", first = True).text
    #Atribui diretório do query a uma variável
    path = web_scrapping.criarDiretorio()
    salvarResolu(resolucoes, path, i)
    #Abre novo workbook para adicionar os dados da resolução
    wb = openpyxl.Workbook()
    wb.save(path + '/' + '.xlsx')
