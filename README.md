# Veilige Chat Applicatie met TLS en Diffie-Hellman Key Exchange

Dit is een eenvoudig voorbeeld van een beveiligde communicatie tussen een server en een client met behulp van het TLS-handshake-protocol en de Diffie-Hellman key exchange. De communicatie is versleuteld met AES in CBC-modus.

## Installatie

### automatisch

1. **Een automatische installatie uitvoeren door het shellscript te activeren:**
    ```bash
    ./setup_script.sh
    ```

### handmatig

1. **Clone de repository naar je lokale machine:**

    ```bash
    git clone https://github.com/naliQ4/appliedcrypto-2023-2024.git
    ```

2. **Maak een Python virtual environment (venv) aan en activeer deze:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Installeer de vereiste pakketten:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Genereer een zelfondertekend servercertificaat met OpenSSL:**

    ```bash
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout clientcert.key -out clientcert.crt
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
