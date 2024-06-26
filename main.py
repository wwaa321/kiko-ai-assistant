# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 939)
        MainWindow.setStyleSheet("background-color: #e9f0f1;\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 401, 861))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.output_content = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_content.sizePolicy().hasHeightForWidth())
        self.output_content.setSizePolicy(sizePolicy)
        self.output_content.setMinimumSize(QtCore.QSize(0, 450))
        self.output_content.setMaximumSize(QtCore.QSize(16777215, 450))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.output_content.setFont(font)
        self.output_content.setStyleSheet("background-color: #f4f9fa;;\n"
"border: 1px solid #a6bbd0;\n"
"border-radius: 3px;\n"
"padding-top: 10px;;\n"
"")
        self.output_content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_content.setObjectName("output_content")
        self.verticalLayout.addWidget(self.output_content)
        self.comboBox_function = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_function.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.comboBox_function.setFont(font)
        self.comboBox_function.setStyleSheet("QComboBox {\n"
"    background-color: #f4f9fa;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 3px;\n"
"}\n"
"QComboBox:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.comboBox_function.setObjectName("comboBox_function")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.verticalLayout.addWidget(self.comboBox_function)
        self.lineEdit_notes = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_notes.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.lineEdit_notes.setFont(font)
        self.lineEdit_notes.setStyleSheet("QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 3px;\n"
"}\n"
"QLineEdit:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"}")
        self.lineEdit_notes.setFrame(False)
        self.lineEdit_notes.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.lineEdit_notes.setObjectName("lineEdit_notes")
        self.verticalLayout.addWidget(self.lineEdit_notes)
        self.input_text = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.input_text.setMinimumSize(QtCore.QSize(0, 70))
        self.input_text.setMaximumSize(QtCore.QSize(16777215, 180))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.input_text.setFont(font)
        self.input_text.setStyleSheet("background-color: #ffffff;;\n"
"border: 1px solid #a6bbd0;\n"
"border-radius: 3px;\n"
"\n"
"")
        self.input_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.input_text.setPlainText("")
        self.input_text.setObjectName("input_text")
        self.verticalLayout.addWidget(self.input_text)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, 3, -1)
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_submit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_submit.sizePolicy().hasHeightForWidth())
        self.button_submit.setSizePolicy(sizePolicy)
        self.button_submit.setMinimumSize(QtCore.QSize(0, 50))
        self.button_submit.setMaximumSize(QtCore.QSize(350, 50))
        self.button_submit.setBaseSize(QtCore.QSize(390, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_submit.setFont(font)
        self.button_submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_submit.setStyleSheet("QPushButton {\n"
"    background-color: #a6bbd0;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#000;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #000;\n"
"}")
        self.button_submit.setDefault(False)
        self.button_submit.setObjectName("button_submit")
        self.horizontalLayout_3.addWidget(self.button_submit)
        self.button_Favorites = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_Favorites.sizePolicy().hasHeightForWidth())
        self.button_Favorites.setSizePolicy(sizePolicy)
        self.button_Favorites.setMinimumSize(QtCore.QSize(50, 50))
        self.button_Favorites.setMaximumSize(QtCore.QSize(50, 50))
        self.button_Favorites.setBaseSize(QtCore.QSize(361, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_Favorites.setFont(font)
        self.button_Favorites.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_Favorites.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_Favorites.setText("")
        self.button_Favorites.setObjectName("button_Favorites")
        self.horizontalLayout_3.addWidget(self.button_Favorites)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_Import_Notes_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_Import_Notes_3.setMinimumSize(QtCore.QSize(50, 50))
        self.button_Import_Notes_3.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_Import_Notes_3.setFont(font)
        self.button_Import_Notes_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_Import_Notes_3.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_Import_Notes_3.setText("")
        self.button_Import_Notes_3.setObjectName("button_Import_Notes_3")
        self.horizontalLayout_2.addWidget(self.button_Import_Notes_3)
        self.button_Import_Notes_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_Import_Notes_2.setMinimumSize(QtCore.QSize(50, 50))
        self.button_Import_Notes_2.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_Import_Notes_2.setFont(font)
        self.button_Import_Notes_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_Import_Notes_2.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_Import_Notes_2.setText("")
        self.button_Import_Notes_2.setObjectName("button_Import_Notes_2")
        self.horizontalLayout_2.addWidget(self.button_Import_Notes_2)
        self.button_Import_Notes = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_Import_Notes.setMinimumSize(QtCore.QSize(50, 50))
        self.button_Import_Notes.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_Import_Notes.setFont(font)
        self.button_Import_Notes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_Import_Notes.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_Import_Notes.setText("")
        self.button_Import_Notes.setObjectName("button_Import_Notes")
        self.horizontalLayout_2.addWidget(self.button_Import_Notes)
        self.button_export = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_export.setMinimumSize(QtCore.QSize(50, 50))
        self.button_export.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_export.setFont(font)
        self.button_export.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_export.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_export.setText("")
        self.button_export.setObjectName("button_export")
        self.horizontalLayout_2.addWidget(self.button_export)
        self.button_clear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_clear.sizePolicy().hasHeightForWidth())
        self.button_clear.setSizePolicy(sizePolicy)
        self.button_clear.setMinimumSize(QtCore.QSize(50, 50))
        self.button_clear.setMaximumSize(QtCore.QSize(50, 50))
        self.button_clear.setBaseSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_clear.setFont(font)
        self.button_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_clear.setToolTip("")
        self.button_clear.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_clear.setText("")
        self.button_clear.setObjectName("button_clear")
        self.horizontalLayout_2.addWidget(self.button_clear)
        self.button_clipboard = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_clipboard.sizePolicy().hasHeightForWidth())
        self.button_clipboard.setSizePolicy(sizePolicy)
        self.button_clipboard.setMinimumSize(QtCore.QSize(50, 50))
        self.button_clipboard.setMaximumSize(QtCore.QSize(50, 50))
        self.button_clipboard.setBaseSize(QtCore.QSize(361, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_clipboard.setFont(font)
        self.button_clipboard.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_clipboard.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_clipboard.setText("")
        self.button_clipboard.setObjectName("button_clipboard")
        self.horizontalLayout_2.addWidget(self.button_clipboard)
        self.button_todo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_todo.setMinimumSize(QtCore.QSize(50, 50))
        self.button_todo.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.button_todo.setFont(font)
        self.button_todo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_todo.setStyleSheet("QPushButton {\n"
"    background-color: #e9f0f1;;\n"
"    border: 1px solid #a6bbd0;\n"
"    border-radius: 5px;\n"
"    color:#fff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #bdd2e7;\n"
"    border: 1px solid #a6bbd0;\n"
"    color: #fff;\n"
"}")
        self.button_todo.setText("")
        self.button_todo.setObjectName("button_todo")
        self.horizontalLayout_2.addWidget(self.button_todo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 26))
        self.menubar.setObjectName("menubar")
        self.menu_set = QtWidgets.QMenu(self.menubar)
        self.menu_set.setStyleSheet("")
        self.menu_set.setObjectName("menu_set")
        self.menu_info = QtWidgets.QMenu(self.menubar)
        self.menu_info.setObjectName("menu_info")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_xinghuo = QtWidgets.QAction(MainWindow)
        self.action_xinghuo.setObjectName("action_xinghuo")
        self.action_obsidian = QtWidgets.QAction(MainWindow)
        self.action_obsidian.setObjectName("action_obsidian")
        self.action_info = QtWidgets.QAction(MainWindow)
        self.action_info.setObjectName("action_info")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.action_sponsor = QtWidgets.QAction(MainWindow)
        self.action_sponsor.setObjectName("action_sponsor")
        self.menu_set.addAction(self.action_xinghuo)
        self.menu_set.addAction(self.action_obsidian)
        self.menu_info.addAction(self.action_info)
        self.menu_info.addAction(self.action_help)
        self.menu_info.addAction(self.action_sponsor)
        self.menubar.addAction(self.menu_set.menuAction())
        self.menubar.addAction(self.menu_info.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kiko AI助手"))
        self.comboBox_function.setItemText(0, _translate("MainWindow", "对话："))
        self.comboBox_function.setItemText(1, _translate("MainWindow", "扩写以下文档："))
        self.comboBox_function.setItemText(2, _translate("MainWindow", "提高以下文档写作水平："))
        self.comboBox_function.setItemText(3, _translate("MainWindow", "总结以下文档："))
        self.comboBox_function.setItemText(4, _translate("MainWindow", "续写以下内容:"))
        self.comboBox_function.setItemText(5, _translate("MainWindow", "解释以下内容:"))
        self.comboBox_function.setItemText(6, _translate("MainWindow", "翻译以下内容:"))
        self.lineEdit_notes.setText(_translate("MainWindow", "要求："))
        self.input_text.setPlaceholderText(_translate("MainWindow", "在此处输入你的内容"))
        self.button_submit.setText(_translate("MainWindow", "提交"))
        self.button_submit.setShortcut(_translate("MainWindow", "Ctrl+Return"))
        self.menu_set.setTitle(_translate("MainWindow", "配置"))
        self.menu_info.setTitle(_translate("MainWindow", "关于"))
        self.action_xinghuo.setText(_translate("MainWindow", "配置大模型"))
        self.action_obsidian.setText(_translate("MainWindow", "配置ObsidinaAPI"))
        self.action_info.setText(_translate("MainWindow", "产品信息"))
        self.action_help.setText(_translate("MainWindow", "使用帮助"))
        self.action_sponsor.setText(_translate("MainWindow", "赞助支持"))
