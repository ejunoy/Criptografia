def mcd(a,b):
    if(a==0 or b ==0):
        return 0
    if(a == 1):
        return 1
    if b>=a:
        modulo = b%a 
        div = (b-b%a)/a 
        if modulo==0:
            return int(div) 
        else:
            return mcd(modulo,div)
    else:
        return mcd(b,a)

def hill():
    contador = 0
    for a in range(26):
        for b in range(26):
            for c in range(26):
                for d in range(26):
                    det = a*d-b*c 
                    if mcd(det, 26)==1:
                        contador = contador+1
                        print(f"{a} {b}\n")
                        print(f"{c} {d}\n")
                        print(f"determinante: {det}\n\n")
    return contador

total = hill()
print(f"En total hay {total} matrices invertibles módulo 26")
