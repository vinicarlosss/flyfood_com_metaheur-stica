import random


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
    while contador < 10:
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


