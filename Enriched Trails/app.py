import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel , QMainWindow, QLineEdit , QPushButton , QInputDialog , QComboBox
from PyQt5 import QtCore 
from PyQt5 import QtGui
import sys
from main import *
from html import *
import webbrowser
import os

# =====================================
#   Technologies du web sémantique
#          -- Projet 1 --
#   Author : Sajaendra , Deniz
# =====================================

# FUNCTION

def search():

    # Reading parameters
    file_name =  input_1.currentText()

    try :
        distance = int(input_2.currentText())
    except ValueError : 
        print("Should be Integer")
        return

    if (file_name == "") :
        print(" Empty File Name ")
        return  
    
    
    print("Paramters are good ... , Running the search function ...")
    
    Info = GPS_INFO(file_name,distance)
    
    f = open('index.html','w')
 
    urlimg = "./images\/"+ str(file_name[:-4]) +".png)"
    message = define_html(urlimg,Info)
 
    f.write(message)
    f.close()
    
    filename = 'file:///'+os.getcwd()+'/' + 'index.html'
    
    webbrowser.open_new_tab(filename)


# Application : UNIGE_MAP
app = QApplication([])

# Window __init__
win = QMainWindow()
win.setWindowIcon(QtGui.QIcon('icon.ico'))
win.setGeometry( 500,200,500,200 )
win.setWindowTitle( "---  UNIGE_MAP  ---" )

# Labels 
label = QLabel(win)
label.setText("GPX : ")
label.move(50,50)

label = QLabel(win)
label.setText("Distance (m) : ")
label.move(50,100)

# Input  
#input_1 = QLineEdit(win)
#input_1.setPlaceholderText("   ___.gpx")

input_1 = QComboBox(win)
input_1.addItems(["","4sDDFdd4cjA.gpx","btSeByOExEc.gpx","kmrcRbHcMpg.gpx","PO21QxqG2co.gpx","pRAjjKqHwzQ.gpx","rx1-4gf5lts.gpx","tIRn_qJSB5s.gpx","UAQjXL9WRKY.gpx"])
input_1.move(150 ,50 )

input_2 = QComboBox(win)
input_2.addItems(["","100","500","1000","2000"])
input_2.move(150 ,100 )

# Buttons 



run_button = QPushButton("Search",win)
run_button.move( 300,50 )

quit_button = QPushButton("Quit",win)
quit_button.move( 300,90 )


# Button Handlder

run_button.clicked.connect(search)
quit_button.clicked.connect(QApplication.instance().quit)


win.show()
app.exec_()




