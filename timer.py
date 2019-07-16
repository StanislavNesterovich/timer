import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.cancel = QPushButton('Cancel Shut Down', self)
        self.cancel.clicked.connect(self.cancelTimer)
        self.cancel.resize(250, 50)
        self.cancel.move(25, 300)

        self.qbtn = QPushButton('Quit', self)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(250, 50)
        self.qbtn.move(25, 200)

        self.pb_num1 = QPushButton('Set Timer', self)
        self.pb_num1.clicked.connect(self.show_dialog_num1)
        self.pb_num1.resize(250, 50)
        self.pb_num1.move(25, 400)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)

        self.resize(300, 600)
        self.center()
        self.setWindowTitle('Timer for Windows 10')
        self.show()

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