# Veilige Chat Applicatie met TLS en Diffie-Hellman Key Exchange

Dit is een eenvoudig voorbeeld van een beveiligde communicatie tussen een server en een client met behulp van het TLS-handshake-protocol en de Diffie-Hellman key exchange. De communicatie is versleuteld met AES in CBC-modus.

## Installatie

1. **Clone de repository naar je lokale machine en open deze met Visual Studio Code:**

    ```bash
    git clone https://github.com/naliQ04/appliedcrypto-2023-2024.git
    ```

3. **zorg ervoor dat je in de directory /appliedcrypto-2023-2024 zin**

    ```bash
    cd appliedcrypto-2023-2024
    ```

4. **Open een command prompt in visual studio code**

5. **Maak een Python virtual environment (venv) aan en activeer deze:**

    venv aanmaken
    ```bash
    python -m venv venv
    ```

    venv activeren indien deze niet is geactiveerd
    ```bash
    .\.venv\Scripts\activate
    ```

6. **Installeer de vereiste pakketten:**

    ```bash
    pip3 install -r requirements.txt
    ```

7. **Genereer een zelfondertekend servercertificaat met OpenSSL en voer de velden na eigen keuze in:**

    ```bash
    openssl req -x509 -nodes -days 365 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout servercert.key -out servercert.crt
    ```

## Starten van de Server

1. **open de eerste terminal en voer de commando uit om de server programma te starten:**

    ```bash
    python server.py
    ```

## Starten van de Client

1. **open de tweede terminal en voer de commando uit om de client programma te starten:**

    ```bash
    python client.py
    ```

Volg de instructies in de terminal om berichten uit te wisselen met end-to-end versleuteling via TLS en Diffie-Hellman key exchange. Beëindig het programma door 'exit' in te voeren.

Vergeet niet om de Python virtual environment (venv) te deactiveren wanneer je klaar bent:

```bash
deactivate
```

## Modules van toepassing tot dit project

- cryptography
- socket
- openssl
