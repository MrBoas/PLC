#!/usr/bin/python3
import sys
import re
import random

from .bot_tradutor import bot_tradutor # atm tradutor
from .bot_lista import bot_lista # atm proverbios

despedidas = [
    "Adeus parceiro",
    "Até à próxima colega",
]
lista = [
    ( r'batatas(.*)', "love"),
    ( r'(?:.* )?(.+) em (\w+)\b\??', lambda x: bot_tradutor.traduz(x.group(1),x.group(2).capitalize())), # regra a mão
    # bot2.geraRegras()[0], # regra automatica (beta)
    ( r'(.+)', lambda x: bot_lista.gera_resposta(x.group(1))),
    ( r'(.+)', "FDS"),
]
# print(lista)




##### Auxiliares #####
# append de uma mensagem ao ficheiro de log
def append2file(msg,ident):
    file = 'log.txt'
    file = open(file,'a')
    if ident == 'user':
        file.write('User: '+msg+'\n')
    elif ident == 'bot':
        file.write('Bots: '+msg+'\n')
    else:
        file.write('\n---FIM DE CONVERSA---\n\n')
    file.close()


##### Funcoes #####
# percorre as regras até encontrar uma que dê match e devolve o output
def parse(content):
    for regex,out in lista:
        # print(regex,out)
        match = re.match(regex,content)
        if match==None:
            print("    NONE of this")
        else:
            # print(match)
            if callable(out):
                output = out(match)
                if output != None:
                    return output
            else:
                return out+'=>'+match.group(0)
    return "Negative Sir!" # TODO devolver uma frase de falha ou entretenimento

# onde tudo começa
def main():
    if (len(sys.argv)>1): # caso seja inserido um argumento (input file)
        file = sys.argv[1]
        content = open(file,'r').read()
        result = parse(content)
        print(result)
    else: # caso não haja input file, lê do stdin
        while True:
            inputUser = input()
            append2file(inputUser,'user')
            if inputUser == "quit": # diretor termina com "quit"
                break
            result = parse(inputUser)
            append2file(result,'bot')
            print(result)
        despedida = random.choice(despedidas)
        append2file(despedida,'bot')
        print(despedida)
        append2file('','') # log de fim de conversa


##### Run #####
# print(open('../bots_info.md','r').read())
main()
# print(getMeme())
# print(bot_gera.gera_resposta('galinha'))