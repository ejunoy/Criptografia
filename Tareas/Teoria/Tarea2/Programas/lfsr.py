def push(estado, valor):
    copia = estado.copy()
    copia[0]=valor
    for i in range(1,len(estado)):
        copia[i]=estado[i-1]
    return copia

def calcPush(lugares, estado):
    valor = 1
    for i in lugares:
        lugar = i-1 
        valor = (valor+estado[lugar])%2
    return valor 

def siguienteEstado(lugares, estado):
    valor = calcPush(lugares, estado)
    nuevoEstado = push(estado, valor)
    return nuevoEstado

def comparar(estado1,estado2):
    if len(estado1) != len(estado2):
        return False
    for i in range(len(estado1)):
        if estado1[i]!=estado2[i]:
            return False
    return True


def lfsr(lugares, seed):
    estados=[seed]
    while(True):
        estadoActual = estados[-1]
        estado = siguienteEstado(lugares, estadoActual)
        repetido = False
        for estado2 in estados:
            if comparar(estado, estado2):
                repetido = True
                break
        if(repetido):
            return estados
        else:
            estados.append(estado)

def alAzar(lugares,seed):
    estados = lfsr(lugares,seed)
    lista = []
    for estado in estados:
        lista.append(estado[-1])
    return lista

