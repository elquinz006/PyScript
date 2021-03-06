import sys
import os
import ntpath
import configparser
from parseSA import mergeSA
import utils

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSlot

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
# InputList = []
# SnapList = []
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# form_class = uic.loadUiType("main.ui")[0]
main_ui = uic.loadUiType(BASE_DIR+r'\main.ui')[0]

#화면을 띄우는데 사용되는 Class 선언
# class WindowClass(QMainWindow, main_ui) :
class WindowClass(QMainWindow) :
    def __init__(self) -> None :
        super().__init__()
        # self.setupUi(self)
        uic.loadUi('main.ui', self)

        self.connections()

    def update_buttons_status(self):
        self.mBtnUp.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnDown.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == (self.mOuput.count() -1))
        self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

    @pyqtSlot()
    def connections(self):
        # Status bar

        self.actionSave_Config.triggered.connect(self.SaveConf)
        self.actionLoad_Config.triggered.connect(self.LoadConf)
        self.actionExit.triggered.connect(app.quit)

        # Btn
        self.btn_SelectFile.clicked.connect(self.getfiles)
        ext = 'cd'
        self.btn_SelectInput.clicked.connect(lambda: self.showList(ext))

        # Edit
        self.actionMerge_Summary_files.triggered.connect(self.MergeSA)

    @pyqtSlot()
    def getfiles(self):
        global Exec
        fileName = QFileDialog.getOpenFileName(
            self, 'Select TASS exec', filter="exe (*.exe)")[0]
        Exec = ntpath.basename(fileName)
        Exec = os.path.splitext(Exec)[0]
        self.label_Exec.setText(Exec)
        config.set('EXE','TASSexe',Exec)

    @pyqtSlot()
    def showList(self, ext):
        res = []
        ifld = QFileDialog.getExistingDirectory(self, 'Select Directory')
        # ext = 'cd'
        if ext=='cd':
            self.InputList = utils.getfilist(ifld, ext)
            for icd in self.InputList:
                self.mInput.addItem(icd)
        elif ext=='snp':
            self.SnapList = utils.getfilist(ifld, ext)

    @pyqtSlot()
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

    @pyqtSlot()
    def LoadConf(self):
        name = QFileDialog.getOpenFileName(
            self, 'Load configuration file', filter="ini (*.ini)")[0]

    @pyqtSlot()
    def MergeSA(self):
        SAfld = QFileDialog.getExistingDirectory(self, 'Select Directory')
        SAfile = QFileDialog.getSaveFileName(self, 'Save Collection of SA_summary file')
        mergeSA(SAfld, SAfile[0])

    @pyqtSlot()
    def on_mButtonToSelected_clicked(self):
        while self.mInput.count() > 0:
            self.mOuput.addItem(self.mInput.takeItem(0))

    @pyqtSlot()
    def on_mBtnMoveToAvailable_clicked(self):
        item = self.mInput.currentRow()
        print(item)
        self.mOuput.addItem(self.mInput.takeItem(self.mInput.currentRow()))

    @pyqtSlot()
    def on_mBtnMoveToSelected_clicked(self):
        self.mInput.addItem(self.mOuput.takeItem(self.mOuput.currentRow()))

    @pyqtSlot()
    def on_mButtonToAvailable_clicked(self):
        while self.mOuput.count() > 0:
            self.mInput.addItem(self.mOuput.takeItem(0))

    @pyqtSlot()
    def on_mBtnUp_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row - 1, currentItem)
        self.mOuput.setCurrentRow(row - 1)

    @pyqtSlot()
    def on_mBtnDown_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row + 1, currentItem)
        self.mOuput.setCurrentRow(row + 1)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    # raise SystemExit(app.exec_())
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
