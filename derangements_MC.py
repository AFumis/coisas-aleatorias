import random
import time

#coloque aqui as pessoas que participam do amigo secreto
pessoas=['A','B','C','D','E']
#para cada pessoa, coloque em sua respectiva (pelo index) lista quem ela nao pode tirar 
restri=[['B','D'],['A'],[],['E'],['A']]

def main():
    n=int(input('Digite n: '))
    t=time.time()
    cont=0
    for i in range(n):
        der=derangement(pessoas)
        cont+=testa(der,restri)
    print('Runtime: ',time.time()-t, 'seconds')
    print('n = ',n)
    print('cont = ',cont)
    print('Prob de não ter "marmelada": %.2f' % (100*cont/n),'%')
    

def derangement(lista):
#adaptado de https://stackoverflow.com/questions/25200220/generate-a-random-derangement-of-a-list
    while True:
        v = lista[:]
        for j in range(len(v) - 1, -1, -1):
            p = random.randint(0, j)
            if v[p] == lista[j]:
                break
            else:
                v[j], v[p] = v[p], v[j]
        else:
            if v[0] != lista[0]:
                return v
            
def testa(l,rest):
    t=1
    for i in range(len(l)):
        if l[i] in rest[i]:
            t=0
            break
    return t
    
if __name__ == "__main__":
    main()