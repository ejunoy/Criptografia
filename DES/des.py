def byteToChar(bits):
    numero = 0
    for i in range(8):
        bit = bits[7-i]
        numero = numero + bit*(2**i)
    return chr(numero)

def groupToMatrix(bits):
    row = bits[5]+2*bits[0]
    column = bits[4]+2*bits[3]+4*bits[2]+8*bits[1]
    return {"row":row, "column":column}


class Block():
    def __init__(self,text):
        self.text = text
    
    def numbers(self):
        numbers = []
        for letter in self.text: 
            number = ord(letter)
            numbers.append(number)
        return numbers

    def bits(self):
        numbers = self.numbers()
        bits = []
        for number in numbers:
            numberBits = []
            for power in range(8):
                numberBits.append(int((number&(2**power))/(2**power)))
            for i in range(len(numberBits)):
                bits.append(numberBits[len(numberBits)-1-i])
        return bits

class Block32(Block):
    def expand(self):
        expansion = [
                32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9,
                8, 9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1
                ]
        bits = self.bits()
        expandido = []
        for entrada in expansion:
            expandido.append(bits[entrada-1])
        string = ""
        for byte in range(6):
            bits = expandido[8*byte: 8*(byte+1)]
            letter = byteToChar(bits)
            string = string + letter 
        return Block48(string)


class Block48(Block):
    def xor(self,key):
        bits = self.bits()
        bitsKey = key.bits()
        finalBits = []
        for i in range(48):
            finalBits.append(bits[i]^bitsKey[i])
        string = ""
        for byte in range(6):
            bits = finalBits[8*byte: 8*(byte+1)]
            letter = byteToChar(bits)
            string = string+letter 
        return Block48(string)
    def split(self):
        bits = self.bits()
        grupos = []
        for i in range(8):
            grupos.append(bits[6*i:6*(i+1)])
        return grupos
    
    def applySBoxes(self):
        sBoxes = [
            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 0, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 5, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, ,9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]], 
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], 
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], 
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10 ,14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], 
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
        ]
        groups = self.split()
        for i in range(8):
            sBox = sBoxes[i]
            group = groups[i]
            toMatrix = groupToMatrix(group)
            row = toMatrix["row"]
            col = toMatrix["column"]
            value = sBox[row,col]
            bits = []






class Block64(Block):
    def left(self):
        return Block32(self.text[:4])
    def right(self):
        return Block32(self.text[4:])
    def initialPermutation(self):
        permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                       60, 52, 44, 36, 28, 20, 12, 4,
                       62, 54, 46, 38, 30, 22, 14, 6,
                       64, 56, 48, 40, 32, 24, 16, 8,
                       57, 49, 41, 33, 25, 17, 9, 1,
                       59, 51, 43, 35, 27, 19, 11, 3,
                       61, 53, 45, 37, 29, 21, 13, 5,
                       63, 55, 47, 39, 31, 23, 15, 7]
        bits = self.bits()
        newBits = bits.copy()
        for i in range(64):
            newBits[i] = bits[permutation[i]-1]
        string = ""
        for byte in range(8):
            bits = newBits[8*byte:8*(byte+1)]
            letter = byteToChar(bits)
            string = string+letter
        return Block64(string)

    def finalPermutation(self):
        initialPermutation = [58, 50, 42, 34, 26, 18, 10, 2,
                              60, 52, 44, 36, 28, 20, 12, 4,
                              62, 54, 46, 38, 30, 22, 14, 6,
                              64, 56, 48, 40, 32, 24, 16, 8,
                              57, 49, 41, 33, 25, 17, 9, 1,
                              59, 51, 43, 35, 27, 19, 11, 3,
                              61, 53, 45, 37, 29, 21, 13, 5,
                              63, 55, 47, 39, 31, 23, 15, 7]
        permutation = initialPermutation.copy()
        for i in range(64):
            for j in range(64):
                if i == initialPermutation[j]-1:
                    permutation[i]=j+1
                    break
        bits = self.bits()
        newBits = bits.copy()
        for i in range(64):
            newBits[i] = bits[permutation[i]-1]
        string = ""
        for byte in range(8):
            bits = newBits[8*byte:8*(byte+1)]
            letter = byteToChar(bits)
            string = string+letter
        return Block64(string)
        

