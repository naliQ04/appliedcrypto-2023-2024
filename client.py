# Copyright (c) 2024 naliQ04
# Applied Cryptography 2023/2024

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


# Globale variabele voor de private key
global_private_key = None

# Functie voor het uitvoeren van het TLS-handshake-protocol
def tls_handshake(client_socket):
    global global_private_key

    # Stuur ClientHello naar de server
    client_socket.send(b"ClientHello")
    print("Sent: ClientHello")

    # Wacht op ServerHello
    response = client_socket.recv(1024)
    if response == b"ServerHello":
        print("Received: ServerHello")

        # Stuur ServerKeyExchange naar de server
        client_socket.send(b"ServerKeyExchange")
        print("Sent: ServerKeyExchange")

        # Ontvang het servercertificaat 
        cert_bytes = client_socket.recv(2048)

        # Gebruik de globale private_key als deze al is gegenereerd
        if global_private_key is None:
            global_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

        # Laad het servercertificaat vanuit een bestand
        with open('servercert.crt', 'rb') as f:
            cert_data = f.read()

        # Vergelijk het ontvangen certificaat met het lokale certificaat
        if cert_bytes == cert_data:
            print("Received server certificate")

            # Stuur ClientKeyExchange naar de server
            client_socket.send(b"ClientKeyExchange")
            print("Sent: ClientKeyExchange")

            # Ontvang Finished van de server
            response = client_socket.recv(1024)
            if response == b"Finished":
                print("Received: Finished")
                print("TLS handshake completed successfully")

            else:
                print("Finished failed")
                
        else:
            print("Server certificate verification failed")
            
# Functie voor het uitvoeren van de Diffie-Hellman key exchange
def perform_diffie_hellman_key_exchange(client_socket):

    global global_private_key

    # Controleer of er een private key beschikbaar is
    if global_private_key is None:
        print("No private key")
        pass

    # Genereer de public key van de client
    public_key = global_private_key.public_key()

    # Stuur de public key naar de server
    client_socket.send(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    # Ontvang de public key van de server
    server_public_key_data = client_socket.recv(1024)
    server_public_key = serialization.load_pem_public_key(server_public_key_data, default_backend())

    # Bereken de shared key
    shared_key = global_private_key.exchange(ec.ECDH(), server_public_key)
    return shared_key

# Functie voor het opzetten van de verbinding
def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    return client_socket

# Functie voor het versturen van een versleuteld bericht
def send_message(client_socket, message, shared_key, iv):
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
    client_socket.send(ciphertext)

# Functie voor het ontvangen van een versleuteld bericht
def receive_message(client_socket, shared_key, iv):
    ciphertext = client_socket.recv(1024)
    
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
def close_connection(client_socket, shared_key, iv):
    del shared_key
    del iv
    client_socket.close()

# Mainprogramma
def main():
    connection = connect()

    # Voer het TLS-handshake-protocol uit
    tls_handshake(connection)

    # Voer de Diffie-Hellman key exchange uit
    shared_key = perform_diffie_hellman_key_exchange(connection)
    #print("Shared Key:", shared_key.hex())

    # Ontvang de willekeurige IV van de server
    iv = connection.recv(16)

    # Blijf berichten uitwisselen totdat 'exit' wordt ingevoerd
    while True:
        received_message = receive_message(connection, shared_key, iv)
        print("Server:", received_message)

        if received_message.lower() == 'exit':
            break

        message_to_send = input("Client: ")
        send_message(connection, message_to_send, shared_key, iv)

        if message_to_send.lower() == 'exit':
            break

    # Sluit de verbinding en vernietig de sleutel en IV
    close_connection(connection, shared_key, iv)
    print("key and iv destroyed")

if __name__ == "__main__":
    main()
