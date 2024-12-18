import os
from Crypto.Hash import RIPEMD160
from redundancy import Redundancy

def random_bytes(bits: int) -> bytes:
    byte_length = (bits + 7) // 8 
    return os.urandom(byte_length).hex()

def ripemd160(msg: str) -> str:
    h = RIPEMD160.new()
    h.update(bytes.fromhex(msg))
    return h.hexdigest()

def get_redundancy_table(k_exp: int, l_exp: int, r_f: Redundancy, truncation: int) -> dict:
    k = 2**k_exp
    l = 2**l_exp
    redundancy_table = {}
    for i in range(k):
        x_0 = random_bytes(truncation)
        x_prev = x_0
        for j in range(l):
            x_prev = ripemd160(r_f.get(x_prev))[36:]
        redundancy_table[x_0] = x_prev
    return redundancy_table

def prediction_by_hellman(k: int, l: int, truncation: int) -> float:
    n = 2**truncation

    sum = float(0)
    for i in range(1, k+1):
        for j in range(l):
            sum += (1 - (i*l)/n)**(j+1)
    
    return sum / float(n)
