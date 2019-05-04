import csv
import re
import json
import os

###################################################################################################
# Variáveis globais/funções/listas

# tipos correspondentes de cada questão
tuplo_questao_tipo = [
    ('quem','Pessoal'),
    ('quando','Temporal'),
    ('qnde','Local'),
    ('quantos','Numeral'),
    ('qual','Objeto'),
    ('em que','Objeto'),
    ('quais','Objeto'),
    ('o que','Objeto')
]

questoes = ['quem','quantos','onde','quando','qual','em que','quais','o que']
questoes_exp_reg = '|'.join(questoes)

lista_exp_reg = [
    # para as situações em que não existe um nome da coluna na frase
    (r'^('+questoes_exp_reg+r')(.*)\b\??'), # começa com questao
    (r'(.*)('+questoes_exp_reg+r')\b\??$'), # acaba com questao
    (r'(.+)('+questoes_exp_reg+r')(.+)\b\??'), # tem a questao a meio
]


##################################################################################################
# funções para carregar o ficheiro json e o csv

# faz o open do json e guarda
def save_json(path_files_csv):
    json_file = json.loads(open(path_files_csv).read())
    return json_file

# retorna a lista com as colunas do csv
def get_lista_nomeColunas(json_file):
    dict_keys_nomeColuna = json_file['individuals.csv'].keys()
    lista_nomeColunas = []
    for nome_coluna in dict_keys_nomeColuna:
        lista_nomeColunas.append(nome_coluna)
    return lista_nomeColunas

# retorna  o conteúdo do csv
def openCSV(path):
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        valores_csv = []
        lista_nomeColunas = []
        flag = 0
        for row in spamreader:
            if flag == 0:
                flag = 1
                lista_nomeColunas = row
            else:
                valores_csv.append(row)
    return lista_nomeColunas,valores_csv

#################################################################################################

# retorna o conteudo do json e do csv
def get_schema_nomeColunas_valorescsv(schema,csv):

    # paths só para testing individual
    path_csv = os.path.dirname(os.getcwd()) + '/data/' + csv
    path_schema = os.path.dirname(os.getcwd()) + '/data/' + schema

    # path geral
    # path_csv = os.getcwd() + '/data/' + csv
    # path_schema = os.getcwd() + '/data/' + schema

    # guarda o conteudo do ficheiro json com o schema
    schema = save_json(path_schema)
    (nome_colunas,valores_csv) = openCSV(path_csv)

    return schema,nome_colunas,valores_csv

# percorre a lista de exp reg e retorna a questao e o resto da frase
def procura_mensagem(mensagem):
    for exp_reg in lista_exp_reg:
        match = re.search(exp_reg, mensagem,re.IGNORECASE)
        if match is not None:
                num_matches = len(match.groups())
                if num_matches == 2:
                    if match.group(1).lower() in questoes:
                        questao = match.group(1)
                        resto_frase = match.group(2)
                    else:
                        questao = match.group(2)
                        resto_frase = match.group(1)
                else:
                    questao = match.group(2)
                    resto_frase = match.group(1) + match.group(3)
                return questao,resto_frase

# verifica se o nome da coluna está contida na mensagem
def verifica_existe_nome_coluna(resto_frase,nome_colunas):
    nome_coluna_obj = ""

    nome_colunas_exp_reg = '|'.join(nome_colunas)
    match = re.search(r'('+nome_colunas_exp_reg+r')',resto_frase,re.IGNORECASE)

    if match is not None:
        nome_coluna_obj = match.group(1)

    return nome_coluna_obj

# retorna qual é o tipo de uma questao
def busca_tipo_questao(questao):
    for quest,tipo in tuplo_questao_tipo:
        if questao.lower() == quest:
            return tipo

# descobre qual é a coluna obj quando não está presente na questao
def busca_colunas_tipo_especifico(schema,tipo_questao,nome_colunas):
    lista_colunas_obj = []
    for nome_coluna in nome_colunas:
        tipo_coluna = schema[nome_coluna]['Tipo']
        if tipo_questao == tipo_coluna:
            lista_colunas_obj.append(nome_coluna)
    return lista_colunas_obj

# procura no csv qual é o elemento da pergunta
# para apagar provavelemente
def procura_elemento(resto_frase,valores_csv):
    linha = 0
    for row in valores_csv:
        for elemento in row:
            if elemento is not "":
                if elemento.lower() in resto_frase.lower():
                    return linha
        linha += 1

# retorna as linhas em que tem o elemento contido na memsangem
def procura_elementos(resto_frase,valores_csv):
    lista_linhas = []
    linha = 0
    for row in valores_csv:
        for elemento in row:
            if elemento is not "":
                if elemento.lower() in resto_frase.lower():
                    lista_linhas.append(linha)
        linha += 1
    return lista_linhas

def trata_resultado(lista_respostas):
    respostas = []
    for resposta_linha in lista_respostas:
        r = ','.join(resposta_linha)
        respostas.append(r[:-1])
    resposta = '\n'.join(respostas)
    return resposta

# responde quando tem a coluna objetivo
def respond_full_agr(nome_colunas,nome_coluna_obj,resto_frase,valores_csv):
    lista_respostas = []
    coluna = nome_colunas.index(nome_coluna_obj.capitalize())
    linhas = procura_elementos(resto_frase,valores_csv)
    for linha in linhas:
        print('coluna: '+ str(coluna) + ' linha: ' + str(linha))
        resposta = valores_csv[linha][coluna]
        lista_respostas.append(resposta)
    return lista_respostas

########### for now
# responde para quando não tem a coluna objetivo
def respond_missing_arg(nome_colunas,lista_colunas_obj,resto_frase,valores_csv):
    lista_colunas = []
    lista_respostas = []
    for coluna_obj in lista_colunas_obj:
        coluna = nome_colunas.index(coluna_obj.capitalize())
        lista_colunas.append(coluna)
    lista_linhas = procura_elementos(resto_frase,valores_csv)
    print('lista_colunas: '+ str(lista_colunas) + ' lista_linhas: ' + str(lista_linhas))
    for linha in lista_linhas:
        resposta_linha = []
        for coluna in lista_colunas:
            resposta = valores_csv[linha][coluna]
            resposta_linha.append(resposta)
        lista_respostas.append(resposta_linha)
    return lista_respostas

def responde(mensagem,schema,csv):
    resposta = ""
    # retorna o schema e o conteudo do csv
    (schema,nome_colunas,valores_csv) = get_schema_nomeColunas_valorescsv(schema,csv)

    # divide a questao do resto da frase e retorna os valores
    questao,resto_frase = procura_mensagem(mensagem)
    print("questao: "+ questao)
    print("resto_frase: " + resto_frase)

    # vai verificar se a coluna está especifica na mensagem
    nome_coluna_obj = verifica_existe_nome_coluna(resto_frase,nome_colunas)
    print("nome_coluna_obj: "+nome_coluna_obj)

    # caso a coluna esteja especificada na mensagem
    if nome_coluna_obj is not "":
        lista_respostas = respond_full_agr(nome_colunas,nome_coluna_obj,resto_frase,valores_csv)
        resposta = (',').join(lista_respostas)
    # caso a coluna não esteja espeficiada na mensagem
    else:
        tipo_questao = busca_tipo_questao(questao)
        print("tipo_questao: " + tipo_questao)
        lista_colunas_obj = busca_colunas_tipo_especifico(schema,tipo_questao,nome_colunas)
        print("lista_colunas_obj: " + str(lista_colunas_obj))
        lista_respostas = respond_missing_arg(nome_colunas,lista_colunas_obj,resto_frase,valores_csv)
        resposta = trata_resultado(lista_respostas)

    if resposta == "":
        resposta = 'Não existe.'

    return resposta

# resposta,ratio = responde("Em que dia é a informática em portugal","agenda_SEI_schema.json","agenda_SEI.csv")
# print(resposta)

# resposta = responde("Em que dia é a informática em Portugal?","agenda_SEI_schema.json","agenda_SEI.csv")
# resposta = responde("em que dia é a informática em portugal?","agenda_SEI_schema.json","agenda_SEI.csv")
# resposta = responde("dia é em que a informática em portugal?","agenda_SEI_schema.json","agenda_SEI.csv")
# resposta =  responde("dia é a informática em portugal em que","agenda_SEI_schema.json","agenda_SEI.csv")
# resposta = responde("Quais são os oradores da Informática em Portugal?","agenda_SEI_schema.json","agenda_SEI.csv")
resposta = responde("Quais são as sessões social?","agenda_SEI_schema.json","agenda_SEI.csv")
# resposta = responde("Quais são as atividades do tipo social?","agenda_SEI_schema.json","agenda_SEI.csv")
print('\nResposta:')
print(resposta)