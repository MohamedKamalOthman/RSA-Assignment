# creating chatting server client using socket programming
import socket
from struct import pack, unpack
import RSA
import pickle

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# generate RSA keys
rsa = RSA.RSA()
keys = rsa.generate_keys()
try:
    # create socket object if it was not created then this instance is a server
    sock.bind(("localhost", 4321))
    sock.listen()
    client, address = sock.accept()
    # the server sends the public key to the client
    # the server receives the public key from the client
    client.send(pickle.dumps(keys[1]))  # the e value
    msg = client.recv(1024)
    e = pickle.loads(msg)
    client.send(pickle.dumps(keys[0]))  # the n value
    msg = client.recv(1024)
    n = pickle.loads(msg)

    # set the public key of the other instance
    rsa.set_public_key(n, e)
    print("Public keys:", (n, e))

    while 1:

        msg = input("Enter message: ")
        msg = rsa.encode(msg)
        msg = pickle.dumps(msg)
        client.send(msg)

        msg = client.recv(1024)
        msg = pickle.loads(msg)
        # decode the message
        msg = rsa.decode(msg)
        print(msg)


except:
    # port was open so this instance is a client
    sock.connect(("localhost", 4321))
    client = sock
    # the client receives the public key from the server
    # the client sends the public key to the server

    msg = client.recv(1024)
    e = pickle.loads(msg)
    client.send(pickle.dumps(keys[1]))  # the e value

    msg = client.recv(1024)
    n = pickle.loads(msg)
    client.send((pickle.dumps(keys[0])))  # the n value

    # set the public key of the other instance
    rsa.set_public_key(n, e)

    # public keys
    print("Public keys:", (n, e))

    while 1:

        msg = client.recv(1024)
        msg = pickle.loads(msg)
        # decode the message
        msg = rsa.decode(msg)
        print(msg)

        msg = input("Enter message: ")
        msg = rsa.encode(msg)
        msg = pickle.dumps(msg)
        client.send(msg)

# close the socket
sock.close()
