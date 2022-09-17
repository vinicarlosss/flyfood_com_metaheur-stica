import random
from functools import  reduce


def modulo(termOne, termTwo):  # Função para determinar o módulo das distâncias
    resultado = termOne - termTwo
    if resultado < 0:
        resultado *= -1
        return resultado
    return resultado


def distancia(termOne, termTwo):  # Função para determinar a distância entre dois pontos de entrega
    return termOne + termTwo


def funcaoCusto(individuos,coordenadas, modulo, distancia):  # cálculo do custo da solução
    custoindividuos = [0 for _ in range(len(individuos))]
    contador = 0
    maiorcusto = 0
    while contador < len(individuos):
        custo = 0
        # O laço for faz uma iteração definindo i como cada ponto de entrega do possível melhor circuito.
        for i in individuos[contador]:
            # se é o primeiro ponto de entrega começamos contabilizando a distância do restaurante
            if individuos[contador].index(i) == 0:
                xOne = coordenadas[f'R'][0]
                yOne = coordenadas['R'][1]
                xTwo = coordenadas[f'{i}'][0]
                yTwo = coordenadas[f'{i}'][1]
                custo += distancia(modulo(xOne,xTwo), modulo(yOne, yTwo))
                entregaAtual = i
            # Até o penúltimo ponto de entrega contabilizamos a distância indo do ponto de entrega atual(que no caso é o
            # da interação anterior) até o ponto de entrega que está na vez.
            elif individuos[contador].index(i) < len(individuos[contador]) - 1:
                xOne = coordenadas[f'{entregaAtual}'][0]
                yOne = coordenadas[f'{entregaAtual}'][1]
                xTwo = coordenadas[f'{i}'][0]
                yTwo = coordenadas[f'{i}'][1]
                custo += distancia(modulo(xOne, xTwo), modulo(yOne, yTwo))
                entregaAtual = i
            # Quando chegamos no penultimo ponto, contabilizamos a distância do penúltimo  ponto de entrega até
            # o ultimo e depois do último ponto até o restaurante.
            else:
                xOne = coordenadas[f'{entregaAtual}'][0]
                yOne = coordenadas[f'{entregaAtual}'][1]
                xTwo = coordenadas[f'{i}'][0]
                yTwo = coordenadas[f'{i}'][1]
                custo += distancia(modulo(xOne, xTwo), modulo(yOne, yTwo))
                xOne = coordenadas[f'{i}'][0]
                yOne = coordenadas[f'{i}'][1]
                xTwo = coordenadas['R'][0]
                yTwo = coordenadas['R'][1]
                custo += distancia(modulo(xOne, xTwo), modulo(yOne, yTwo))
                if contador == 0:
                    maiorcusto = custo
                else:
                    maiorcusto = custo if custo > maiorcusto else maiorcusto
        custoindividuos[contador] = custo
        contador += 1
    custoindividuos.append(maiorcusto)
    return custoindividuos


def funcaoAptidao(custos, individuos):  # função para calcular a aptidão dos indivíduos
    aptidoes = [0 for _ in range(len(individuos))]
    for i in range(len(individuos)):
        aptidoes[i] = (custos[i]*-1) + custos[len(individuos)]
    return aptidoes

def soma(a,b):
    return a+b

def trataNumero(numero):
    subtraendo = numero.__floor__()
    if numero - subtraendo >= 0.75:
        return numero.__ceil__()
    return numero.__floor__()


def roleta(aptidao, individuos):  # função para seleção dos indivíduos que vão se reproduzir
    opcoesroleta = [0 for _ in range(100)]
    total = reduce(soma, aptidao)
    percentuais = [0 for _ in range(len(individuos))]
    for i in range(len(aptidao)):
        valorPercentual = ((aptidao[i]/total)*100)
        percentuais[i] = trataNumero(valorPercentual)

    index = 0
    contador = 0
    while True:

        if index == len(individuos):
            break
        elif percentuais[index] != 0:
            for i in range(percentuais[index]):
                opcoesroleta[contador] = individuos[index]
                contador += 1

        index += 1

    individuosselecionados = [0 for _ in range(len(individuos))]
    contador = 0
    while True:
        numeroaleatorio = random.randint(0,99)
        if contador == len(individuosselecionados):
            break
        elif opcoesroleta[numeroaleatorio] != 0:
            individuosselecionados[contador] = opcoesroleta[numeroaleatorio]
            contador += 1

    return individuosselecionados


def cruzamento(individuos):
    individuosfilhos = []
    contador = 0
    listaparceiros = [0 for _ in range(int(len(individuos)/2))]
    while True:
        if contador == len(listaparceiros):
            break
        else:
            numeroaleatorio = random.randint(0,len(individuos)-1)
            listaparceiros[contador] = individuos[numeroaleatorio]
            individuos.remove(individuos[numeroaleatorio])
            contador += 1
    contador = 0
    while True:
        pontocorte = [random.randint(0, (len(individuos[0])-1)),random.randint(0, (len(individuos[0])-1))]

        if pontocorte[0] != pontocorte[1]:
            pontocorte.sort()
            break
    while contador <= len(individuos) - 1:
        paium = individuos[contador].copy()
        paidois = listaparceiros[contador].copy()
        filhoum = [0 for _ in range(len(paium))]
        filhodois = [0 for _ in range(len(paidois))]
        mapeamentos = []
        contadordois = pontocorte[0]
        while True:
            if contadordois > pontocorte[1]:
                break
            filhoum[contadordois] = paidois[contadordois]
            filhodois[contadordois] = paium[contadordois]
            mapeamentos.append([paium[contadordois], paidois[contadordois]])
            contadordois += 1
        contadordois = 0
        while contadordois < len(filhoum): # filho 1
            if filhoum[contadordois] == 0:
                if paium[contadordois] not in filhoum: # se o gene do pai não estiver no filho, adicione
                    filhoum[contadordois] = paium[contadordois]
                else:  # se não estiver procure nos mapeamentos
                    for i in mapeamentos:
                        if i[0] == paium[contadordois]:
                            referencia = i[1]
                            if referencia not in filhoum:
                                filhoum[contadordois] = referencia
                            else:
                                index = 0
                                mapeamentos2 = mapeamentos.copy()
                                mapeamentos2.remove(i)
                                while True:
                                    if mapeamentos2[index][0] == referencia and mapeamentos2[index][1] not in filhoum:
                                        filhoum[contadordois] = mapeamentos2[index][1]
                                        break
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][0] not in filhoum:
                                        filhoum[contadordois] = mapeamentos2[index][0]
                                        break
                                    elif mapeamentos2[index][0] == referencia and mapeamentos2[index][0] in filhoum:
                                        referencia = mapeamentos2[index][1]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][1] in filhoum:
                                        referencia = mapeamentos2[index][0]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                index += 1
                            break
                        elif i[1] == paium[contadordois]:
                            referencia = i[0]
                            if referencia not in filhoum:
                                filhoum[contadordois] = referencia
                            else:
                                index = 0
                                mapeamentos2 = mapeamentos.copy()
                                mapeamentos2.remove(i)
                                while True:
                                    if mapeamentos2[index][0] == referencia and mapeamentos2[index][1] not in filhoum:
                                        filhoum[contadordois] = mapeamentos2[index][1]
                                        break
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][0] not in filhoum:
                                        filhoum[contadordois] = mapeamentos2[index][0]
                                        break
                                    elif mapeamentos2[index][0] == referencia and mapeamentos2[index][0] in filhoum:
                                        referencia = mapeamentos2[index][1]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][1] in filhoum:
                                        referencia = mapeamentos2[index][0]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1

                                    index += 1
                            break

            contadordois += 1
        contadordois = 0
        while contadordois < len(filhodois): # filho 2
            if filhodois[contadordois] == 0: # se o filho não tiver gene nessa posição
                if paidois[contadordois] not in filhodois: # se o gene do pai dois não estiver no filho dois, adicione
                    filhodois[contadordois] = paidois[contadordois]
                else: # se o gene já estiver no filho dois, procure nos mapeamentos com qual gene esse gene foi mapeado no ponto de corte
                    for i in mapeamentos:
                        if i[0] == paidois[contadordois]: # se o primeiro item dos mapeamentos é igual o gene que está sendo procurado a referência é o outro item
                            referencia = i[1]
                            if referencia not in filhodois: # se a referencia não estiver no filho dois, adicione ele
                                filhodois[contadordois] = referencia
                            else: # se estiver no filho dois vamos procurar nos mapeamentos novamente o gene mapeado com a referência
                                index = 0
                                mapeamentos2 = mapeamentos.copy()
                                mapeamentos2.remove(i)
                                while True:
                                    if mapeamentos2[index][0] == referencia and mapeamentos2[index][1] not in filhodois:
                                        filhodois[contadordois] = mapeamentos2[index][1]
                                        break
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][0] not in filhodois:
                                        filhodois[contadordois] = mapeamentos2[index][0]
                                        break
                                    elif mapeamentos2[index][0] == referencia and mapeamentos2[index][0] in filhodois:
                                        referencia = mapeamentos2[index][1]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][1] in filhodois:
                                        referencia = mapeamentos2[index][0]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    index += 1
                            break
                        elif i[1] == paidois[contadordois]:
                            referencia = i[0]
                            if referencia not in filhodois:
                                filhodois[contadordois] = referencia
                            else:
                                index = 0
                                mapeamentos2 = mapeamentos.copy()
                                mapeamentos2.remove(i)
                                while True:
                                    if mapeamentos2[index][0] == referencia and mapeamentos2[index][1] not in filhodois:
                                        filhodois[contadordois] = mapeamentos2[index][1]
                                        break
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][0] not in filhodois:
                                        filhodois[contadordois] = mapeamentos2[index][0]
                                        break
                                    elif mapeamentos2[index][0] == referencia and mapeamentos2[index][0] in filhodois:
                                        referencia = mapeamentos2[index][1]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    elif mapeamentos2[index][1] == referencia and mapeamentos2[index][1] in filhodois:
                                        referencia = mapeamentos2[index][0]
                                        mapeamentos2.remove(mapeamentos2[index])
                                        index = -1
                                    index += 1
                            break
            contadordois += 1
        individuosfilhos.append(filhoum)
        individuosfilhos.append(filhodois)
        contador += 1

    return individuosfilhos


def mutacao(individuos):
    for i in individuos:
        taxamutacao = random.randint(1,10)
        if taxamutacao > 7:
            primeirogene = random.randint(0, len(i)-1)
            segundogene = random.randint(0, len(i) - 1)
            geneescolhido = i[primeirogene]
            i[primeirogene] = i[segundogene]
            i[segundogene] = geneescolhido
    return individuos


def criarPopulacaoInicial(individuos):  # função de criação da população inicial
    populacao = [[0 for _ in range(len(individuos))] for _ in range(10)]
    contador = 0
    while contador < 10:
        copiaIndividuos = individuos.copy()
        for i in range(len(individuos)):
            index = random.randint(0, len(copiaIndividuos) - 1)
            populacao[contador][i] = copiaIndividuos[index]
            copiaIndividuos.remove(copiaIndividuos[index])

        contador += 1
    return populacao


arquivo = open('matriz.txt', 'r')
pontos_entrega = []  # array para armazenar os pontos de entrega
circuitos = []  # array para armazenar todos os possíveis circuitos a serem realizados
coordenadas = {}  # dicionário para armazenar as coordenadas dos pontos de entrega
contador = 0
for linha in arquivo:
    linha = linha.replace(" ", "")
    if contador == 0:  # definindo o número de linhas e colunas da matriz
        n = int(linha[0])
        m = int(linha[1])
    elif contador <= n:
        for i in linha:  # verificando linha por linha do arquivo onde estão localizados os pontos de entrega
            if i == 'R':
                coordenadas['R'] = (linha.index(i) + 1, contador)
            elif i != '0' and i != '\n':
                pontos_entrega.append(i)
                coordenadas[f'{i}'] = (linha.index(i) + 1, contador)
    contador += 1

arquivo.close()
populacaoInicial = criarPopulacaoInicial(pontos_entrega)
custos = funcaoCusto(populacaoInicial, coordenadas, modulo, distancia)
aptidao = funcaoAptidao(custos, populacaoInicial)
individuosparareproduzir = roleta(aptidao, populacaoInicial)
print(reduce(soma, custos))
contador = 0
individuoscruzados = cruzamento(individuosparareproduzir)
individuosmutados = mutacao(individuoscruzados)
while contador < 20:
    populacao = individuosmutados
    custos = funcaoCusto(populacao, coordenadas, modulo, distancia)
    aptidao = funcaoAptidao(custos, populacao)
    individuosparareproduzir = roleta(aptidao, populacao)
    individuoscruzados = cruzamento(individuosparareproduzir)
    individuosmutados = mutacao(individuoscruzados)
    print(reduce(soma, custos))
    contador += 1






