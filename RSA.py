import random
from Mapping import MAPPING, INVERSE_MAPPING
from Crypto.Util import number
import os


class RSA:
    def __init__(self):
        self.suppress_print = False
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None
        self.pn = None
        self.bits = 1024

    def generate_keys(self):
        if not self.suppress_print:
            print("Generating keys...")
            print("Generating p and q...")
        # generate p and q
        self.p = number.getPrime(int(self.bits / 2), randfunc=os.urandom)
        self.q = number.getPrime(int(self.bits / 2 + 1), randfunc=os.urandom)
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

    def encode(self, message: str):
        if self.pn is None or self.e is None:
            raise Exception("n and e must be set first first")
        # split message into blocks of 5 characters and append space if necessary
        blocks = [message[i : i + 5] for i in range(0, len(message), 5)]
        if len(blocks[-1]) < 5:
            blocks[-1] += " " * (5 - len(blocks[-1]))
        # convert each block to a number
        blocks = [self.__convert_block(block) for block in blocks]
        # convert each number to cipher text using fast modular exponentiation
        blocks = [
            self.__fast_modular_exponentiation(block, self.e, self.pn)
            for block in blocks
        ]
        return blocks

    def decode(self, ciphertext_blocks) -> str:
        """"""
        if self.d is None or self.n is None:
            raise Exception("d and n must be generated first")
        # convert cipher text to message using fast modular exponentiation
        message = ""
        for cipher in ciphertext_blocks:
            block = ""
            deciphered = self.__fast_modular_exponentiation(cipher, self.d, self.n)
            for _ in range(5):
                m = deciphered % 37
                deciphered //= 37
                block += INVERSE_MAPPING.get(m, " ")
            message += block[::-1]
        return message

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
        r = 1
        if 1 & e:
            r = b
        while e:
            e >>= 1
            b = (b * b) % m
            if e & 1:
                r = (r * b) % m
        return r

    @staticmethod
    def __convert_block(block):
        """Convert a block of 5 characters to a number"""
        sum = 0
        for i in range(len(block)):
            sum += MAPPING.get(block[i], 36) * 37 ** (4 - i)
        return sum


def test():
    """Test RSA.py"""
    rsa = RSA()
    rsa.suppress_print = True
    message = "1234554321"
    keys = rsa.generate_keys()
    rsa.set_public_key(*keys)
    cipher = rsa.encode(message)
    decoded_message = rsa.decode(cipher)
    # assert that the message is the same after encoding and decoding if not then print the differences
    assert (
        message == decoded_message
    ), f"message: {message} decoded_message: {decoded_message}"


test()
