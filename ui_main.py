# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTextBrowser,
    QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(709, 565)
        font = QFont()
        font.setPointSize(12)
        Form.setFont(font)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 50, 71, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.label.setFont(font1)
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(7, 30, 671, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 131, 31))
        self.label_2.setFont(font1)
        self.add_url = QPushButton(Form)
        self.add_url.setObjectName(u"add_url")
        self.add_url.setGeometry(QRect(600, 50, 81, 31))
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 290, 181, 21))
        self.label_3.setFont(font1)
        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 310, 671, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 330, 51, 31))
        self.label_4.setFont(font1)
        self.quality = QComboBox(Form)
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.addItem("")
        self.quality.setObjectName(u"quality")
        self.quality.setGeometry(QRect(70, 330, 101, 31))
        self.download = QPushButton(Form)
        self.download.setObjectName(u"download")
        self.download.setGeometry(QRect(10, 520, 171, 31))
        self.remain_file = QCheckBox(Form)
        self.remain_file.setObjectName(u"remain_file")
        self.remain_file.setGeometry(QRect(10, 370, 171, 31))
        self.remain_file.setChecked(False)
        self.info = QTextBrowser(Form)
        self.info.setObjectName(u"info")
        self.info.setGeometry(QRect(420, 320, 261, 231))
        font2 = QFont()
        font2.setPointSize(8)
        self.info.setFont(font2)
        self.video_url_input = QTextEdit(Form)
        self.video_url_input.setObjectName(u"video_url_input")
        self.video_url_input.setGeometry(QRect(80, 50, 511, 32))
        font3 = QFont()
        font3.setPointSize(8)
        font3.setKerning(True)
        self.video_url_input.setFont(font3)
        self.video_url_input.setAcceptRichText(False)
        self.openinexplorer = QPushButton(Form)
        self.openinexplorer.setObjectName(u"openinexplorer")
        self.openinexplorer.setGeometry(QRect(10, 480, 171, 31))
        self.setting = QPushButton(Form)
        self.setting.setObjectName(u"setting")
        self.setting.setGeometry(QRect(10, 440, 81, 31))
        self.video_list = QTableWidget(Form)
        if (self.video_list.columnCount() < 3):
            self.video_list.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.video_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.video_list.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.video_list.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.video_list.setObjectName(u"video_list")
        self.video_list.setGeometry(QRect(10, 90, 671, 192))
        self.video_list.setFont(font2)
        self.video_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.video_list.setRowCount(0)
        self.login = QPushButton(Form)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(100, 440, 81, 31))
        self.state = QTextBrowser(Form)
        self.state.setObjectName(u"state")
        self.state.setGeometry(QRect(210, 510, 181, 41))
        self.qrcode = QLabel(Form)
        self.qrcode.setObjectName(u"qrcode")
        self.qrcode.setGeometry(QRect(210, 325, 181, 181))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u54d4\u54e9\u54d4\u54e9\u5168\u7ad9\u89c6\u9891\u4e0b\u8f7d~~Ciallo", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u89c6\u9891\u5730\u5740\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Step1:\u89e3\u6790\u89c6\u9891\u5730\u5740", None))
        self.add_url.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Step2:\u9009\u62e9\u6e05\u6670\u5ea6\u4e0b\u8f7d", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6e05\u6670\u5ea6\uff1a", None))
        self.quality.setItemText(0, QCoreApplication.translate("Form", u"\u8d85\u6e05 4K", None))
        self.quality.setItemText(1, QCoreApplication.translate("Form", u"\u9ad8\u6e05 1080P60", None))
        self.quality.setItemText(2, QCoreApplication.translate("Form", u"\u9ad8\u6e05 1080P+", None))
        self.quality.setItemText(3, QCoreApplication.translate("Form", u"\u9ad8\u6e05 1080P", None))
        self.quality.setItemText(4, QCoreApplication.translate("Form", u"\u9ad8\u6e05 720P", None))
        self.quality.setItemText(5, QCoreApplication.translate("Form", u"\u6e05\u6670 480P", None))
        self.quality.setItemText(6, QCoreApplication.translate("Form", u"\u6d41\u7545 360P", None))

        self.download.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d", None))
        self.remain_file.setText(QCoreApplication.translate("Form", u"\u4fdd\u7559\u97f3\u89c6\u9891\u5206\u79bb\u6587\u4ef6", None))
        self.video_url_input.setPlaceholderText(QCoreApplication.translate("Form", u" \u8bf7\u8f93\u5165\u89c6\u9891\u5730\u5740~~", None))
        self.openinexplorer.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u4e0b\u8f7d\u6587\u4ef6\u5939", None))
        self.setting.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e", None))
        ___qtablewidgetitem = self.video_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u53ef\u9009", None));
        ___qtablewidgetitem1 = self.video_list.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u6807\u9898", None));
        ___qtablewidgetitem2 = self.video_list.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u4e13\u8f91\u540d", None));
        self.login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.qrcode.setText("")
    # retranslateUi

