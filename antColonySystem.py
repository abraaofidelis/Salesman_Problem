# -*- coding: utf-8 -*-
"""

@author: Abraão de Castro Fidelis 02/06/2019

"""
#===============================================================
# Bibliotecas importadas
import random
import tkinter
from math import sqrt
#===============================================================
# Parametros 
alpha = 1
beta = 1
sigma = 0.15
q = 10
eta = 0.1   

n_pontos = 5
n_formigas = 5      #número de formigas
iteracoes = 200


#n_iteracoes = 20    #número de iterações

#Inicialização
                    #feromônio inicial
#matrizFeromonios = [[eta]*5]*5           #matrix para atualização de feromonios depositados
#matrizDistancias =[[0, 50, 30, 22, 23],
#                   [50, 0, 22, 48, 29],
#                   [30, 22, 0, 34, 32],
#                   [22, 48, 34, 0, 35],
#                   [23, 29, 32, 35, 0]]

matrizFeromonios = [[eta]*n_pontos]*n_pontos

#pocos = ["A", "B", "C", "D", "E"]  #poços que serão percorridos
#matrizProbabilidades = matrizProbabilidades = [[0]*(len(pontos))]*(len(pontos))       #matrix de probabilidades de caminhos
#===============================================================

#Função para usar o Método da Roleta
def rodaRoleta(probabilidades):  
    roleta = []
    n=0
    #responsável por montar a roleta de acordo com as probabilidades
    for i in probabilidades:
        j = int(i*100/sum(probabilidades)) #quantidade inteira de elementos que serão acrecentados na roleta
        roleta.extend([n]*j)
        n+=1
    #faz o sorteio usando a roleta 
    sorteio = random.choice(roleta)
    return sorteio

#===============================================================
# inicializa matriz probabilidades
def iniMatrizes(pocos):
    for i in range(len(pocos)):
        n=0
        temp = []
        for j in range(len(pocos)):
            if i != j:
                tau = 1/matrizDistancias[i][j]
                temp.append({"tau":tau, "eta":eta, "tau_eta":(tau**alpha)*(eta**beta)})
                n += (tau**alpha)*(eta**beta)
            else:
                temp.append({"tau":0, "eta":0, "tau_eta":0})
        for j in temp:
            j["prob"]=(j["tau_eta"]/n)*100
        matrizProbabilidades[i]=temp
    return matrizProbabilidades
#===============================================================
# posiciona as formigas nos pontos
def posicionaFormigas(n_formigas, pocos):
    if len(pocos) > n_formigas:
        ini_rota = random.sample(range(len(pocos)),n_formigas)
        return ini_rota
    else:      
        n1 = int(n_formigas/len(pocos))
        n2 =   n_formigas % len(pocos)
        ini_rota = []
        for i in range(n1):
            ini_rota.extend(random.sample(range(len(pocos)),len(pocos)))
        ini_rota.extend(random.sample(range(len(pocos)),n2))
        return ini_rota

#===============================================================
# filtra as probabilidades
def filtra(matrizProbabilidades):
    filtro = []
    for i in range(len(matrizProbabilidades)):
        filtro.append(matrizProbabilidades[i]["prob"])
    return  filtro      

#===============================================================
# explora rotas
def exploraRotas(ini_rota, pocos, matrizProbabilidades):   
    rotas = []
    for i in ini_rota:
        temp =[]
        #montando uma lista auxiliar
        n = []
        a = 0
        while a < len(pocos):
            n.append(a)
            a += 1
            
        n.remove(i)
        temp.append(i)
        
        m = i      
        while len(n)>1:
            prob_total = filtra(matrizProbabilidades[m])
            prob = []
            #monta a lista prob apenas com os caminhos que ainda não foram percorridos
            for j in n:
                prob.append(prob_total[j])
            m = rodaRoleta(prob)
            m = n[m]
            temp.append(m)
            n.remove(m)
        temp.append(n[0])
        rotas.append(temp)
    return rotas

#===============================================================
# calcula distancia das rotas
def distanciaRotas(rotas, matrizDistancias):
    distancias = []
    for n in rotas:
        i = 0
        j = 1
        distancia = matrizDistancias[n[0]][n[len(n)-1]]
        while j < len(n):
            distancia += matrizDistancias[n[i]][n[j]]
            i +=1
            j +=1
        distancias.append(distancia)
    return distancias

#===============================================================
# atualiza Matriz Feromônio
def atualizaFeromonio(rotas, matrizFeromonios, distanciasTotais, sigma, q):
    #matrizFeromonios = [x*(1-sigma) for x in matrizFeromonios]
    a=0
    while a < len(matrizFeromonios[:][0]):
        temp = []
        for n in matrizFeromonios[a]:
            m = n*(1-sigma)
            if m < 0:
                temp.append(0)
            else:
                temp.append(m)
        matrizFeromonios[a] = temp
        a +=1
  
    a = 0
    for n in rotas:
        i = 0
        j = 1
        matrizFeromonios[n[0]][n[len(n)-1]] +=  q/distanciasTotais[a]
        while j < len(n):
            matrizFeromonios[n[i]][n[j]] += q/distanciasTotais[a]
            i +=1
            j +=1
        a +=1
    return matrizFeromonios

#===============================================================
# atualiza Matriz Probabilidades
def atualizaMatrizProbabilidades(matrizProbabilidades, matrizFeromonios):
    for i in range(len(pontos)):
        n=0
        temp = []
        for j in range(len(pontos)):
            if i != j:
                tau = 1/matrizDistancias[i][j]
                eta =  matrizFeromonios[i][j]
                temp.append({"tau":tau, "eta":eta, "tau_eta":(tau**alpha)*(eta**beta)})
                n += (tau**alpha)*(eta**beta)
            else:
                temp.append({"tau":0, "eta":0, "tau_eta":0})
        for j in temp:
            j["prob"]=(j["tau_eta"]/n)*100
        matrizProbabilidades[i]=temp
    return matrizProbabilidades
#===============================================================
def geraPontos(n_pontos):
    pontos = []
    i = 0
    while i < n_pontos:
        pontos.append(random.sample(range(500), 2))
        i += 1          
    return pontos
#===============================================================
def geraMatrizDistancias(pontos):
    matrizDistancias = []
    i = 0
    while i < len(pontos):
        j = 0
        temp = []
        while j < len(pontos):
            if j != i:
                temp.append( sqrt((pontos[i][0]-pontos[j][0])**2 + (pontos[i][1]-pontos[j][1])**2))
            else:
                temp.append(0)
            j += 1
        matrizDistancias.append(temp)
        i += 1
    return matrizDistancias
#===============================================================
# Main 
    
pontos = geraPontos(n_pontos)
matrizDistancias = geraMatrizDistancias(pontos)
matrizProbabilidades = matrizProbabilidades = [[0]*(len(pontos))]*(len(pontos))
 
matrizProbabilidades = iniMatrizes(pontos)
ini_rota = posicionaFormigas(n_formigas, pontos)


i = 0
while i < iteracoes:
    rotas = exploraRotas(ini_rota, pontos, matrizProbabilidades)
    distanciasTotais = distanciaRotas(rotas,matrizDistancias)
    matrizFeromonios = atualizaFeromonio(rotas, matrizFeromonios, distanciasTotais, sigma, q)
    matrizProbabilidades = atualizaMatrizProbabilidades(matrizProbabilidades, matrizFeromonios)
    i += 1
    
#i = 0
#showRotas = []
#while i < len(rotas):
#    temp = ""
#    for n in rotas[i]:
#        temp = temp + str(n)
#    temp = temp + temp[0]
#    showRotas.append(temp)    
#    i += 1

print(distanciasTotais)    
print(rotas)

#==============================================================================================
# Tela TKINTER

top = tkinter.Tk()
top.title("Algoritmo Colonia de Formigas")

C = tkinter.Canvas(top, height=500, width=800)

i = 0
while i < len(pontos):
    C.create_rectangle(pontos[i][0] - 5, 500 - pontos[i][1] + 5, pontos[i][0] + 5, 500 - pontos[i][1] - 5,fill='red')
    j = i+1
    while j < len(pontos):
        C.create_line(pontos[i][0],500 - pontos[i][1], pontos[j][0],500 - pontos[j][1] , fill='gray', width=1)
        j +=1
    i += 1

#Traçar a Rota final no gráfico
final = rotas[distanciasTotais.index(min(distanciasTotais))]
C.create_line(pontos[final[0]][0],500 - pontos[final[0]][1], pontos[final[len(final)-1]][0],500 - pontos[final[len(final)-1]][1] , fill='blue', width=2)
i = 0
while i < len(final)-1:
    C.create_line(pontos[final[i]][0],500 - pontos[final[i]][1], pontos[final[i+1]][0],500 - pontos[final[i+1]][1] , fill='blue', width=2)
    i += 1


C.pack()
top.mainloop()