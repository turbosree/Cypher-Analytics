# A security mechanism model for key ceremony in a distributed embedded control system.
# TODO: Secure storage and trasport of secret cryptographic materials
#
# Author: sreejith.naarakathil@gmail.com

import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from secretsharing import PlaintextToHexSecretSharer
import time

# Email setup (replace with your own details)
SMTP_SERVER = 'smtp.gmail.com'
IMAP_SERVER = 'imap.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-password'
RECEIVER_EMAILS = ['receiver1@gmail.com', 'receiver2@gmail.com', 'receiver3@gmail.com']

def send_email(sender, password, receiver, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, text)
    server.quit()

def receive_email(user, password, mailbox, search_criterion):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(user, password)
    mail.select(mailbox)

    result, data = mail.uid('search', None, search_criterion)
    if result == 'OK':
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(BODY[TEXT])')
        raw_email = data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        return email_message.get_payload()

# 1. Generate transport key and production key
transport_key = Fernet.generate_key()
production_key = Fernet.generate_key()
shares = PlaintextToHexSecretSharer.split_secret(transport_key.decode(), 2, 3)

# 2. Send each share via email
for i, receiver in enumerate(RECEIVER_EMAILS):
    send_email(SENDER_EMAIL, SENDER_PASSWORD, receiver, 'Transport Key Fragment', shares[i])

# Allow time for emails to be sent
time.sleep(5)

# 3. Simulate receiving the shares from emails and reconstruct the transport key
received_shares = []
for receiver in RECEIVER_EMAILS:
    share = receive_email(SENDER_EMAIL, SENDER_PASSWORD, 'inbox', '(FROM "' + receiver + '")')
    received_shares.append(share)

reconstructed_transport_key = PlaintextToHexSecretSharer.recombine_secret(received_shares)

# 4. Verify transport key using Key Check Value (KCV)
digest = hashes.Hash(hashes.SHA256())
digest.update(transport_key)
original_kcv = digest.finalize()

digest = hashes.Hash(hashes.SHA256())
digest.update(reconstructed_transport_key.encode())
reconstructed_kcv = digest.finalize()

if original_kcv == reconstructed_kcv:
    print("KCV Verification Successful")
else:
    print("KCV Verification Failed")

# 5. Encrypt production key with transport key and send it
cipher_suite = Fernet(reconstructed_transport_key.encode())
encrypted_production_key = cipher_suite.encrypt(production_key)

send_email(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAILS[0], 'Encrypted Production Key', encrypted_production_key.decode())

# 6. Receive encrypted production key
received_encrypted_production_key = receive_email(SENDER_EMAIL, SENDER_PASSWORD, 'inbox', '(FROM "' + RECEIVER_EMAILS[0] + '")')

# 7. Return key ceremony successful email
send_email(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAILS[0], 'Key Ceremony Successful', 'The key ceremony was successful')

# 8. Verify return email and destroy all local copies of keys
confirmation = receive_email(SENDER_EMAIL, SENDER_PASSWORD, 'inbox', '(FROM "' + RECEIVER_EMAILS[0] + '")')
if confirmation.strip() == 'The key ceremony was successful':
    print("Key Ceremony was successful. Destroying all local copies of keys.")
    transport_key = None
    production_key = None
    shares = None
    received_shares = None
    reconstructed_transport_key = None
    encrypted_production_key = None
    received_encrypted_production_key = None
