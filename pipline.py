import numpy as np

text = './default_text.txt'

def access_bit(data, num):
    shift = int(num % 8)
    return (data & (1<<shift)) >> shift

def to_bit_array(byte_array):
    bits = []

    for byte in byte_array:
        for i in range(8):
            bits.append(access_bit(byte, i))
    return np.array(bits)

def to_byte_array(bit_array):
    return np.packbits(bit_array, bitorder='little')

## 1 -> 1
## 0 -> -1
def bit_array_to_channel_fromat(bit_array):
    return 2*np.array(bit_array) - 1

#(no noise)
def channel_fromat_to_bit_array(bit_array):
    return (np.array(bit_array) + 1) // 2

def byte_array_to_channel_fromat(byte_array):
    return bit_array_to_channel_fromat(to_bit_array(byte_array))

def channel_fromat_to_byte_array(channel_fromat):
    return to_byte_array(channel_fromat_to_bit_array(channel_fromat)).tobytes()

##encoding='utf-8'
#channel fromat is a numpy array
with open(text, 'rb') as f:
    data = f.read()
   
    channel = byte_array_to_channel_fromat(data)
    text = channel_fromat_to_byte_array(channel)

    print(text.decode())
    
