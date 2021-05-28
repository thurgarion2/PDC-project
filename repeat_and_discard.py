import numpy as np

class encoder:

    def __init__(self, n):
        self.block_size = 3*n
        self.padding = 3*50

        self.erased_block_size = 2*n
        self.possible_block = np.ones((self.erased_block_size,2))
        self.possible_block[:,1] = - self.possible_block[:,1]
        self.choice_to_bit = {0 : 1, 1 : -1}


    def padd(self):
        return np.ones((self.padding))

    #bits : numpy array composed of (-1,1)
    def encode(self, bits):
        blocks = [self.padd()]

        for b in bits:
           blocks.append(np.ones((self.block_size))*b) 

        return np.concatenate(blocks)
    
    def find_erased_bit(self, padded_bit):
        return np.argmin([np.sum(padded_bit[i::3]) for i in range(3)]) 

    def remove_erased_bit(self, erase_bit, block):
        mask = [i for i in range(self.block_size) if i%3!=erase_bit]
        return block[mask]
    
    def dist(self, arrays, array):
        return  np.sum((arrays - array)**2, axis = 0)

    def decode_block(self, erase_bit, block):
        block = self.remove_erased_bit(erase_bit, block)

        block = block.reshape((-1,1))
        choice = np.argmin(self.dist(self.possible_block, block))
        return self.choice_to_bit[choice]


    def decode(self, channel_output):
        erase_bit = self.find_erased_bit(channel_output[:self.padding])

        nb_blocks = channel_output[self.padding:].size / self.block_size
        blocks = np.split(channel_output[self.padding:], nb_blocks)

        reconstructed = []
        for block in blocks:
            reconstructed.append(self.decode_block(erase_bit,block))
        
        return np.array(reconstructed, dtype= int)