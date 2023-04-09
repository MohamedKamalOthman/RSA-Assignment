import random
from Mapping import MAPPING, INVERSE_MAPPING
from Crypto.Util import number
import os


class RSA:
    def __init__(self):
        self.suppress_print = False
        self.primes = None
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None
        self.bits = 1024

    def generate_keys(self):
        if not self.suppress_print:
            print("Generating keys...")
            print("Generating p and q...")
        # generate p and q
        self.p = number.getPrime(self.bits, randfunc=os.urandom)
        self.q = number.getPrime(self.bits, randfunc=os.urandom)
        # compute n
        self.n = self.p * self.q
        # compute phi(n)
        phi = (self.p - 1) * (self.q - 1)
        # compute e where 1 < e < phi(n) and gcd(e, phi(n)) = 1
        e = random.randint(1, phi)
        while self.__gcd(e, phi) != 1:
            e = random.randint(1, phi)
        # compute d where (d * e) % phi(n) = 1
        self.d = self.__modular_inverse(e, phi)
        # return public key (n, e)
        if not self.suppress_print:
            print("Finished generating keys")
            print("Public key: ", (self.n, e))
        return (self.n, e)

    def set_public_key(self, pn, e):
        self.pn, self.e = pn, e
        pass

    def encode(self, message: str):
        if self.p is None or self.q is None:
            raise Exception("p and q must be generated first")
        # split message into blocks of 5 characters and append space if necessary
        blocks = [message[i : i + 5] for i in range(0, len(message), 5)]
        if len(blocks[-1]) < 5:
            blocks[-1] += " " * (5 - len(blocks[-1]))
        # convert each block to a number
        blocks = [self.__convert_block(block) for block in blocks]
        # convert each number to cipher text using fast modular exponentiation
        blocks = [
            self.__fast_modular_exponentiation(block, self.d, self.n)
            for block in blocks
        ]
        return blocks

    def decode(self, ciphertext_blocks) -> str:
        if self.pn is None or self.e is None:
            raise Exception("n and e must be set first first")
        # convert cipher text to message using fast modular exponentiation
        message = ""
        for cipher in ciphertext_blocks:
            block = ""
            deciphered = self.__fast_modular_exponentiation(cipher, self.e, self.pn)
            for _ in range(5):
                m = deciphered % 37
                deciphered //= 37
                block += INVERSE_MAPPING.get(m, " ")
            message += block[::-1]
        return message

    def __generate_primes(self):
        self.primes = [
            i
            for i in range(2 ** (self.bits - 1), 2 ** (self.bits))
            if self.__is_prime(i)
        ]

    @staticmethod
    def __is_prime(n):
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        r = int(n**0.5)
        f = 5
        while f <= r:
            if n % f == 0:
                return False
            if n % (f + 2) == 0:
                return False
            f += 6
        return True

    @staticmethod
    def __gcd(a, b):
        """Calculate the Greatest Common Divisor of a and b. using Euclid's Algorithm"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def __modular_inverse(e, phi):
        """Calculate the modular inverse of e % phi(n)"""
        return pow(e, -1, phi)

    @staticmethod
    def __fast_modular_exponentiation(b, e, m):
        """Calculate (b^e) % m"""
        return pow(b, e, m)

    @staticmethod
    def __get_mapping(char: str) -> int:
        return MAPPING.get(char, 36)

    @staticmethod
    def __convert_block(block):
        sum = 0
        for i in range(len(block)):
            sum += MAPPING.get(block[i], 36) * 37 ** (4 - i)
        return sum


def test():
    print("RSA.py loaded")
    rsa = RSA()
    keys = rsa.generate_keys()
    rsa.set_public_key(*keys)
    cipher = rsa.encode("hello world, i am a message")
    print(cipher)
    print(rsa.decode(cipher))


# test()
