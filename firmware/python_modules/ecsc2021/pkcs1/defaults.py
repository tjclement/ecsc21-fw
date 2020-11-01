import random, os


class CryptoRandom:
    @staticmethod
    def getrandbits(bits):
        return int.from_bytes(os.urandom(bits//8), 'big')

    @staticmethod
    def randint(a, b):
        return random.randint(a, b)


default_crypto_random = CryptoRandom
default_pseudo_random = random
