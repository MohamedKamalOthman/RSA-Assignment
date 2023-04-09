# This script is used to analyze how the number of bits affect the attack time of RSA algorithm
# The attack is done by factoring the n value of the RSA algorithm

# First we need to import the necessary libraries
import time
import RSA
import matplotlib.pyplot as plt

# Generate RSA keys
rsa_victim = RSA.RSA()
rsa_victim.suppress_print = True
rsa_attacker = RSA.RSA()


# known plaintext message
message = "Hello World"


# factorize n
def factor(n):
    # initialize p and q
    p = 0
    q = 0
    # loop over all numbers from 1 to n
    for i in range(1, int((n + 1) ** (1 / 2))):
        # if i is a factor of n
        if n % i == 0:
            p = i
            q = n // i
    return p, q


encryption_times = []
decryption_times = []
attack_times = []
# loop over different number of bits from 1 to 28
for i in range(2, 20):
    # generate keys
    rsa_victim.bits = i
    n, e = rsa_victim.generate_keys()
    # attack by factorising n
    start = time.time()
    p, q = factor(n)
    end = time.time()
    attack_times.append(end - start)

# plot attack with matplotlib
plt.plot(attack_times)
plt.title("Attack time vs number of bits")
plt.xlabel("Number of bits")
plt.ylabel("Attack time (s)")
plt.show()

# analyze the encryption/decryption time
for i in range(2, 1024):
    # generate keys
    rsa_victim.bits = i
    n, e = rsa_victim.generate_keys()
    rsa_victim.set_public_key(n, e)
    # encode message
    start = time.time()
    cipher = rsa_victim.encode(message)
    end = time.time()
    encryption_times.append(end - start)
    # decode message
    start = time.time()
    message = rsa_victim.decode(cipher)
    end = time.time()
    decryption_times.append(end - start)

# plot encryption time
plt.plot(encryption_times)
plt.title("Encryption time vs number of bits")
plt.xlabel("Number of bits")
plt.ylabel("Encryption time (s)")
plt.show()

# plot decryption time
plt.plot(decryption_times)
plt.title("Decryption time vs number of bits")
plt.xlabel("Number of bits")
plt.ylabel("Decryption time (s)")
plt.show()
