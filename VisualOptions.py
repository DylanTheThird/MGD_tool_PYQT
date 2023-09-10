# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VisualOptions.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from otherFunctions import update_config_data
import GlobalVariables
from SimpleFields import ElementsList, mod_temp_data

class Visual_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("VisualOptions")
        Dialog.resize(310, 500)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 10, 301, 481))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lcdNumber = QtWidgets.QLCDNumber(self.widget)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout.addWidget(self.lcdNumber)
        self.dial = QtWidgets.QDial(self.widget)
        self.dial.setMaximum(30)
        self.dial.setPageStep(1)
        self.dial.setWrapping(True)
        self.dial.setNotchesVisible(False)
        self.dial.setObjectName("dial")
        self.horizontalLayout.addWidget(self.dial)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_prev_font = QtWidgets.QLabel(self.widget)
        self.label_prev_font.setObjectName("label_prev_font")
        self.verticalLayout.addWidget(self.label_prev_font)
        self.comboBox_font = QtWidgets.QFontComboBox(self.widget)
        self.comboBox_font.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBox_font.setObjectName("comboBox_font")
        self.comboBox_font.activated.connect(self.display_font_in_label)
        self.verticalLayout.addWidget(self.comboBox_font)
        self.label_next_font = QtWidgets.QLabel(self.widget)
        self.label_next_font.setObjectName("label_next_font")
        self.verticalLayout.addWidget(self.label_next_font)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        # self.label.setFrameShape(QtWidgets.QFrame.Panel)
        # self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setObjectName("label")
        self.label.mousePressEvent = lambda arg1: self.mark_field(field_no=1)
        self.verticalLayout_2.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        # self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.mousePressEvent = lambda arg1: self.mark_field(field_no=0)
        self.verticalLayout_2.addWidget(self.textEdit)
        """here is for adding stances"""
        self.stance_text = QtWidgets.QLineEdit()
        self.stance_text.setPlaceholderText('NEW STANCE')
        # main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.stance_text.setObjectName("stanceText")
        # self.textEdit.returnPressed.connect(self.add_stance)
        # self.textEdit.setFocus()
        self.verticalLayout_2.addWidget(self.stance_text)
        button_stance = QtWidgets.QPushButton("Add Stance", self.widget)
        self.verticalLayout_2.addWidget(button_stance)
        button_stance.clicked.connect(self.add_stance)
        self.tree_stances = StanceElement()
        self.tree_stances.set_up_widget(self.verticalLayout_2)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.update_config)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.dial.valueChanged['int'].connect(self.lcdNumber.display)
        self.dial.valueChanged['int'].connect(self.set_font)
        # self.dial_2.valueChanged['int'].connect(self.change_font_in_dropdown)
        # self.current_dial_font_values = self.dial_2.value()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.selected_widget = 2

        # update data to current font as in config file which was loaded to global var
        current_font = QtGui.QFont(GlobalVariables.Glob_Var.current_label_font_type,
                                   GlobalVariables.Glob_Var.current_label_font_size)
        # current_font = self.textEdit.font()
        self.label.setFont(current_font)
        current_font = QtGui.QFont(GlobalVariables.Glob_Var.current_text_font_type,
                                   GlobalVariables.Glob_Var.current_text_font_size)
        self.textEdit.setText("Click label or this field to change font.\nExample text used in scenes and other places")
        self.textEdit.setFont(current_font)
        self.comboBox_font.setCurrentText(current_font.family())
        self.dial.setValue(current_font.pointSize())
        self.display_font_in_label()


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Visual Options"))
        self.label_prev_font.setText(_translate("Dialog", "previous font"))
        self.label_next_font.setText(_translate("Dialog", "next font"))
        self.label.setText(_translate("Dialog", "TextLabel"))

    def test(self):
        print('test')
    def mark_field(self, field_no):
        if field_no == 1:
            self.selected_widget = 1
            self.label.setFrameShape(QtWidgets.QFrame.Panel)
            self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        else:
            self.selected_widget = 2
            self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.textEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.update_input_values()

    def update_input_values(self):
        if self.selected_widget == 1:
            currect_font = self.label.font()
        else:
            currect_font = self.textEdit.font()
        self.dial.setValue(currect_font.pointSize())
        self.comboBox_font.setCurrentText(currect_font.family())
        self.display_font_in_label()

    def font_up(self):
        current_font_no = self.comboBox_font.currentIndex()
        if current_font_no > self.comboBox_font.count():
            self.comboBox_font.setCurrentIndex(current_font_no+1)
            self.display_font_in_label()

    def font_down(self):
        current_font_no = self.comboBox_font.currentIndex()
        if current_font_no < 0:
            self.comboBox_font.setCurrentIndex(current_font_no-1)
            self.display_font_in_label()

    def display_font_in_label(self):
        current_font_no = self.comboBox_font.currentIndex()
        self.comboBox_font.maxCount()
        if self.comboBox_font.count() > current_font_no > 0:
            self.label_prev_font.setText(self.comboBox_font.itemText(current_font_no - 1))
            self.label_next_font.setText(self.comboBox_font.itemText(current_font_no + 1))
        elif current_font_no == 0:
            self.label_prev_font.setText(self.comboBox_font.itemText(current_font_no))
            self.label_next_font.setText(self.comboBox_font.itemText(current_font_no + 1))
        elif current_font_no == self.comboBox_font.count():
            self.label_prev_font.setText(self.comboBox_font.itemText(current_font_no - 1))
            self.label_next_font.setText(self.comboBox_font.itemText(current_font_no))
        self.set_font()

    def set_font(self):
        font_type = self.comboBox_font.currentText()
        font_size = self.dial.value()
        if self.selected_widget == 1:
            self.label.setFont(QtGui.QFont(font_type, font_size))
        else:
            # self.textEdit.setCurrentFont(QtGui.QFont(font_type, font_size))
            self.textEdit.setFont(QtGui.QFont(font_type, font_size))

    def update_config(self):
        currect_label = self.label.font()
        currect_text = self.textEdit.font()
        update_config_data(['label_font_type', 'label_font_size', 'text_font_type',
                            'text_font_size'], [currect_label.family(), currect_label.pointSize(),
                                                        currect_text.family(), currect_text.pointSize()])
        # app.setStyleSheet("QLabel{font-size: 18pt;}") # - different way, but no access to main app from here
        QtWidgets.QApplication.setFont(currect_label, "QLabel")
        QtWidgets.QApplication.setFont(currect_label, "QTextEdit") # TODO check if this works
        """get stances from custom branch and save in temp mod data."""
        stances_list = self.tree_stances.get_data()
        stances_list = stances_list[0]['Custom']
        mod_temp_data.add_stances(stances_list)

    def add_stance(self):
        new_stance = self.stance_text.text()
        self.stance_text.clear()
        # selection = self.tree_stances.selected_element()
        # insert = None
        # if selection:
        #     if selection.parent().data() == 'Custom':
        #         insert = selection.row()
        # if insert:
        #     self.tree_stances.insert_row([new_stance])
        # else:
        self.tree_stances.add_data([new_stance], 'Custom')


class StanceElement(ElementsList):
    def __init__(self, title='Stances'):
        super().__init__(None, listTitle=title, search_field=True)
        self.add_data(GlobalVariables.Glob_Var.stances)
    def delete_with_backup(self):
        selected_stance_item = self.selected_element()
        item_parent = self.find_root_parent(selected_stance_item)
        if item_parent:
            if item_parent.text() != 'Custom':
                return
        else:
            return
        super().delete_with_backup()


# class Stances_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("StancesOptions")
#         Dialog.resize(240, 310)
#         self.widget = QtWidgets.QWidget(Dialog)
#         # self.widget.setGeometry(QtCore.QRect(0, 10, 301, 281))
#         self.widget.setObjectName("widget")
#         main_layout = QtWidgets.QVBoxLayout()
#         self.widget.setLayout(main_layout)
#         main_layout.setObjectName("horizontalLayout")
#         self.textEdit = QtWidgets.QLineEdit()
#         # main_layout.setAlignment(QtCore.Qt.AlignCenter)
#         self.textEdit.setObjectName("textEdit")
#         # self.textEdit.returnPressed.connect(self.add_stance)
#         # self.textEdit.setFocus()
#         main_layout.addWidget(self.textEdit)
#         button_stance = QtWidgets.QPushButton("Add Stance", self.widget)
#         main_layout.addWidget(button_stance)
#         button_stance.clicked.connect(self.test)
#         self.tree_stances = StanceElement()
#         self.tree_stances.set_up_widget(main_layout)
#         self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")
#         main_layout.addWidget(self.buttonBox)
#         self.retranslateUi(Dialog)
#         self.buttonBox.accepted.connect(self.update_config)
#         self.buttonBox.accepted.connect(Dialog.accept)
#         self.buttonBox.rejected.connect(Dialog.reject)
#         # button_stance.clicked.connect(self.add_stance)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#     def test(self):
#         print('test')
#
#
#     def retranslateUi(self, dialog):
#         _translate = QtCore.QCoreApplication.translate
#         dialog.setWindowTitle(_translate("Dialog", "Stance Options"))
#
#     def add_stance(self):
#         new_stance = self.textEdit.text()
#         self.textEdit.clear()
#
#         selection = self.tree_stances.selected_element()
#         insert = None
#         if selection:
#             if selection.parent().data() == 'Custom':
#                 insert = selection.row()
#         if insert:
#             self.tree_stances.insert_row([new_stance])
#         else:
#             self.tree_stances.add_data([new_stance])
#
#     def update_config(self):
#         """get stances from custom branch and save in temp mod data."""
#         stances_list = self.tree_stances.get_data()
#         stances_list = stances_list[0]['Custom']
#         mod_temp_data.add_stances(stances_list)

# might as well add here object for stances

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     # window = Window()
#     window = QtWidgets.QMainWindow()
#     prototype = Stances_Dialog(window)
#     prototype.setupUi()
#     window.show()
#     sys.exit(app.exec())
