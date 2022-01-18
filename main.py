import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QAction
import re
from configparser import ConfigParser
import paho.mqtt.client as paho
from paho import mqtt
import datetime
import time
from bitarray import bitarray
import struct
from struct import *
import sqlite3
from PyQt5 import QtSql


#***************GLOBAL VARIABLES**********
aprevious = [0 for x in range(32)]
tabla = 0
greska = ["" for x in range(22)]
greska[0] = "Smetnje zatezanja trake"
greska[1] = "Preteze uze desno"
greska[2] = "Preteze uze lijevo"
greska[3] = "Bocno skretanje rep"
greska[4] = "Bocno skretanje pog. st."
greska[5] = "Preopt. Bimetal m1"
greska[6] = "Preopt. Bimetal m2"
greska[7] = "Preg. Os m1"
greska[8] = "Pregar. os m2"
greska[9] = "Grij.Rez.Red m1"
greska[10] = "Grij. Nam m1"
greska[11] = "Grij. lez. m2"
greska[12] = "Grij. Nam m2"
greska[13] = "sf6 gas m1"
greska[14] = "SF6 gas m2"
greska[15] = "Zapunj. kosa"
greska[16] = "Not pogon"
greska[17] = "Not kljuc"
greska[18] = "Proklizavanje"
greska[19] = "Krajnji vrata M1"
greska[20] = "Krajnji vrata M2"
greska[21] = "Greska kocnice sig"
#***************GLOBAL VARIABLES**********


conn = sqlite3.connect('baza.db')

c = conn.cursor()
def insertVaribleIntoTable(timestamp, greska, brGreske):
   
    global c
    global conn

    sqlite_insert_with_param = """INSERT INTO testtable(
                    timestamp, greska,
                    brGreske)
                    VALUES(?,?,?);"""

    data_tuple = (timestamp, greska, brGreske)
    c.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful

def on_message(client, userdata, msg):       
    if(msg.topic == "plc/tabla"):
        global tabla
        tabla = msg.payload

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("unterusername", "enterpasword")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("entercloud", 8883)


# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.loop_start()

file = 'config.ini'
config = ConfigParser()
config.read(file)

class Settings(QtWidgets.QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        loadUi("settings.ui", self)
        #self.connect(exit,QtCore.SIGNAL('triggered()'),QtCore.SLOT('close()'))
        self.pushButton.clicked.connect(self.editconfig)
        self.pushButton_2.clicked.connect(self.gotowelcome)
        
    def gotowelcome(self):
        welcome = Welcome()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()


    def editconfig(self):
        cloud = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
  
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)
        config.set('broker','cloud', cloud )
        config.set('broker','username', username )
        config.set('broker','password', password )

        with open(file, 'w') as configfile:
            config.write(configfile)
        #user = config['broker']
        #print(user['username'])
class Analiza(QtWidgets.QDialog):
    def __init__(self):
        super(Analiza, self).__init__()
        loadUi("analiza.ui", self)
        self.pushButton.clicked.connect(lambda: button_clicked(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: button_2_clicked(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: button_3_clicked(self.pushButton_3))
        self.comboBox.currentIndexChanged.connect(lambda: selectionchange(self.comboBox.currentIndex()))
        self.pushButton_4.clicked.connect(self.gotowelcome)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setStyleSheet("QTableView {alternate-background-color: #060109; background-color: #070e1e;} QHeaderView::section { background-color: #15202b; }")
        self.tableView_2.setAlternatingRowColors(True)
        self.tableView_2.setStyleSheet("QTableView {alternate-background-color: #060109; background-color: #070e1e;} QHeaderView::section { background-color: #15202b; }")       
        self.tableView_3.setAlternatingRowColors(True)
        self.tableView_3.setStyleSheet("QTableView {alternate-background-color: #060109; background-color: #070e1e;} QHeaderView::section { background-color: #15202b; }")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(backgroundprocess)
        self.timer.start(700)



        def loadDatabase():
        
            db_connect = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db_connect.setDatabaseName("baza.db")
            db_connect.open()
            model = QtSql.QSqlQueryModel()
            model.setQuery("SELECT * FROM testtable ;")
            self.tableView.setModel(model)
        loadDatabase()
        def button_2_clicked(pushButton):
            db_connect = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db_connect.setDatabaseName("baza.db")
            db_connect.open()
            model = QtSql.QSqlQueryModel()
            model.setQuery("SELECT * FROM testtable ;")
            self.tableView.setModel(model)
        def button_clicked(pushButton):
            db_connect = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db_connect.setDatabaseName("baza.db")
            db_connect.open()
            model = QtSql.QSqlQueryModel()
            model.setQuery("DELETE FROM testtable;")
            self.tableView.setModel(model)
        
        def selectionchange(currentIndex):
            greskica = str(currentIndex)
            db_connect = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db_connect.setDatabaseName("baza.db")
            db_connect.open()
            model = QtSql.QSqlQueryModel()
            kveri = "SELECT * FROM testtable WHERE brGreske = " + greskica
            model.setQuery(kveri)
            self.tableView_2.setModel(model)
        
        def button_3_clicked(pushButton):
            pocetak = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm")
            kraj = self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm")
            #pocetak = self.dateTimeEdit.dateTime()
            #kraj = self.dateTimeEdit_2.dateTime()
            pocetakstr = str(pocetak)
            krajstr = str(kraj)
            
            db_connect = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db_connect.setDatabaseName("baza.db")
            db_connect.open()
            
            #query.prepare("SELECT * FROM testtable WHERE timestamp BETWEEN ? AND ?;")
            sql = "SELECT * from testtable WHERE timestamp BETWEEN datetime('{}') AND datetime('{}')".format(pocetak, kraj)
            #query.bindValue(0, pocetak)
            #query.bindValue(1, kraj)
            query = QtSql.QSqlQuery(sql)
            query.exec_()


            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            self.tableView_3.setModel(model)

    def gotowelcome(self):
        self.timer.stop()
        welcome = Welcome()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()

       
    
class Tjedan(QtWidgets.QDialog):
    def __init__(self):
        super(Tjedan, self).__init__()

        loadUi("tjedan.ui", self)
        self.pushButton_2.clicked.connect(self.gotowelcome)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.pushButton.clicked.connect(self.gotoanalysis)

        def changelabelcolor():
            
            client.loop_start()
            client.subscribe("plc/tabla", qos=1)
            global a
            a = bitarray('0' * 32, endian='little')
            v=int(tabla)

            for k in range(32):
                bit = (v >> k) & 1
                a[k] = bit
                        
            if(a[0] == 0):
                self.label_43.setStyleSheet("background-color: red")
            else:
                self.label_43.setStyleSheet("background-color: green")
            if(a[1] == 0):
                self.label_44.setStyleSheet("background-color: red")
            else:
                self.label_44.setStyleSheet("background-color: green")
            if(a[2] == 0):
                self.label_45.setStyleSheet("background-color: red")
            else:
                self.label_45.setStyleSheet("background-color: green")
            if(a[3] == 0):
                self.label_46.setStyleSheet("background-color: red")
            else:
                self.label_46.setStyleSheet("background-color: green")
            if(a[4] == 0):
                self.label_47.setStyleSheet("background-color: red")
            else:
                self.label_47.setStyleSheet("background-color: green")
            if(a[5] == 0):
                self.label_48.setStyleSheet("background-color: red")
            else:
                self.label_48.setStyleSheet("background-color: green")
            if(a[6] == 0):
                self.label_49.setStyleSheet("background-color: red")
            else:
                self.label_49.setStyleSheet("background-color: green")
            if(a[7] == 0):
                self.label_410.setStyleSheet("background-color: red")
            else:
                self.label_410.setStyleSheet("background-color: green")
            if(a[8] == 0):
                self.label_411.setStyleSheet("background-color: red")
            else:
                self.label_411.setStyleSheet("background-color: green")
            if(a[9] == 0):
                self.label_412.setStyleSheet("background-color: red")
            else:
                self.label_412.setStyleSheet("background-color: green")
            if(a[10] == 0):
                self.label_413.setStyleSheet("background-color: red")
            else:
                self.label_413.setStyleSheet("background-color: green")
            if(a[11] == 0):
                self.label_414.setStyleSheet("background-color: red")
            else:
                self.label_414.setStyleSheet("background-color: green")
            if(a[12] == 0):
                self.label_415.setStyleSheet("background-color: red")
            else:
                self.label_415.setStyleSheet("background-color: green")
            if(a[13] == 0):
                self.label_416.setStyleSheet("background-color: red")
            else:
                self.label_416.setStyleSheet("background-color: green")
            if(a[14] == 0):
                self.label_417.setStyleSheet("background-color: red")
            else:
                self.label_417.setStyleSheet("background-color: green")
            if(a[15] == 0):
                self.label_418.setStyleSheet("background-color: red")
            else:
                self.label_418.setStyleSheet("background-color: green")
            if(a[16] == 0):
                self.label_419.setStyleSheet("background-color: red")
            else:
                self.label_419.setStyleSheet("background-color: green")
            if(a[17] == 0):
                self.label_420.setStyleSheet("background-color: red")
            else:
                self.label_420.setStyleSheet("background-color: green")
            if(a[18] == 0):
                self.label_421.setStyleSheet("background-color: red")
            else:
                self.label_421.setStyleSheet("background-color: green")
            if(a[19] == 0):
                self.label_422.setStyleSheet("background-color: red")
            else:
                self.label_422.setStyleSheet("background-color: green")
            if(a[20] == 0):
                self.label_423.setStyleSheet("background-color: red")
            else:
                self.label_423.setStyleSheet("background-color: green")
            if(a[21] == 0):
                self.label_424.setStyleSheet("background-color: red")
            else:
                self.label_424.setStyleSheet("background-color: green")

 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(changelabelcolor)
        self.timer.start(700) 


    def closeEvent(self, event):
        print("close")  
        
    def gotowelcome(self):
        self.timer.stop()
        welcome = Welcome()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()
    def gotoanalysis(self):
        self.timer.stop()
        welcome = Analiza()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()
        
    

class Welcome(QtWidgets.QMainWindow):
    def __init__(self):
        super(Welcome, self).__init__()
        loadUi("home.ui", self)
        self.pushButton_4.clicked.connect(self.gotomain)
        #self.pushButton.setStyleSheet("QPushButton::hover{background-color: light-green}; ")
        self.actioncon.triggered.connect(self.gotosettings)
        self.pushButton_3.clicked.connect(self.gototjedan)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(backgroundprocess)
        self.timer.start(700)

    def gotomain(self):
        self.timer.stop()
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()
    
    def gotosettings(self):
        self.timer.stop()

        settings = Settings()
        widget.addWidget(settings)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()
    
    def gototjedan(self):
        self.timer.stop()
        tjedan = Tjedan()
        widget.addWidget(tjedan)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.show()

class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.gotomain)
                    
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(backgroundprocess)
        self.timer.start(700)


    def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                         "QUIT",
                                         "Are you sure want to stop process?",
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def gotomain(self):
       # self.hide()
        self.timer.stop()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if(username == "goran123" and password == "boboneco"):
            welcome = Welcome()
            widget.addWidget(welcome)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.showMaximized()

        elif((username != "goran123" or password != "boboneco") and (username == "" and password != "")):
            self.label_5.setText("Username field can't be blank. ")

        elif((username != "goran123" or password != "boboneco") and (username != "" and password == "")):
            self.label_5.setText("Please enter Password. ")

        elif((username != "goran123" or password != "boboneco") and (username == "" and password == "")):
            self.label_5.setText("Please enter username and password. ")
            
        elif((username != "goran123" or password != "boboneco") and (username != "" and password != "")):
            self.label_5.setText("Wrong username or pasword")

def backgroundprocess():

    client.loop_start()
    client.subscribe("plc/tabla", qos=1)

    a = bitarray('0' * 32, endian='little')
    v=int(tabla)
    for k in range(32):
        bit = (v >> k) & 1
        a[k] = bit
    print(a[1])

    z = struct.unpack("<L", a)[0]
    vrijeme = datetime.datetime.now()
    #client.publish("plc/tabla", z, qos=1)
    global aprevious
    for it in range(22):
        if(a[it]==0 and a[it]!=aprevious[it]):
            global greska
            insertVaribleIntoTable(vrijeme, greska[it], it)


    for k in range(32):
        aprevious[k] = a[k] 


            










    




 


#main
app = QApplication(sys.argv)
welcome = Login()
#tjedan = Tjedan()
#tjedan.__init__()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.showMaximized()
#welcome.show()
sys.exit(app.exec_())