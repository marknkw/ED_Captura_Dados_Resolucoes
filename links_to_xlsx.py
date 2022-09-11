#Importa funções de web_scrapping
import web_scrapping
#Importa funções que criação xlsx
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

#Função para abrir arquivos e baixar o conteúdo de cada uma das
#páginas contendo as resoluções
def testeDasPaginas():
    #Abre o arquivo com as resoluções e executa o teste de conexão para cada página
    with open('resolucoes.txt', 'r', encoding='UTF-8') as file:
        #uso do operador walrus ':=' implementado na versão 3.8 do python
        #uso re rstrip() para retirada de newlines e espaços indesejados
        while (i := file.readline().rstrip()):
            print(i)


testeDasPaginas()
