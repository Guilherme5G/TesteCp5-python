import requests
from fontTools.varLib import addFeatureVariations

adega = {
    'vinho' : ['Cabernet Sauvignon', 'Merlot', 'Malbec', 'Chardonnay', 'Sauvignon Blanc', 'Rose Piscine'],
    'Preco' : [75, 60, 85, 70, 65, 95],
    'Vinicola' : ['Concha y Toro', 'Miolo', 'Catena Zapata', 'Salton', 'Casa Valduga', 'Chateau La Gordonne'],
    'Tipo' : ['Tinto', 'Tinto', 'Tinto', 'Branco', 'Branco', 'Rose'],
    'Uva' : ['Cabernet Sauvignon', 'Merlot', 'Malbec', 'Chardonnay', 'Sauvignon Blanc', 'Negrette'],
    'Safra' : [2020, 2021, 2019, 2022, 2022, 2021],
    'Estoque' : [40, 60, 35, 50, 45, 25]
}

def forca_opcao(msg,lista_opcao):
    opcoes = "\n".join(lista_opcao)
    escolha = input(f"{msg}\n{opcoes}\n->")
    while escolha not in lista_opcao:
        print("Invalido!!")
        escolha = input(f"{msg}\n{opcoes}\n->")
    return escolha

def verifica_numero(msg):
    num = input(msg)
    while not num.isnumeric():
        num = input(msg)
    return int(num)

def cria_indices():
    global indices
    indices = {}
    for i in range(len(adega["vinho"])):
        indices[adega['vinho'][i]] = i
    return indices

def remover():
    item = forca_opcao("Qual vinho voce deseja remover?",adega['vinho'])
    indice_item = indices[item]
    for key in adega.keys():
        adega[key].pop(indice_item)
    cria_indices()
    return

def cadastrar():
    for key in adega.keys():
        info = input(f"Diga o novo {key}: ")
        adega[key].append(info)
    cria_indices()
    return

def atualizar():
    item = forca_opcao("Qual vinho sera atualizado?",adega['vinho'])
    indice_item = indices[item]
    info_a_atualizar = forca_opcao(f"Qual informacao sobre {item} sera atualizada?",adega.keys())
    info = input(f"Diga o novo {info_a_atualizar}")
    adega[info_a_atualizar][indice_item] = info

    escolha = forca_opcao("voce deseja atualizar mais alguma coisa?",['s','n'])
    if escolha == 's':
        return atualizar()
    return

def comprar():
    item = forca_opcao("Qual vinho voce quer comprar?",adega['vinho'])
    indice_item = indices[item]
    for key in adega.keys():
        print(f"{key} :{adega[key][indice_item]}")
    continuar = forca_opcao(f"Voce vai levar o {item}?",['s','n'])
    if continuar == 's':
        qtd = verifica_numero(f"Quantos {item} voce quer?")
        if qtd <= adega['Estoque'][indice_item]:
            adega['Estoque'][indice_item] -= qtd
            valor = adega['Preco'][indice_item]*qtd
            carrinho['Valor Total'] += valor
            if item in carrinho['Itens'].keys():
                carrinho['Itens'][item] += qtd
            else:
                carrinho['Itens'][item] = qtd
        else:
            print(f"Invalido! Nao mais que {adega['Estoque'][indice_item]} no estoque!")
    continuar = forca_opcao("Voce quer ver mais vinhos ou encerrar?",['mais','encerrar'])
    if continuar == "mais":
        return comprar()
    return

def cadastrar_endereco():
    while True:
        cep = input("Diga seu cep: ")
        endereco = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if endereco.status_code == 200:
            carrinho['Estoque'] = endereco.json()
            return
        print("Fale um cep Valido!")

carrinho = {
    'Endereco' : {},
    'Itens' : {},
    "Valor Total" : 0
}

indices = cria_indices()
cadastrar_endereco()
comprar()
cadastrar()
remover()
atualizar()
print(carrinho)
print(adega)