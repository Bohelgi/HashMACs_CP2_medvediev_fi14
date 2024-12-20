from redundancy import Redundancy
import tools

truncation = 16
N = 10000

def first_attack():
    k_exponent = [10, 12, 14]
    l_exponent = [5, 6, 7]

    for k in k_exponent:
        for l in l_exponent:
            success = 0
            redundancy_function = Redundancy(128 - truncation)
            redundancy_table = tools.get_redundancy_table(k, l, redundancy_function, truncation)

            L = 2**l
            for i in range(N):
                random_hash = tools.ripemd160(tools.random_bytes(256))[36:]
                for j in range(L):
                    if tools.binary_search(redundancy_table, random_hash):
                        success += 1
                        break
                    else:
                        random_hash = tools.ripemd160(redundancy_function.get(random_hash))[36:]
            
            print("---New Attack---")
            print(f"K: 2^{k}")
            print(f"L: 2^{l}")
            print(f"Prediction by Hellman: {tools.prediction_by_hellman(2**k, 2**l, truncation)}")
            print(f"Success rate: {success / N}\n")

def second_attack():
    k_exponent = [10, 12, 14]
    l_exponent = [5, 6, 7]

    for k in k_exponent:
        K = 2**k
        for l in l_exponent:
            success = 0
            redundancy_tables = {}
            L = 2**l
            for i in range(K):
                redundancy_function = Redundancy(128 - truncation)
                redundancy_table = tools.get_redundancy_table(k, l, redundancy_function, truncation)
                redundancy_tables[redundancy_function] = redundancy_table
            
            for i in range(N):
                hashes = [tools.ripemd160(tools.random_bytes(256))[36:] for _ in range(L)]
                out = False
                for j in range(L):
                    for redundancy_function, redundancy_table in redundancy_tables.items():
                        if tools.binary_search(redundancy_table, hashes[j]):
                            success += 1
                            out = True
                            break
                        else:
                            hashes[j] = tools.ripemd160(redundancy_function.get(hashes[j]))[36:]
                    if out:
                        break

            print("---New Attack---")
            print(f"K: 2^{k}")
            print(f"L: 2^{l}")
            print(f"Prediction by Hellman: {tools.prediction_by_hellman(2**k, 2**l, truncation)}")
            print(f"Success rate: {success / N}\n")
                

if __name__ == "__main__":
    # first_attack()
    second_attack()
