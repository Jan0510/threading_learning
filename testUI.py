# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(842, 660)
        self.Log = QtWidgets.QPlainTextEdit(Form)
        self.Log.setGeometry(QtCore.QRect(420, 180, 371, 411))
        self.Log.setReadOnly(True)
        self.Log.setPlainText("")
        self.Log.setObjectName("Log")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 170, 381, 141))
        self.groupBox.setObjectName("groupBox")
        self.bnt_refreshPrintersList = QtWidgets.QPushButton(self.groupBox)
        self.bnt_refreshPrintersList.setGeometry(QtCore.QRect(280, 40, 75, 23))
        self.bnt_refreshPrintersList.setObjectName("bnt_refreshPrintersList")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 54, 12))
        self.label_2.setObjectName("label_2")
        self.FormatFileList = QtWidgets.QComboBox(self.groupBox)
        self.FormatFileList.setGeometry(QtCore.QRect(10, 100, 251, 22))
        self.FormatFileList.setObjectName("FormatFileList")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 54, 12))
        self.label.setObjectName("label")
        self.bnt_tryPrint = QtWidgets.QPushButton(self.groupBox)
        self.bnt_tryPrint.setGeometry(QtCore.QRect(280, 100, 75, 23))
        self.bnt_tryPrint.setObjectName("bnt_tryPrint")
        self.PrintersList = QtWidgets.QComboBox(self.groupBox)
        self.PrintersList.setGeometry(QtCore.QRect(10, 40, 251, 22))
        self.PrintersList.setObjectName("PrintersList")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 340, 381, 251))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lineEdit_sourceCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_sourceCount.setGeometry(QtCore.QRect(110, 30, 51, 20))
        self.lineEdit_sourceCount.setReadOnly(True)
        self.lineEdit_sourceCount.setObjectName("lineEdit_sourceCount")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 71, 16))
        self.label_3.setObjectName("label_3")
        self.bnt_Start = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_Start.setGeometry(QtCore.QRect(30, 160, 75, 23))
        self.bnt_Start.setObjectName("bnt_Start")
        self.bnt_Stop = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_Stop.setGeometry(QtCore.QRect(130, 160, 75, 23))
        self.bnt_Stop.setObjectName("bnt_Stop")
        self.lineEdit_PrintCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_PrintCount.setGeometry(QtCore.QRect(20, 220, 113, 20))
        self.lineEdit_PrintCount.setReadOnly(True)
        self.lineEdit_PrintCount.setObjectName("lineEdit_PrintCount")
        self.lineEdit_FailedCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_FailedCount.setGeometry(QtCore.QRect(170, 220, 113, 20))
        self.lineEdit_FailedCount.setReadOnly(True)
        self.lineEdit_FailedCount.setObjectName("lineEdit_FailedCount")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(30, 200, 54, 12))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(180, 200, 54, 12))
        self.label_6.setObjectName("label_6")
        self.comboBox_sourceName = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_sourceName.setGeometry(QtCore.QRect(110, 70, 241, 22))
        self.comboBox_sourceName.setObjectName("comboBox_sourceName")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(20, 110, 71, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_sourceContent = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_sourceContent.setGeometry(QtCore.QRect(110, 110, 181, 21))
        self.lineEdit_sourceContent.setReadOnly(True)
        self.lineEdit_sourceContent.setObjectName("lineEdit_sourceContent")
        self.bnt_sourceContentModify = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_sourceContentModify.setGeometry(QtCore.QRect(300, 110, 51, 21))
        self.bnt_sourceContentModify.setObjectName("bnt_sourceContentModify")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 60, 641, 91))
        self.groupBox_3.setObjectName("groupBox_3")
        self.serial_state_info = QtWidgets.QLabel(self.groupBox_3)
        self.serial_state_info.setGeometry(QtCore.QRect(11, 51, 101, 23))
        self.serial_state_info.setText("")
        self.serial_state_info.setObjectName("serial_state_info")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 22, 101, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.SerialList = QtWidgets.QComboBox(self.layoutWidget)
        self.SerialList.setObjectName("SerialList")
        self.horizontalLayout.addWidget(self.SerialList)
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget_2.setGeometry(QtCore.QRect(130, 20, 113, 22))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.BaudrateList = QtWidgets.QComboBox(self.layoutWidget_2)
        self.BaudrateList.setObjectName("BaudrateList")
        self.BaudrateList.addItem("")
        self.BaudrateList.addItem("")
        self.BaudrateList.addItem("")
        self.horizontalLayout_2.addWidget(self.BaudrateList)
        self.widget = QtWidgets.QWidget(self.groupBox_3)
        self.widget.setGeometry(QtCore.QRect(380, 20, 239, 54))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.bnt_scanSerial = QtWidgets.QPushButton(self.widget)
        self.bnt_scanSerial.setObjectName("bnt_scanSerial")
        self.gridLayout.addWidget(self.bnt_scanSerial, 0, 0, 1, 1)
        self.bnt_closeSerial = QtWidgets.QPushButton(self.widget)
        self.bnt_closeSerial.setObjectName("bnt_closeSerial")
        self.gridLayout.addWidget(self.bnt_closeSerial, 0, 1, 1, 1)
        self.bnt_openSerial = QtWidgets.QPushButton(self.widget)
        self.bnt_openSerial.setObjectName("bnt_openSerial")
        self.gridLayout.addWidget(self.bnt_openSerial, 0, 2, 1, 1)
        self.bnt_connect_2 = QtWidgets.QPushButton(self.widget)
        self.bnt_connect_2.setObjectName("bnt_connect_2")
        self.gridLayout.addWidget(self.bnt_connect_2, 1, 0, 1, 1)
        self.bnt_connect = QtWidgets.QPushButton(self.widget)
        self.bnt_connect.setObjectName("bnt_connect")
        self.gridLayout.addWidget(self.bnt_connect, 1, 1, 1, 1)
        self.bnt_break = QtWidgets.QPushButton(self.widget)
        self.bnt_break.setObjectName("bnt_break")
        self.gridLayout.addWidget(self.bnt_break, 1, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "GroupBox"))
        self.bnt_refreshPrintersList.setText(_translate("Form", "刷新列表"))
        self.label_2.setText(_translate("Form", "标签文件"))
        self.label.setText(_translate("Form", "打印机"))
        self.bnt_tryPrint.setText(_translate("Form", "试打印"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))
        self.label_3.setText(_translate("Form", "数据源个数"))
        self.bnt_Start.setText(_translate("Form", "运行"))
        self.bnt_Stop.setText(_translate("Form", "停止"))
        self.lineEdit_PrintCount.setText(_translate("Form", "0"))
        self.lineEdit_FailedCount.setText(_translate("Form", "0"))
        self.label_5.setText(_translate("Form", "打印次数"))
        self.label_6.setText(_translate("Form", "失败次数"))
        self.label_4.setText(_translate("Form", "数据源名称"))
        self.label_7.setText(_translate("Form", "数据源内容"))
        self.bnt_sourceContentModify.setText(_translate("Form", "修改"))
        self.groupBox_3.setTitle(_translate("Form", "GroupBox"))
        self.label_8.setText(_translate("Form", "串口"))
        self.label_9.setText(_translate("Form", "波特率"))
        self.BaudrateList.setItemText(0, _translate("Form", "115200"))
        self.BaudrateList.setItemText(1, _translate("Form", "9600"))
        self.BaudrateList.setItemText(2, _translate("Form", "38400"))
        self.bnt_scanSerial.setText(_translate("Form", "扫描串口"))
        self.bnt_closeSerial.setText(_translate("Form", "关闭串口"))
        self.bnt_openSerial.setText(_translate("Form", "打开串口"))
        self.bnt_connect_2.setText(_translate("Form", "自动连接"))
        self.bnt_connect.setText(_translate("Form", "连接设备"))
        self.bnt_break.setText(_translate("Form", "断开连接"))
