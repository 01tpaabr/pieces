import copy
import sys
import numpy as np
import matplotlib.pyplot as plt

#Algoritmo para mostrar configuração de uma matriz 2^n x 2^n -1, preenchida por peças do tipo:
#[ 1 , -1 ]
#[ 1 ,  1 ]

print('Tamanho: ', end="")
tamanho = int(input())

#Codificação das peças para adicionar cor:
numeroPeca = 1

#Peça basica
tiposPecas = [0 for i in range(tamanho)]
tiposPecas[0] = [[0,-1],[0,0]]



def printTabuleiro(tabuleiro):
    for i in tabuleiro:
        for j in i:
            print(" " + str(j) + " ", end = '')
        print('\n')
    
def criaTabuleiro(n):
    tamanho = 2 ** n
    tabuleiro = [[0] * tamanho for i in range(tamanho)]
    tabuleiro[0][tamanho - 1] = -1
    return tabuleiro

def rotacionaBasico(peca):
    temp = copy.deepcopy(peca)
    for i in range(len(peca[0])):
        for j in range(len(peca[i])):
            curr = peca[i][j]
            temp[j][(len(peca[0]) - 1) - i] = curr       

    return temp

def rotaciona(peca, tipo):
    #Uma peça será como um tabuleiro, uma matriz n x n que pode ser formada por varias sub-peças
    if tipo == 1: #Rotação 1 vez para a direita
        peca = rotacionaBasico(peca)
    elif tipo == 2: #Rotação 2 vezes para a direita
        peca = rotacionaBasico(rotacionaBasico(peca))
    elif tipo == 3: #Rotação 3 vezes para a direita
        peca = rotacionaBasico(rotacionaBasico(rotacionaBasico(peca)))

    return peca

#Pega algum dos tipos de peça, e codifica uma nova peça com seu numero próprio
def colorePeca(tipoPeca):
    novaPeca = copy.deepcopy(tipoPeca)
    for i in range(len(novaPeca[0])):
        global numeroPeca
        tempNumero = numeroPeca

        for j in range(len(novaPeca[0])):
            if novaPeca[i][j] != -1:
                novaPeca[i][j] += tempNumero % 5

    numeroPeca += 1

    return novaPeca

def colocaPeca(tabuleiro, peca, pos):
    #Dada a posição onde o canto superior esquerdo da peça deve ficar, posiciona a peca
    #Se uma parte da peça estiver preenchida por -1, não deve mudar o valor que já está no tabuleiro
    for i in range(pos[0], (pos[0] + len(peca[0]))):
        for j in range(pos[1], (pos[1] + len(peca[0]))):
            currPeca = peca[i - pos[0]][j - pos[1]]
            if currPeca != -1:
                if tabuleiro[i][j] != 0:
                    print("Tentou-se colocar uma peça em algum lugar invalido:")
                    print("x: " + str(i))
                    print("y: " + str(j))
                    print("Valor: " + str(tabuleiro[i][j]))
                    print("Pos inicial x: " + str(pos[0]))
                    print("Pos inicial y: " + str(pos[1]))
                    printTabuleiro(tabuleiro)
                    
                    sys.exit()
        
                tabuleiro[i][j] = currPeca
                
    
    return tabuleiro

#Criar peça para n = 2:
def criarPeca2():
    tempTabuleiro = criaTabuleiro(2)
    
    #Cria sub-pecas
    tempList = []
    for i in range(5):
        tempList.append(colorePeca(tiposPecas[0]))
        

    tempTabuleiro = colocaPeca(tempTabuleiro, tempList[0], [0,2])
    tempTabuleiro = colocaPeca(tempTabuleiro, tempList[1], [1,1])
    tempTabuleiro = colocaPeca(tempTabuleiro, tempList[2], [2,0])
    tempTabuleiro = colocaPeca(tempTabuleiro, rotaciona(tempList[3], 1), [0,0])
    tempTabuleiro = colocaPeca(tempTabuleiro, rotaciona(tempList[4], 3), [2,2])

    return tempTabuleiro

def preenche(tabuleiro, n):
    #Temos que para n = 1 e n = 2, a solução é unica
    #Mas para n > 2, a solução é feita pela junção de peças conseguidas pela solução de n-1, rotacionadas
    #mais uma peça no centro do tabuleiro
    #Cada peça será representada por um número >= 0 
    tamanhoReal = 2 ** n
    global tiposPecas

    if n == 1:
        novaPeca = colorePeca(tiposPecas[0])
        return colocaPeca(tabuleiro, novaPeca, [0,0])
    elif n == 2:
        peca2 = criarPeca2()
        tiposPecas[1] = copy.deepcopy(peca2)
        return peca2
    #Quer dizer que já foi calculado
    elif tiposPecas[n - 1] != 0:
        return tiposPecas[n - 1]


    novaPeca = colocaPeca(tabuleiro, colorePeca(preenche(criaTabuleiro(n-1), n-1)), [0, (tamanhoReal//2)])
    novaPeca = colocaPeca(tabuleiro, colorePeca(preenche(criaTabuleiro(n-1), n-1)), [(tamanhoReal//2), 0])
    novaPeca = colocaPeca(tabuleiro, rotaciona(colorePeca(preenche(criaTabuleiro(n-1), n-1)), 1), [0, 0])
    novaPeca = colocaPeca(tabuleiro, rotaciona(colorePeca(preenche(criaTabuleiro(n-1), n-1)), 3), [tamanhoReal//2, tamanhoReal//2])
    
    tiposPecas[n - 1] = novaPeca

    #Remover peças que já não são necessárias
    tiposPecas[n - 2] = 0


    return novaPeca
    


tabuleiro = criaTabuleiro(tamanho)
tabuleiro = preenche(tabuleiro, tamanho)

show = np.matrix(tabuleiro)
plt.imshow(show)
plt.colorbar()
plt.show()
