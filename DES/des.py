def byteToChar(bits):
    numero = 0
    for i in range(8):
        bit = bits[7-i]
        numero = numero + bit*(2**i)
    return chr(numero)


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
    def hola():
        print("hola")


class Block64(Block):
    def left(self):
        return Block32(self.text[:4])
    def right(self):
        return Block32(self.text[4:])
    def initialPermutation(self):
        permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                       60, 52, 44, 36, 28, 20, 12, 4,
                       62, 54, 46, 38, 30, 22, 14, 6,
                       64, 56, 58, 40, 32, 24, 16, 8,
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
                              64, 56, 58, 40, 32, 24, 16, 8,
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
        

