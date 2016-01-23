import GetCoast
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *
from PyQt4.QtCore import QVariant
import sys
import re
import ExcelMake
from bs4 import BeautifulSoup
import time



app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui= GetCoast.Ui_Form()
ui.setupUi(Form)
Form.show()

ui.btn_login()


# ui.btn_ExtractExcel()

# ui.btn_ExtractExcel()

time.sleep(10)

print(ui.getConnectState())

sys.exit(app.exec_())


# codelist = ui.GetCodeListByMarket(10)

# print(codelist)