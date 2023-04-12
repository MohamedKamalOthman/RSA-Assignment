# creating chatting server client using socket programming
import RSA
import socket
import pickle
import threading
import signal
import sys

sock = None


def signal_handler(sig, frame):
    """Handle the SIGINT signal"""
    global sock
    # close the socket
    if sock is not None:
        sock.close()
        sock = None
    # exit the program
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def exchange_keys(sock, rsa):
    """Exchange the public keys between the server/client"""
    # generate keys
    keys = rsa.generate_keys()
    # the server/client sends the public key to the client
    # the server/client receives the public key from the client
    sock.send(pickle.dumps(keys[1]))  # the e value
    msg = sock.recv(2048)
    e = pickle.loads(msg)
    sock.send(pickle.dumps(keys[0]))  # the n value
    msg = sock.recv(2048)
    n = pickle.loads(msg)

    # set the public key of the other instance
    rsa.set_public_key(n, e)
    print("Received Public key:", (n, e))


def sock_connect(sock, port=4321):
    """Connect to the server/client"""
    # create socket object if it was not created then this instance is a server
    try:
        sock.bind(("localhost", port))
        sock.listen()
        client, _ = sock.accept()
    except:
        # port was open so this instance is a client
        sock.connect(("localhost", port))
        client = sock

    return client


def send_message(sock, rsa):
    """Send the message to the server/client"""
    while True:
        # read the message
        msg = input()
        if msg is None or msg == "":
            continue
        # encode the message
        msg = rsa.encode(msg)
        msg = pickle.dumps(msg)
        sock.send(msg)


def recv_message(sock, rsa):
    """Receive the message from the server/client"""
    while True:
        msg = sock.recv(4096)
        msg = pickle.loads(msg)
        # decode the message
        msg = rsa.decode(msg)
        print(f"Received Message: {msg}")


def main():
    """Main function"""
    global sock
    # create socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server/client
    sock = sock_connect(sock)

    # generate RSA keys
    rsa = RSA.RSA()

    # exchange keys
    exchange_keys(sock, rsa)

    # creating threads
    # Send message thread
    t1 = threading.Thread(target=send_message, args=(sock, rsa), name="t1", daemon=True)
    # Receive message thread
    t2 = threading.Thread(target=recv_message, args=(sock, rsa), name="t2", daemon=True)

    # starting threads
    t1.start()
    t2.start()

    # wait until all threads finish
    t1.join()
    t2.join()

    # close the socket
    if sock is not None:
        sock.close()
        sock = None


if __name__ == "__main__":
    main()
