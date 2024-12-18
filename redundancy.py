import os

class Redundancy:
    def __init__(self, n: int):
        byte_length = (n + 7) // 8  # Convert bit length to byte length
        random_bytes = os.urandom(byte_length)  # Generate random bytes
        self.r = random_bytes.hex()

    def get(self, x: str) -> str:
        return self.r + x