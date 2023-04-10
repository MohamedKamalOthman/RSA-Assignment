import random
from Mapping import MAPPING, INVERSE_MAPPING
from Crypto.Util import number
import os


class RSA:
    """RSA encryption and decryption class"""

    def __init__(self):
        """Initialize RSA object"""
        self.suppress_print = False
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None
        self.pn = None
        self.bits = 1024

    def generate_keys(self) -> tuple:
        """Generate public and private keys"""
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
        while self.__egcd(e, phi)[0] != 1:
            e = random.randint(1, phi)
        # compute d where (d * e) % phi(n) = 1
        self.d = self.__modular_inverse(e, phi)
        # return public key (n, e)
        if not self.suppress_print:
            print("Finished generating keys")
            print("Public key: ", (self.n, e))
        return (self.n, e)

    def set_public_key(self, pn, e):
        """Set the public key (n, e)"""
        self.pn, self.e = pn, e

    def encode(self, message: str) -> list:
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
        """Decode a list of cipher text blocks into a message"""
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
            # reverse the block and append it to the message
            message += block[::-1]
        return message

    @staticmethod
    def __fast_modular_exponentiation(b, e, m) -> int:
        """Calculate (b^e) % m"""
        r = 1
        # if last bit is 1 then set r = b
        if 1 & e:
            r = b
        while e:
            e >>= 1
            # update b to b^2 % m
            b = (b * b) % m
            # if last bit is 1 then update r to r * b % m
            if e & 1:
                r = (r * b) % m
        return r

    @staticmethod
    def __egcd(a, b) -> tuple:
        """Extended Euclidean Algorithm for calculating the modular inverse"""
        p1 = 1
        q1 = 0
        h1 = a
        p2 = 0
        q2 = 1
        h2 = b

        while h2 != 0:
            r = h1 // h2
            p3 = p1 - r * p2
            q3 = q1 - r * q2
            h3 = h1 - r * h2
            p1 = p2
            q1 = q2
            h1 = h2
            p2 = p3
            q2 = q3
            h2 = h3

        return h1, p1, q1

    @staticmethod
    def __modular_inverse(e, phi) -> int:
        """Calculate the modular inverse of e and phi"""
        _, x, _ = RSA.__egcd(e, phi)
        return x % phi

    @staticmethod
    def __convert_block(block) -> int:
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
