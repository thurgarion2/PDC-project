import numpy as np

class encoder:

    def __init__(self):
        self.block_size = 9
        self.codewords = self.construct_codewords()
        self.codewords_size = self.codewords.shape[1]
        

    def construct_codewords(self):
        c_9 = self.construct_cn(9)
        c_8 = self.construct_cn(8)
        c_8 = np.concatenate([c_8,c_8],axis=0)

        return np.concatenate([c_9,c_8],axis=1)

    def construct_cn(self,n):
        c = np.array([1]).reshape((1,1))

        for loop in range(n):
            c = self.next_codewords(c)
        return c[:,1:]

    

    def next_codewords(self,c):
        c1 = np.concatenate([c,c], axis=1)
        c2 = np.concatenate([c,-c], axis=1)
        return np.concatenate([c1,c2], axis=0)

    def decode(self, channel_output):

        erasedIndex = self.find_erased_bit(channel_output)

        nb_blocks = channel_output.size/self.codewords_size
        blocks = np.split(channel_output, nb_blocks)

      
        reconstructed = []
        for block in blocks:
            reconstructed.append(self.decode_block(block, erasedIndex))
            erasedIndex = (erasedIndex - (self.codewords_size) % 3 + 3)%3
           

      
        return self.unpad(np.concatenate(reconstructed))

    def encode(self, bits):
        bits = self.pad(bits)
        nb_blocks = bits.size/self.block_size
        blocks = np.split(bits, nb_blocks)

        encoded = []
        for block in blocks:
            encoded.append(self.encode_block(block))
        return np.concatenate(encoded)
    

    #block an numpy array of length n
    def encode_block(self, block):
        index = self.index((block+1)//2)
        return self.codewords[index,:]
    
    def index(self,block):
        return int(np.sum(2**np.arange(block.size)*block))



    def decode_block(self, block, erasedIndex):
        
        
        block[erasedIndex::3] = 0

        block = block.reshape((1,-1))
        index = np.argmin(self.dist(self.codewords,block))
        return self.index_to_block(index)
    
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

    def find_erased_bit(self, bits):
        possible = [bits[::3],bits[1::3],bits[2::3]]
        return np.argmin([np.sum(b**2) for b in possible])


    #first block is used to know how many bits were used for paddind
    def pad(self, bits):
        nb_pad = self.block_size - (bits.size % self.block_size)
        padding = np.ones((nb_pad))
        return np.concatenate([self.index_to_block(nb_pad),bits,padding])
    
    def unpad(self, bits):
        nb_pad = max(self.index((bits[:self.block_size]+1)//2),1)
        return bits[self.block_size:-nb_pad]
   
            