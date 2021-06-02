import numpy as np
from numpy.core.shape_base import block

class encoder:

    def __init__(self, n):
        self.block_size = n
        self.codewords_size = 2**n

        self.codewords = self.construct_codewords(n)

    def construct_codewords(self,n):
        c = np.array([1]).reshape((1,1))

        for loop in range(n):
            c = self.next_codewords(c)
        return c

    def next_codewords(self,c):
        c1 = np.concatenate([c,c], axis=1)
        c2 = np.concatenate([c,-c], axis=1)
        return np.concatenate([c1,c2], axis=0)
    
    def index(self,block):
        return int(np.sum(2**np.arange(block.size)*block))

    #block an numpy array of length n
    def encode_block(self, block):
        index = self.index((block+1)//2)
        return self.codewords[index,:]

    
    def dist(self, arrays, array):
        return  np.sum((arrays - array)**2, axis = 1)
    
    def index_to_block(self, index):
        block = np.zeros((self.block_size), dtype=int)
        curr = 0
        while index != 0:
            block[curr] = index & 1
            index = index >> 1
            curr = curr + 1
        return (block*2)-1

    def decode_block(self, block):
        block = block.reshape((1,-1))
        index = np.argmin(self.dist(self.codewords,block))
        return self.index_to_block(index)

    #first block is used to know how many bits were used for paddind
    def pad(self, bits):
        nb_pad = self.block_size - (bits.size % self.block_size)
        padding = np.ones((nb_pad))
        return np.concatenate([self.index_to_block(nb_pad),bits,padding])
    
    def unpad(self, bits):
        nb_pad = self.index((bits[:self.block_size]+1)//2)
        return bits[self.block_size:-nb_pad]

    #TODO :: add padding in case bits_size is not mutiple of block_size
    def encode(self, bits):
        bits = self.pad(bits)
        nb_blocks = bits.size/self.block_size
        blocks = np.split(bits, nb_blocks)

        encoded = []
        for block in blocks:
            encoded.append(self.encode_block(block))
        return np.concatenate(encoded)
    
    def decode(self, channel_output):
        nb_blocks = channel_output.size/self.codewords_size
        blocks = np.split(channel_output, nb_blocks)

        reconstructed = []
        for block in blocks:
            if len(reconstructed)%10 == 0:
                print(len(reconstructed))
            reconstructed.append(self.decode_block(block))
        return self.unpad(np.concatenate(reconstructed))


        


# # constructs C_n given n
# def construct_c(n, c_0):
#     if n == 0:
#         return c_0   
#     c_n = []
#     for i in range(n):
#         c_i = []
#         for c in c_0:
#             c_i.append(np.block([c,c]))
#             c_i.append(np.block([c, -c]))
#         c_n = construct_c(i, c_i)
#     return c_n

# # constructs all possible bit permutation of length n
# def per(n):
#     permutations = []
#     for i in range(1 << n):
#         s = bin(i)[2:]
#         s = '0' * (n - len(s)) + s
#         permutations.append(s)
#     return permutations

# # constructs the map from bit sequence of length n (string, ex: '010') to codeword of length 2^n (ex: [1, -1, 1, -1, 1, -1, 1, -1])
# def mapping(n):
#     permutations = per(n)
#     codewords = construct_c(n, [1])

#     map = {}
#     for i in range(pow(2,n)):
#         map.update({permutations[i]: codewords[i]})

#     return map

# # encodes blocks of bits of length n 
# # bits is a string of bits 0 and 1
# def encode(bits, n):
#     map = mapping(n)
#     sequence = []
#     for b in range(0, len(bits), n):
#         sequence.append(map.get(bits[b:b+n]))
#     return np.concatenate(sequence)

def channel(chanInput):
    chanInput = np.clip(chanInput,-1,1)
    erasedIndex = np.random.randint(3)
    chanInput[erasedIndex:len(chanInput):3] = 0
    return chanInput + np.sqrt(10)*np.random.randn(len(chanInput))

if __name__ == '__main__':
    encoder = encoder(10)
    data = np.array([-1,1,1])
    encoded = encoder.encode(data)
    print(encoded)
    channel_output = channel(encoded)

    print(encoder.decode(channel_output))






