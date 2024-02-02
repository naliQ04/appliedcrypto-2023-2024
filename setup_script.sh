#!/bin/bash

# Maak een Python virtual environment (venv) aan
python3 -m venv myvenv

# Activeer de venv
source myvenv/bin/activate

# Installeer vereiste pakketten
pip install -r requirements.txt

# Voer OpenSSL-opdracht uit om een zelfondertekend servercertificaat te genereren

# Definieer de variabelen voor certificaatinformatie
COUNTRY="NL"
STATE="North-Holland"
CITY="Amsterdam"
ORGANIZATION="YourClientOrganization"
COMMON_NAME="YourClientCommonName"
EMAIL="client@example.com"

# Voer OpenSSL-opdracht uit om een zelfondertekend clientcertificaat te genereren met EC
openssl req -x509 -nodes -days 365 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
    -keyout clientcert.key -out clientcert.crt \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/CN=$COMMON_NAME/emailAddress=$EMAIL"

# Deactiveer de venv
deactivate

echo "Setup voltooid. Gebruik 'source myvenv/bin/activate' om de venv te activeren."
echo "----."
echo "start nu eerst de server.py in de eerste terminal."
echo "----."
echo "start daarna pas de client.py in een tweede terminal"
