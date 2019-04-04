from bot_lista import bot_lista
from bot_tradutor import bot_tradutor
from bot_wiki import bot_wiki
from bot_csv import bot_csv
from bot_QA import bot_QA
from util import *

regras_bot_lista = [
    (['NORMAL'],1,r'(.+)', lambda x,dataset: bot_lista.gera_resposta_dsl(x.group(1),dataset[0]))
]

regras_bot_wiki = [
    (['NORMAL'],5,r'[Oo] que sabes sobre (.*)\b\??',lambda x,dataset : bot_wiki.gera_resposta_dsl(x.group(1),dataset[0])),
    (['NORMAL'],5,r'[Ff]ala me sobre (.*)\b\??',lambda x,dataset : bot_wiki.gera_resposta_dsl(x.group(1),dataset[0])),
]

regras_bot_tradutor = [
    (['NORMAL'],4,r'[Cc]omo se diz ([\w ]+) em (\w+)\b\??', lambda x: bot_tradutor.traduz(x.group(1),x.group(2))),
    (['NORMAL'],5, r'[Qq]ual é a tradução de ([\w ]+) em (\w+)\b\??', lambda x: bot_tradutor.traduz(x.group(1),x.group(2))),
    (['NORMAL'],4, r'([\w ]+) como se diz em (\w+)\b\??', lambda x: bot_tradutor.traduz(x.group(1),x.group(2))),
    (['NORMAL'],4, r'[Ee]m (\w+) como se diz (\w+)\b\??', lambda x: bot_tradutor.traduz(x.group(2),x.group(1))),
    (['NORMAL'],4, r'([\w ]+) em (\w+) diz-se ([\w ]+)\b\??', lambda x: bot_tradutor.guardar_dicionario(x.group(1),x.group(2),x.group(3))),
    (['NORMAL'],4, r'([\w ]+) diz-se ([\w ]+) em (\w+)\b\??', lambda x: bot_tradutor.guardar_dicionario(x.group(1),x.group(3),x.group(2)))
]

regras_bot_csv = [
    (['NORMAL'],3,r'('+tipos_perguntas_exp+r').*', lambda x,dataset: bot_csv.responde_dsl(x.group(0),dataset[0],dataset[1])),
]

regras_bot_QA = [
    (['NORMAL'],2,r'('+tipos_perguntas_exp+r').*', lambda x,dataset: bot_QA.responde(x.group(0),dataset[0])),
]

regras_estado = [
    ('CHATEADO',r'És mesmo ('+insultos_exp_reg+r')', lambda : 'CHATEADO'),
    ('CHATEADO',r'És ('+insultos_exp_reg+r')', lambda : 'CHATEADO'),
    ('CHATEADO',r'Tu és ('+insultos_exp_reg+r')', lambda : 'CHATEADO'),
    ('CHATEADO',r'Desculpa', lambda : 'NORMAL')
]

def get_regras(bot):
    regras = []
    if bot == 'bot_lista':
        regras = regras_bot_lista
    elif bot == 'bot_tradutor':
        regras = regras_bot_tradutor
    elif bot == 'bot_wiki':
        regras = regras_bot_wiki
    elif bot == 'bot_csv':
        regras = regras_bot_csv
    elif bot == 'bot_QA':
        regras = regras_bot_QA
    return regras