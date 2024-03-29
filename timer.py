import sys
import os
from time import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

TIME_LIMIT = 100

class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count +=1
            time.sleep(1)
            self.countChanged.emit(count)

class Example(QWidget):

    def __init__(self, ):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        # self.lcd = QtGui.QLCDNumber(self)
        # self.lcd.display(strftime("%H" + ":" + "%M"))
        #

        QToolTip.setFont(QFont('SansSerif', 10))

        self.cancel = QPushButton('Cancel', self)
        self.cancel.clicked.connect(self.cancelTimer)
        self.cancel.resize(250, 50)
        self.cancel.move(25, 300)
        self.cancel.setToolTip('This button cancels the logout.')

        self.qbtn = QPushButton('Quit', self)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(250, 50)
        self.qbtn.move(25, 200)
        self.qbtn.setToolTip("Exit from the program")

        self.pb_num1 = QPushButton('Set Timer', self)
        self.pb_num1.clicked.connect(self.show_dialog_num1)
        self.pb_num1.resize(250, 50)
        self.pb_num1.move(25, 400)

        self.progress = QProgressBar(self)
        self.progress.resize(285, 50)
        self.progress.move(25, 0)
        self.progress.setMaximum(100)

        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        self.resize(300, 600)
        self.center()
        self.setWindowTitle('Timer for Windows 10')
        self.show()

    def Time(self):
        self.lcd.display(strftime("%H" + ":" + "%M"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_dialog_num1(self):
        value, ok = QInputDialog.getInt(self, 'Set timer', 'Enter the number of minutes')
        if not ok:
          return
        elif ok:
          value = int(value) * 60
          status = os.system("shutdown -s -f -t " + str(value))
          self.calc = External()
          self.calc.countChanged.connect(self.onCountChanged)
          self.calc.start()


    def onCountChanged(self, value):
        self.progress.setValue(value)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def cancelTimer(self):
        status = os.system("shutdown -a")
        if status == 0:
            print("good")
        else:
            print(status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())