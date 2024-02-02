# Copyright (c) 2024 naliQ04
# Applied Cryptography 2023/2024
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import os


# Globale variabele voor de private key
global_private_key = None

# Functie voor het uitvoeren van het TLS-handshake-protocol
def tls_handshake(conn):
    global global_private_key

    # Wacht op de ClientHello
    response = conn.recv(1024)


    if response == b"ClientHello":
        print("Received: ClientHello")

        # Stuur ServerHello naar de client
        conn.send(b"ServerHello")
        print("Sent: ServerHello")

        # Wacht op ServerKeyExchange
        response = conn.recv(1024)
        if response == b"ServerKeyExchange":
            print("Received: ServerKeyExchange")

            # Gebruik de globale private_key als deze al is gegenereerd
            if global_private_key is None:
                global_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
                
            # Laad het servercertificaat en stuur het naar de client
            with open('servercert.crt', 'rb') as f:
                cert_data = f.read()
                
            conn.send(cert_data)
            print("Sent server certificate")

            # Wacht op ClientKeyExchange
            response = conn.recv(1024)
            if response == b"ClientKeyExchange":
                print("Received: ClientKeyExchange")
                conn.send(b"Finished")
                print("Sent: Finished")
                print("TLS handshake completed successfully")

            else:
                print("ClientKeyExchange failed")

        else:
            print("ServerKeyExchange failed")

    else:
        print("ClientHello failed")

# Functie voor het uitvoeren van de Diffie-Hellman key exchange
def perform_diffie_hellman_key_exchange(conn):
    global global_private_key

    # Controleer of er een private key beschikbaar is
    if global_private_key is None:
        print("No private key")
        pass

    # Genereer de public key van de server
    public_key = global_private_key.public_key()

    # Stuur de public key naar de client
    conn.send(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    # Ontvang de public key van de client
    client_public_key_data = conn.recv(1024)
    client_public_key = serialization.load_pem_public_key(client_public_key_data, default_backend())

    # Bereken de shared key
    shared_key = global_private_key.exchange(ec.ECDH(), client_public_key)
    return shared_key

# Functie voor het opzetten van de verbinding
def connect():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(1)
    print("Server is listening for connections...")
    conn, addr = server_socket.accept()
    print("Connected to:", addr)
    return conn

# Functie voor het versturen van een versleuteld bericht
def send_message(conn, message, shared_key, iv):
    # Voeg padding toe aan het bericht
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode())
    padded_message += padder.finalize()

    # Versleutel het bericht met AES in CBC-modus
    cipher = Cipher(
        algorithms.AES(shared_key),
        modes.CBC(iv)
    )
    encryptor = cipher.encryptor()

    # Stuur het versleutelde bericht naar de client
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    conn.send(ciphertext)

# Functie voor het ontvangen van een versleuteld bericht
def receive_message(conn, shared_key, iv):
    # Ontvang het versleutelde bericht van de client
    ciphertext = conn.recv(1024)

    # Decrypteer het bericht met AES in CBC-modus
    cipher = Cipher(
        algorithms.AES(shared_key),
        modes.CBC(iv)
    )
    decryptor = cipher.decryptor()

    # Verwijder de padding van het gedecrypteerde bericht
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_message = unpadder.update(padded_message)
    unpadded_message += unpadder.finalize()

    return unpadded_message.decode()

# Functie voor het sluiten van de verbinding
def close_connection(conn, shared_key, iv):
    del shared_key
    del iv
    conn.close()

# Functie voor het genereren van een willekeurige IV
def generate_random_iv():
    return os.urandom(16)

# Mainprogramma
def main():
    # Maak verbinding met de client
    connection = connect()

    # Voer het TLS-handshake-protocol uit
    tls_handshake(connection)
    
    # Voer de Diffie-Hellman key exchange uit
    shared_key = perform_diffie_hellman_key_exchange(connection)
    #print("Shared Key:", shared_key.hex())

    # Genereer een willekeurige IV
    iv = generate_random_iv()

    # Stuur de IV naar de client
    connection.send(iv)

    # Blijf berichten uitwisselen totdat 'exit' wordt ingevoerd
    while True:
        message_to_send = input("Server: ")
        send_message(connection, message_to_send, shared_key, iv)

        if message_to_send.lower() == 'exit':
            break

        received_message = receive_message(connection, shared_key, iv)
        print("Client:", received_message)

        if received_message.lower() == 'exit':
            break

    # Sluit de verbinding en vernietig de sleutel en IV
    close_connection(connection, shared_key, iv)
    print("key and iv destroyed")


if __name__ == "__main__":
    main()
