# This script is used to analyze how the number of bits affect the attack time of RSA algorithm
# The attack is done by factoring the n value of the RSA algorithm

# First we need to import the necessary libraries
import time
import RSA
import matplotlib.pyplot as plt

# Generate RSA keys
rsa_victim = RSA.RSA()
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

times = []
# loop over different number of bits from 1 to 28
for i in range(2, 28):
    # generate keys
    rsa_victim.bits = i
    n, e = rsa_victim.generate_keys()
    # encode message
    cipher = rsa_victim.encode(message)
    # start timing
    start = time.time()
    # factor n
    p, q = factor(n)
    # end timing
    end = time.time()
    times.append(end - start)
    
# plot the results with matplotlib log scale
plt.plot(times)
plt.show()