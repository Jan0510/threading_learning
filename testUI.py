# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from Mycombobox import MyComboBox


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(800, 600))
        Form.setMaximumSize(QtCore.QSize(800, 600))
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setAutoFillBackground(False)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 411, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 381, 221))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 220, 381, 301))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lineEdit_sourceCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_sourceCount.setGeometry(QtCore.QRect(110, 80, 51, 20))
        self.lineEdit_sourceCount.setReadOnly(True)
        self.lineEdit_sourceCount.setObjectName("lineEdit_sourceCount")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 71, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_PrintCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_PrintCount.setGeometry(QtCore.QRect(20, 270, 113, 20))
        self.lineEdit_PrintCount.setReadOnly(True)
        self.lineEdit_PrintCount.setObjectName("lineEdit_PrintCount")
        self.lineEdit_FailedCount = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_FailedCount.setGeometry(QtCore.QRect(170, 270, 113, 20))
        self.lineEdit_FailedCount.setReadOnly(True)
        self.lineEdit_FailedCount.setObjectName("lineEdit_FailedCount")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(30, 250, 54, 12))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(180, 250, 54, 12))
        self.label_6.setObjectName("label_6")
        self.SubstringList = QtWidgets.QComboBox(self.groupBox_2)
        self.SubstringList.setGeometry(QtCore.QRect(110, 120, 241, 22))
        self.SubstringList.setObjectName("SubstringList")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 71, 16))
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(20, 160, 71, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_sourceContent = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_sourceContent.setGeometry(QtCore.QRect(110, 160, 181, 21))
        self.lineEdit_sourceContent.setReadOnly(False)
        self.lineEdit_sourceContent.setObjectName("lineEdit_sourceContent")
        self.bnt_tryModifySourceContent = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_tryModifySourceContent.setGeometry(QtCore.QRect(300, 160, 51, 21))
        self.bnt_tryModifySourceContent.setObjectName("bnt_tryModifySourceContent")
        self.bnt_tryReadFile = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_tryReadFile.setGeometry(QtCore.QRect(280, 70, 75, 23))
        self.bnt_tryReadFile.setObjectName("bnt_tryReadFile")
        self.bnt_tryPrint = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_tryPrint.setGeometry(QtCore.QRect(230, 210, 75, 23))
        self.bnt_tryPrint.setObjectName("bnt_tryPrint")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 54, 12))
        self.label_2.setObjectName("label_2")
        self.btwFileList_copy = QtWidgets.QComboBox(self.groupBox_2)
        self.btwFileList_copy.setGeometry(QtCore.QRect(20, 40, 241, 22))
        self.btwFileList_copy.setObjectName("btwFileList_copy")
        self.bnt_refreshFileList = QtWidgets.QPushButton(self.groupBox_2)
        self.bnt_refreshFileList.setGeometry(QtCore.QRect(280, 40, 75, 23))
        self.bnt_refreshFileList.setObjectName("bnt_refreshFileList")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 10, 351, 341))
        self.groupBox_4.setObjectName("groupBox_4")
        self.lineEdit_password = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_password.setGeometry(QtCore.QRect(100, 56, 133, 20))
        self.lineEdit_password.setTabletTracking(True)
        self.lineEdit_password.setReadOnly(False)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(34, 56, 24, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_employeeID = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_employeeID.setGeometry(QtCore.QRect(100, 20, 133, 20))
        self.lineEdit_employeeID.setTabletTracking(True)
        self.lineEdit_employeeID.setReadOnly(False)
        self.lineEdit_employeeID.setObjectName("lineEdit_employeeID")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(34, 20, 48, 16))
        self.label_10.setObjectName("label_10")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(20, 208, 60, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(10, 238, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(34, 92, 36, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(34, 274, 36, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(34, 310, 36, 16))
        self.label_16.setObjectName("label_16")
        self.lineEdit_workOrder = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_workOrder.setGeometry(QtCore.QRect(100, 92, 133, 20))
        self.lineEdit_workOrder.setObjectName("lineEdit_workOrder")
        self.lineEdit_SN_QTY = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_SN_QTY.setGeometry(QtCore.QRect(100, 238, 133, 20))
        self.lineEdit_SN_QTY.setObjectName("lineEdit_SN_QTY")
        self.lineEdit_NGnum = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_NGnum.setGeometry(QtCore.QRect(100, 274, 133, 20))
        self.lineEdit_NGnum.setObjectName("lineEdit_NGnum")
        self.lineEdit_OKnum = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_OKnum.setGeometry(QtCore.QRect(100, 310, 133, 20))
        self.lineEdit_OKnum.setObjectName("lineEdit_OKnum")
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setGeometry(QtCore.QRect(34, 178, 41, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_original_SN = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_original_SN.setGeometry(QtCore.QRect(100, 178, 133, 20))
        self.lineEdit_original_SN.setObjectName("lineEdit_original_SN")
        self.lineEdit_TARGET_QTY = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_TARGET_QTY.setGeometry(QtCore.QRect(100, 208, 133, 20))
        self.lineEdit_TARGET_QTY.setObjectName("lineEdit_TARGET_QTY")
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setGeometry(QtCore.QRect(30, 130, 54, 12))
        self.label_18.setObjectName("label_18")
        self.lineEdit_btwFileName = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_btwFileName.setGeometry(QtCore.QRect(100, 130, 133, 20))
        self.lineEdit_btwFileName.setReadOnly(True)
        self.lineEdit_btwFileName.setObjectName("lineEdit_btwFileName")
        self.bnt_webapi_login = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_webapi_login.setGeometry(QtCore.QRect(250, 60, 75, 23))
        self.bnt_webapi_login.setObjectName("bnt_webapi_login")
        self.bnt_push_work_order = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_push_work_order.setEnabled(False)
        self.bnt_push_work_order.setGeometry(QtCore.QRect(250, 90, 75, 23))
        self.bnt_push_work_order.setObjectName("bnt_push_work_order")
        self.bnt_modify_btw_file = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_modify_btw_file.setEnabled(False)
        self.bnt_modify_btw_file.setGeometry(QtCore.QRect(250, 180, 75, 23))
        self.bnt_modify_btw_file.setObjectName("bnt_modify_btw_file")
        self.bnt_startAutoRun = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_startAutoRun.setEnabled(True)
        self.bnt_startAutoRun.setGeometry(QtCore.QRect(250, 210, 75, 23))
        self.bnt_startAutoRun.setObjectName("bnt_startAutoRun")
        self.bnt_stopAutoRun = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_stopAutoRun.setEnabled(False)
        self.bnt_stopAutoRun.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.bnt_stopAutoRun.setObjectName("bnt_stopAutoRun")
        self.bnt_connect_SCISmart = QtWidgets.QPushButton(self.groupBox_4)
        self.bnt_connect_SCISmart.setEnabled(False)
        self.bnt_connect_SCISmart.setGeometry(QtCore.QRect(250, 130, 75, 23))
        self.bnt_connect_SCISmart.setObjectName("bnt_connect_SCISmart")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 370, 351, 151))
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
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 50, 239, 54))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.bnt_scanSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_scanSerial.setObjectName("bnt_scanSerial")
        self.gridLayout.addWidget(self.bnt_scanSerial, 0, 0, 1, 1)
        self.bnt_closeSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_closeSerial.setObjectName("bnt_closeSerial")
        self.gridLayout.addWidget(self.bnt_closeSerial, 0, 1, 1, 1)
        self.bnt_openSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_openSerial.setObjectName("bnt_openSerial")
        self.gridLayout.addWidget(self.bnt_openSerial, 0, 2, 1, 1)
        self.bnt_autoSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_autoSerial.setObjectName("bnt_autoSerial")
        self.gridLayout.addWidget(self.bnt_autoSerial, 1, 0, 1, 1)
        self.bnt_connectSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_connectSerial.setObjectName("bnt_connectSerial")
        self.gridLayout.addWidget(self.bnt_connectSerial, 1, 1, 1, 1)
        self.bnt_breakSerial = QtWidgets.QPushButton(self.layoutWidget1)
        self.bnt_breakSerial.setObjectName("bnt_breakSerial")
        self.gridLayout.addWidget(self.bnt_breakSerial, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(10, 120, 54, 12))
        self.label.setObjectName("label")
        self.PrintersList = MyComboBox(self.groupBox_3)
        self.PrintersList.setGeometry(QtCore.QRect(60, 120, 251, 22))
        self.PrintersList.setObjectName("PrintersList")
        self.tabWidget.addTab(self.tab, "")
        self.groupBox_5 = QtWidgets.QGroupBox(Form)
        self.groupBox_5.setGeometry(QtCore.QRect(440, 250, 311, 131))
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(20, 60, 54, 12))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox_5)
        self.label_21.setGeometry(QtCore.QRect(20, 90, 54, 12))
        self.label_21.setObjectName("label_21")
        self.print_num = QtWidgets.QLineEdit(self.groupBox_5)
        self.print_num.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.print_num.setObjectName("print_num")
        self.print_check_OK_num = QtWidgets.QLineEdit(self.groupBox_5)
        self.print_check_OK_num.setGeometry(QtCore.QRect(80, 90, 61, 20))
        self.print_check_OK_num.setObjectName("print_check_OK_num")
        self.label_22 = QtWidgets.QLabel(self.groupBox_5)
        self.label_22.setGeometry(QtCore.QRect(160, 90, 54, 12))
        self.label_22.setObjectName("label_22")
        self.print_check_NG_num = QtWidgets.QLineEdit(self.groupBox_5)
        self.print_check_NG_num.setGeometry(QtCore.QRect(220, 90, 51, 20))
        self.print_check_NG_num.setObjectName("print_check_NG_num")
        self.bnt_reset_print_stage = QtWidgets.QPushButton(self.groupBox_5)
        self.bnt_reset_print_stage.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.bnt_reset_print_stage.setObjectName("bnt_reset_print_stage")
        self.print_stage_status = QtWidgets.QLineEdit(self.groupBox_5)
        self.print_stage_status.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.print_stage_status.setObjectName("print_stage_status")
        self.bnt_active_cv1 = QtWidgets.QPushButton(self.groupBox_5)
        self.bnt_active_cv1.setEnabled(False)
        self.bnt_active_cv1.setGeometry(QtCore.QRect(220, 60, 75, 23))
        self.bnt_active_cv1.setObjectName("bnt_active_cv1")
        self.groupBox_6 = QtWidgets.QGroupBox(Form)
        self.groupBox_6.setGeometry(QtCore.QRect(440, 400, 311, 121))
        self.groupBox_6.setObjectName("groupBox_6")
        self.bnt_reset_recheck_stage = QtWidgets.QPushButton(self.groupBox_6)
        self.bnt_reset_recheck_stage.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.bnt_reset_recheck_stage.setObjectName("bnt_reset_recheck_stage")
        self.label_23 = QtWidgets.QLabel(self.groupBox_6)
        self.label_23.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_23.setObjectName("label_23")
        self.recheck_stage_status = QtWidgets.QLineEdit(self.groupBox_6)
        self.recheck_stage_status.setGeometry(QtCore.QRect(90, 30, 113, 20))
        self.recheck_stage_status.setObjectName("recheck_stage_status")
        self.print_recheck_NG_num = QtWidgets.QLineEdit(self.groupBox_6)
        self.print_recheck_NG_num.setGeometry(QtCore.QRect(230, 90, 51, 20))
        self.print_recheck_NG_num.setObjectName("print_recheck_NG_num")
        self.label_24 = QtWidgets.QLabel(self.groupBox_6)
        self.label_24.setGeometry(QtCore.QRect(30, 90, 54, 12))
        self.label_24.setObjectName("label_24")
        self.recheck_OK_num = QtWidgets.QLineEdit(self.groupBox_6)
        self.recheck_OK_num.setGeometry(QtCore.QRect(90, 90, 61, 20))
        self.recheck_OK_num.setObjectName("recheck_OK_num")
        self.label_25 = QtWidgets.QLabel(self.groupBox_6)
        self.label_25.setGeometry(QtCore.QRect(170, 90, 54, 12))
        self.label_25.setObjectName("label_25")
        self.bnt_active_cv2 = QtWidgets.QPushButton(self.groupBox_6)
        self.bnt_active_cv2.setEnabled(False)
        self.bnt_active_cv2.setGeometry(QtCore.QRect(220, 60, 75, 23))
        self.bnt_active_cv2.setObjectName("bnt_active_cv2")
        self.groupBox_7 = QtWidgets.QGroupBox(Form)
        self.groupBox_7.setGeometry(QtCore.QRect(440, 520, 301, 61))
        self.groupBox_7.setObjectName("groupBox_7")
        self.LogPlain = QtWidgets.QTextBrowser(Form)
        self.LogPlain.setGeometry(QtCore.QRect(440, 40, 301, 191))
        self.LogPlain.setObjectName("LogPlain")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "贴标上位机"))
        self.groupBox.setTitle(_translate("Form", "GroupBox"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))
        self.label_3.setText(_translate("Form", "数据源个数"))
        self.lineEdit_PrintCount.setText(_translate("Form", "0"))
        self.lineEdit_FailedCount.setText(_translate("Form", "0"))
        self.label_5.setText(_translate("Form", "打印次数"))
        self.label_6.setText(_translate("Form", "失败次数"))
        self.label_4.setText(_translate("Form", "数据源名称"))
        self.label_7.setText(_translate("Form", "数据源内容"))
        self.bnt_tryModifySourceContent.setText(_translate("Form", "修改"))
        self.bnt_tryReadFile.setText(_translate("Form", "试读取文件"))
        self.bnt_tryPrint.setText(_translate("Form", "试打印"))
        self.label_2.setText(_translate("Form", "标签文件"))
        self.bnt_refreshFileList.setText(_translate("Form", "刷新列表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
        self.groupBox_4.setTitle(_translate("Form", "GroupBox"))
        self.lineEdit_password.setText(_translate("Form", "Windows123.."))
        self.label_11.setText(_translate("Form", "密码"))
        self.lineEdit_employeeID.setText(_translate("Form", "ate"))
        self.label_10.setText(_translate("Form", "员工编号"))
        self.label_12.setText(_translate("Form", "工单目标量"))
        self.label_13.setText(_translate("Form", "工单目前生产量"))
        self.label_14.setText(_translate("Form", "工单号"))
        self.label_15.setText(_translate("Form", "NG数量"))
        self.label_16.setText(_translate("Form", "OK数量"))
        self.lineEdit_workOrder.setText(_translate("Form", "EM_SPKLABEL_AUTO_TEST01"))
        self.lineEdit_NGnum.setText(_translate("Form", "0"))
        self.lineEdit_OKnum.setText(_translate("Form", "0"))
        self.label_17.setText(_translate("Form", "初始SN"))
        self.label_18.setText(_translate("Form", "标签文件"))
        self.bnt_webapi_login.setText(_translate("Form", "登录mes"))
        self.bnt_push_work_order.setText(_translate("Form", "上传工单"))
        self.bnt_modify_btw_file.setText(_translate("Form", "修改SN"))
        self.bnt_startAutoRun.setText(_translate("Form", "准备就绪"))
        self.bnt_stopAutoRun.setText(_translate("Form", "停止"))
        self.bnt_connect_SCISmart.setText(_translate("Form", "SCISmart"))
        self.groupBox_3.setTitle(_translate("Form", "GroupBox"))
        self.label_8.setText(_translate("Form", "串口"))
        self.label_9.setText(_translate("Form", "波特率"))
        self.BaudrateList.setItemText(0, _translate("Form", "115200"))
        self.BaudrateList.setItemText(1, _translate("Form", "9600"))
        self.BaudrateList.setItemText(2, _translate("Form", "38400"))
        self.bnt_scanSerial.setText(_translate("Form", "扫描串口"))
        self.bnt_closeSerial.setText(_translate("Form", "关闭串口"))
        self.bnt_openSerial.setText(_translate("Form", "打开串口"))
        self.bnt_autoSerial.setText(_translate("Form", "自动连接"))
        self.bnt_connectSerial.setText(_translate("Form", "连接设备"))
        self.bnt_breakSerial.setText(_translate("Form", "断开连接"))
        self.label.setText(_translate("Form", "打印机"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.groupBox_5.setTitle(_translate("Form", "打印检测阶段"))
        self.label_19.setText(_translate("Form", "状态"))
        self.label_20.setText(_translate("Form", "打印数量"))
        self.label_21.setText(_translate("Form", "打印OK"))
        self.print_num.setText(_translate("Form", "0"))
        self.print_check_OK_num.setText(_translate("Form", "0"))
        self.label_22.setText(_translate("Form", "打印NG"))
        self.print_check_NG_num.setText(_translate("Form", "0"))
        self.bnt_reset_print_stage.setText(_translate("Form", "reset"))
        self.bnt_active_cv1.setText(_translate("Form", "相机1"))
        self.groupBox_6.setTitle(_translate("Form", "成品检测阶段"))
        self.bnt_reset_recheck_stage.setText(_translate("Form", "reset"))
        self.label_23.setText(_translate("Form", "状态"))
        self.print_recheck_NG_num.setText(_translate("Form", "0"))
        self.label_24.setText(_translate("Form", "OK数量"))
        self.recheck_OK_num.setText(_translate("Form", "0"))
        self.label_25.setText(_translate("Form", "NG数量"))
        self.bnt_active_cv2.setText(_translate("Form", "相机2"))
        self.groupBox_7.setTitle(_translate("Form", "GroupBox"))
