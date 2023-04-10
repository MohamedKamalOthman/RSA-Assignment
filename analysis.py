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
message = "hi s7"


def encryption_decryption_analysis():
    """Analyze the encryption/decryption time of RSA algorithm"""
    global rsa_victim, rsa_attacker, message
    decryption_times = []
    encryption_times = []
    x_axis = range(16, 2048, 8)
    # analyze the encryption/decryption time
    for i in x_axis:
        # generate keys
        rsa_victim.bits = i
        n, e = rsa_victim.generate_keys()
        rsa_victim.set_public_key(n, e)
        # encode message
        start = time.time_ns()
        cipher = rsa_victim.encode(message)
        end = time.time_ns()
        encryption_times.append((end - start) / 1e6)
        # decode message
        start = time.time_ns()
        message = rsa_victim.decode(cipher)
        end = time.time_ns()
        decryption_times.append((end - start) / 1e6)

    # plot encryption time
    plt.plot(x_axis, encryption_times)
    # plot decryption time
    plt.plot(x_axis, decryption_times)
    plt.title("Encryption/Decryption time vs number of bits")
    plt.xlabel("Number of bits")
    plt.ylabel("time (ms)")
    plt.legend(["Encryption", "Decryption"])
    # save the plot
    plt.savefig("encryption_decryption_time.png")
    plt.close()


def brute_force_analysis():
    """Analyze the attack time of RSA algorithm by brute force"""
    global rsa_victim, rsa_attacker, message

    brute_force_times = []
    x_axis = range(27, 32)

    # loop from 1 to 30 bits brute force attack
    for i in x_axis:
        # Set the number of bits
        rsa_victim.bits = i
        # Generate keys
        n, e = rsa_victim.generate_keys()
        rsa_victim.set_public_key(n, e)
        rsa_attacker.n = n
        # Encode message
        cipher = rsa_victim.encode(message)
        start = time.time_ns()
        # loop over all possible values of d
        for j in range(0, 2**i):
            rsa_attacker.d = j
            # if the decrypted message is the same as the original message then break
            if rsa_attacker.decode(cipher) == message:
                print("Cracked Private Key: ", j)
                break
        end = time.time_ns()
        brute_force_times.append((end - start) / 1e9)

    # plot the results
    plt.plot(x_axis, brute_force_times)
    plt.title("Brute force attack time vs number of bits")
    plt.xlabel("Number of bits")
    plt.ylabel("Attack time (s)")
    plt.xticks(x_axis)
    # save the plot
    plt.savefig("brute_force_attack_time.png")
    plt.close()


def factorization_analysis():
    """Analyze the attack time of RSA algorithm by factoring n"""
    global rsa_victim, rsa_attacker, message

    attack_times = []
    x_axis = range(10, 64)

    # factorize n
    def factor(n):
        # initialize p and q
        p = 0
        q = 0
        # loop over all numbers from 1 to n
        for i in range(3, int((n + 1) ** (1 / 2)), 2):
            # if i is a factor of n
            if n % i == 0:
                p = i
                q = n // i
                break
        if p == 0 or q == 0:
            p = 2
            q = n // 2
        return p, q

    # loop over different number of bits from 1 to 28
    for i in x_axis:
        # generate keys
        rsa_victim.bits = i
        n, e = rsa_victim.generate_keys()
        # attack by factorizing n
        start = time.time_ns()
        factor(n)
        end = time.time_ns()
        attack_times.append((end - start) / 1e9)

    # plot attack with matplotlib
    plt.plot(x_axis, attack_times)
    plt.title("Attack time vs number of bits")
    plt.xlabel("Number of bits")
    plt.ylabel("Attack time (s)")
    # save the plot
    plt.savefig("attack_time.png")


def main():
    """Main function"""
    encryption_decryption_analysis()
    # brute_force_analysis()
    factorization_analysis()


if __name__ == "__main__":
    main()
