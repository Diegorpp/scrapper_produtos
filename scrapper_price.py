.#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import re

def obtem_lista_descricao (bs_obj):
    #Obtem as tags que estão cada um dos produtos divididos por DIVs

    #Casa durante a iteraçao ele chegue em uma pagina que já não tem mais produtos ele gera esse erro.
    try:
        lista_produtos = bs_obj.body.find_all('div', class_ = 'product-grid')[0].div
    except:
        return [[]]
    par = [].copy()
    conjunto = []
    
    for tag in lista_produtos.next_siblings:
        #Verificar se as listas estão vazias por alguma inconsistência na pagina
        if ( len(tag.find_all('div', class_ = re.compile('PriceWrapper-[a-zA-Z0-9]+') )) ) == 0:
            continue
        if ( len(tag.find_all('div', class_ = re.compile('TitleWrapper-[a-zA-Z0-9]+') )) ) == 0:
            continue
        
        #Obtem a tag especifica em que está a informação desejada(descrição e preço)
        #Regex utilizado é para obter a classe independente do código que vai estar inserido na classe.
        general_desc = tag.find_all('div', class_ = re.compile('TitleWrapper-[a-zA-Z0-9]+') )[0].text
        general_price = tag.find_all('div', class_ = re.compile('PriceWrapper-[a-zA-Z0-9]+') )[0]
        general_price = general_price.find_all('span', class_ = re.compile('PriceUI-[a-zA-Z0-9]+') )[0]
        
        #Prepara os dados de forma estruturada pra irem para uma planilha
        par.append(general_desc)
        par.append(general_price.text.replace("R$ ",""))
        conjunto.append(par)
        par = []
    return conjunto

def organiza_dados():
    pass

#Le a planilha com os dados e retorna um DataFrame
def obtem_modelos(dados_csv):
    csv_modelos = pd.read_csv(dados_csv)
    return modelos

#Utilizando modulo csv, mas com pandas é mais facil
def salva_info_scv(dados):
    with open('dados_modelos.ods', mode='w', newline='') as csv_file:
        fieldnames = ["Modelo", "Descricao", "Valor"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for dado in dados:
            writer.writerow(dado)

        print("Dados gravados com sucesso\n")
        return

#Em processo de modularização
def obtem_preco ():
    lista_produtos = bs_obj.body.find_all('div', class_ = 'product-grid')[0].div
    general_price = lista_produtos.find_all('div', class_ = re.compile('PriceWrapper-[a-zA-Z0-9]+') )[0]
    general_price2 = general_price.find_all('span', class_ = re.compile('PriceUI-[a-zA-Z0-9]+') )[0]
    print(general_price2.text)

#Em processo de modularização
def obtem_descricao ():
    lista_produtos = bs_obj.body.find_all('div', class_ = 'product-grid')[0].div
    general_price = lista_produtos.find_all('div', class_ = re.compile('TitleWrapper-[a-zA-Z0-9]+') )[0].text
    print(general_price)


#url_page = "https://www.americanas.com.br/busca/galaxy-j1-mini?limite=24&offset=48"
#Feito exclusivamente para percorrer as paginas das lojas americanas
def percorre_pagina_americanas(produto,paginas=5):
    dados_produtos = pd.DataFrame()
    for i in range(paginas):
        url = "https://www.americanas.com.br/busca/"+str(produto)+"galaxy-j1-mini?limite=24&offset="+str(i*24)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html = requests.get(url, headers=headers)
        bs_obj_new = BeautifulSoup ( html.text, "lxml" )

        if (html.status_code == 200):
            dados_indeferidos = obtem_lista_descricao(bs_obj_new)
            if (dados_indeferidos == [[]]):
                continue
            if (not(dados_indeferidos == [])):
                print(dados_indeferidos)
                dados_produtos = dados_produtos.append(dados_indeferidos)
                print(dados_produtos)
                print(url)
        else:
            print("Erro na url"+url)

    return dados_produtos

#Variaveis de gerencia do script
ARQUIVO = "modelos_celulares.csv'"

#em construção
df_celulares = obtem_modelos(ARQUIVO)
df_celulares = df_celulares.drop( columns='Device_Price')


#Coleta os dados dos produtos e atualiza a descrição na tabela.
todos_dados =  percorre_pagina_americanas()
todos_dados = todos_dados.rename(columns={0:"Description",1:"Price"})


todos_dados.to_csv('dados_produtos.csv')
