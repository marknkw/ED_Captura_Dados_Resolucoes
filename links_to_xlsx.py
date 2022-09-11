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
    file = open(path + '/resolucao_' + str(number) + '.txt', 'r', encoding='utf-8')
    resolu = file.readline()
    file.close()
    return resolu

#Função que salva estado atual de xlsx
def salvarExcel(path):
    wb.save(path)


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
    #Salva resolução completa em arquivo de texto e retorna nome da resolução
    resolu = salvarResolu(resolucoes, path, i)
    #Abre novo workbook para adicionar os dados da resolução
    wb = openpyxl.Workbook()
    #Define nome do excel para dada resolução
    wbname = (path + '/' + str(resolu).strip('\n') + '.xlsx')
    #Cria arquivo excel para dada resolução
    salvarExcel(wbname)
    wb.close()
    #Cria uma versão ativa do worksheet a ser trabalhado
    wb = openpyxl.load_workbook(path + '/' + str(resolu).strip('\n') + '.xlsx')
    wb_active = wb.active
    #Define os dados a serem inseridos na primeira coluna de cada excel:
    dados = {1: "RESOLUÇÃO", 2: "EMPRESA", 3: "AUTORIZAÇÃO", 4: "MARCA", 5: "PROCESSO",
            6: "REGISTRO", 7: "VENDA E EMPREGO", 8: "VENCIMENTO", 9: "APRESENTAÇÃO",
            10: "VALIDADE", 11: "CATEGORIA", 12: "ASSUNTO\nPETIÇÃO", 13: "EXPEDIENTE E PETIÇÃO",
            14: "VERSÃO" }
    wb_active.insert_rows(13)
    for column, value in dados.items():
        wb_active.cell(row = 1, column= column, value = value)
    salvarExcel(wbname)
