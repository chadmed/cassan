import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QComboBox, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import base64
import requests

TIKTOK_API_BASE="https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/"

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Cassan'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 180
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tblabel = QLabel("Enter text to be spoken (max. 300 characters)", self)
        self.tblabel.move(20,20)
        self.tblabel.resize(280,25)

        # Type input
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50)
        self.textbox.resize(280,25)

        self.tblabel = QLabel("Select voice", self)
        self.tblabel.move(20,80)
        self.tblabel.resize(200,25)

        # Select voice
        self.voices = QComboBox(self)
        self.voices.addItem("Female")
        self.voices.addItem("British Male 01")
        self.voices.addItem("British Male 02")
        self.voices.addItem("Male 01")
        self.voices.addItem("Male 02")
        self.voices.move(100,80)
        self.voices.resize(120, 25)

        # Create a button in the window
        self.button = QPushButton('Generate audio', self)
        self.button.move(20,115)
        self.button.resize(110,30)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.voice_input = self.textbox.text()
        #self.voice_input = self.voice_input.replace(" ","%20")
        if len(self.voice_input) > 300:
            self.errdlg = QMessageBox(self)
            self.errdlg.setWindowTitle("Error")
            self.errdlg.setText("Text cannot be longer than 300 characters")
            self.errdlg.exec()
        else:
            self.api_req = {'text_speaker': 'en_us_001',
                    'req_text': self.voice_input}

            if self.voices.currentIndex == 0:
                pass
            elif self.voices.currentIndex == 1:
                self.api_req['text_speaker'] == "en_us_006"
            elif self.voices.currentIndex == 2:
                self.api_req['text_speaker'] == "en_us_010"
            elif self.voices.currentIndex == 3:
                self.api_req['text_speaker'] == "en_us_007"
            elif self.voices.currentIndex == 4:
                self.api_req['text_speaker'] == "en_us_009"
            self.ret = requests.post(TIKTOK_API_BASE, data=self.api_req)
            self.response = self.ret.json()
            with open('output.mp3', 'wb') as fd:
                try:
                    fd.write(base64.urlsafe_b64decode(self.response['data']['v_str']))
                    self.succdlg = QMessageBox(self)
                    self.succdlg.setWindowTitle("Success")
                    self.succdlg.setText("TTS saved to output.mp3")
                    self.succdlg.exec()
                except:
                    self.errdlg = QMessageBox(self)
                    self.errdlg.setWindowTitle("Error")
                    self.errdlg.setText("Could not create output.")
                    self.errdlg.exec()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
