import sys
import os
import ntpath
import configparser
# from parseSA import mergeSA
# from util import *
import utils

# from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic, QtWidgets


def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


config = configparser.ConfigParser()
config.add_section('EXE')
config.add_section('INPUT')
config.add_section('SNAP')


# Global
Exec = ''
Inputfld = ''
Snapfld = ''
InputList = []
SnapList = []
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# form_class = uic.loadUiType("main.ui")[0]
main_ui = uic.loadUiType(BASE_DIR+r'\main.ui')[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # self.setupUI(self)
        # self.setupUI()

    def setupUI(self):
        # self.actionSave_Config = QtWidgets.QAction(self)
        # self.actionLoad_Config = QtWidgets.QAction(self)
        # Status bar
        # Save conf
        self.actionSave_Config.triggered.connect(self.SaveConf)
        # Load conf
        self.actionLoad_Config.triggered.connect(self.LoadConf)
        # Exit
        # self.actionExit.triggered.connect(qApp.quit)
        self.actionExit.triggered.connect(app.quit)

        # Btn
        self.btn_SelectFile.clicked.connect(self.getfiles)
        ext = 'cd'
        self.btn_SelectInput.clicked.connect(lambda: self.showList(ext))

        # Edit
        self.actionMerge_Summary_files.triggered.connect(self.MergeSA)


    def getfiles(self):
    #   filePath = QFileDialog.getOpenFileName(self, filter="exe(*.exe)")
    #   fileName = filePath[0]
    #   print(fileName[0])
        global Exec
        fileName = QFileDialog.getOpenFileName(
            self, 'Select TASS exec', filter="exe (*.exe)")[0]
        Exec = ntpath.basename(fileName)
        Exec = os.path.splitext(Exec)[0]
        self.label_Exec.setText(Exec)
        config.set('EXE','TASSexe',Exec)


    def showList(self, ext):
        res = []
        ifld = QFileDialog.getExistingDirectory(self, 'Select Directory')
        # ext = 'cd'
        if ext=='cd':
            InputList = utils.getfilist(ifld, ext)
            # print(*InputList, sep = "\n")
            model = QStandardItemModel()
            for id in InputList:
                model.appendRow(QStandardItem(id))
            self.list_input.setModel(model)
        elif ext=='snp':
            SnapList = utils.getfilist(ifld, ext)
            # print('Under Construction')


    def SaveConf(self):
        name = QFileDialog.getSaveFileName(
            self, 'Save configuration file', filter="ini (*.ini)")[0]
        if len(Exec)>1:
            with open(name, 'w') as configfile:
                config.write(configfile)
        else:
            # QMessageBox.question(self.window, 'Warning', 'Select TASS exec first')
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Warning')
            msgBox.setText('Select TASS exec first!')
            msgBox.exec_()


    def LoadConf(self):
        name = QFileDialog.getOpenFileName(
            self, 'Load configuration file', filter="ini (*.ini)")[0]


    def MergeSA(self):
        SAfld = QFileDialog.getExistingDirectory(self, 'Select Directory')
        SAfile = QFileDialog.getSaveFileName(self, 'Save Collection of SA_summary file')
      #   print(SAfld)
        mergeSA(SAfld, SAfile[0])


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    myWindow.setupUI()
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

