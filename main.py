import sys

from PyQt5.QtWidgets import QApplication

from gui import GUI
import vulns_1_3
import vulns_4_6
import vulns_7_9
import vulns_10_12

app = QApplication(sys.argv)
gui = GUI()
sys.exit(app.exec_())
