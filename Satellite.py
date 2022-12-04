# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Satellite Tracking GUI developed using PyQt6"""

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from datetime import datetime, timedelta

WINDOW_SIZE = 600

class Satellite(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_UI()
    
    def create_UI(self):
        self.setWindowTitle("Satellite Tracker")
        self.setMinimumSize(WINDOW_SIZE, WINDOW_SIZE)
        self.setLocalTime()
        # self.setContactPeriod()
        self.show()
    
    def lineProperties(self, dir, width=2):
        obj = QFrame()
        if dir == "V":      obj.setFrameShape(QFrame.Shape.VLine)
        elif dir == "H":    obj.setFrameShape(QFrame.Shape.HLine)
        obj.setStyleSheet("background-color: gold; border:none")
        obj.setLineWidth(width)
        return obj
        
    def textProperties(self, obj):
        obj = QLabel(obj)
        obj.setFont(QFont("Times New Roman", 30))
        obj.setStyleSheet("color:aquamarine; border: none;")
        obj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return obj
    
    def setLocalTime(self): 
        timing = str(datetime.now().strftime("%H:%M"))
        initial = str((datetime.now() - timedelta(hours=3)).strftime("%H:%M"))
        final = str((datetime.now() + timedelta(hours=3)).strftime("%H:%M"))
        
        layout = QGridLayout()

        localheader = self.textProperties("Local Time")
        localtime = self.textProperties(timing)
        contacttime = self.textProperties("Contact Time")
        initialheader = self.textProperties("Initial")
        initialtime = self.textProperties(initial)
        finalheader = self.textProperties("Final")
        finaltime = self.textProperties(final)
        
        line0 = self.lineProperties("H")
        line1 = self.lineProperties("V")
        line2 = self.lineProperties("V")
        line3 = self.lineProperties("H")

        layout.addWidget(line0, 0, 0, 1, 5)
        layout.addWidget(localheader, 1, 0, 2, 1)   ## row 0, col 0, rowspan 2, colspan 1
        layout.addWidget(localtime, 3, 0)           ## row 2, col 0
        layout.addWidget(line1, 0, 1, 8, 1)         ## row 0, col 1, rowspan 10,colspan 1
        layout.addWidget(contacttime, 1, 2, 1, 3)   ## row 0, col 2, rowspan 1, colspan 3
        layout.addWidget(initialheader, 2, 2)       ## row 1, col 2
        layout.addWidget(initialtime, 3, 2)         ## row 2, col 2
        layout.addWidget(line2, 2, 3, 6, 1)         ## row 1, col 3, rowspan 9, colspan 1
        layout.addWidget(finalheader, 2, 4)         ## row 1, col 4
        layout.addWidget(finaltime, 3, 4)           ## row 2, col 4
        
        layout.addWidget(line3, 7, 0, 1, 5)         ## row 6, col 0, rowspan 1, colspan 5


        widget = QWidget()
        # widget.setStyleSheet("border: 1px solid white;")
        # widget.setFixedWidth(200)
        widget.setLayout(layout)
        self.setMenuWidget(widget)
    
    def setContactPeriod(self):
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setStyleSheet("border: 1px solid white;")
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Sate = Satellite()
    sys.exit(app.exec())