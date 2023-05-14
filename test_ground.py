
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import QStandardItemModel, QStandardItem, QAbstractItemView, QTreeWidgetItem, QSortFilterProxyModel
from PyQt5.QtCore import Qt, pyqtSignal, QEvent

from SimpleFields import Main_MultiList, ElementsList
from GlobalVariables import Mod_Var


def show_stuff():
    # temp.add_data('test new data')
    # temp2.show()
    # temp1.show()
    sel = temp.selected_element()
    test3 = sel.child(0, 0)
    print(str(test3.text()))

def hide_stuff():
    item1 = QStandardItem()
    item1.setText('test1')
    item2 = QStandardItem()
    item2.setText('parente')
    item2.appendRow(item1)
    main_game_tree_model.appendRow(item2)
    return
    # temp1.hide()
    # temp2.hide()

app = QtWidgets.QApplication([])
first_window = QtWidgets.QWidget()
first_window.setWindowTitle("test first")
# first_window.setGeometry(100, 100, 300, 400)

layout_more_main = QtWidgets.QVBoxLayout()
layout_main = QtWidgets.QHBoxLayout()
layout_more_main.addLayout(layout_main)
first_window.setLayout(layout_more_main)
test_button = QtWidgets.QPushButton(text='hide')
test_button.clicked.connect(hide_stuff)
test_button2 = QtWidgets.QPushButton(text='show')
test_button2.clicked.connect(show_stuff)
layout_main.addWidget(test_button)
"""same model"""

main_game_tree_model = QStandardItemModel()
main_game_sorting = QSortFilterProxyModel()
main_game_sorting.setSourceModel(main_game_tree_model)
main_game_sorting.setRecursiveFilteringEnabled(True)
""""""
temp = ElementsList(first_window)
temp.tree_model = main_game_tree_model
temp.sorting = main_game_sorting
temp.setModel(temp.tree_model)
temp.set_up_widget(layout_main)
temp.add_data(Mod_Var.mod_display)
temp2 = ElementsList(first_window)
temp2.tree_model = main_game_tree_model
temp2.sorting = main_game_sorting
temp2.setModel(temp.tree_model)
temp2.set_up_widget(layout_main)
# temp2.add_data(Mod_Var.mod_display)
# temp1 = QtWidgets.QLineEdit()
# temp.returnPressed.connect(test)
layout_main.addWidget(temp)
layout_main.addWidget(temp2)
layout_main.addWidget(test_button2)
# temp2 = QtWidgets.QLineEdit()
# temp.returnPressed.connect(test)
# layout_main.addWidget(temp2)
"""testing centering stuff"""
test_layout_2 = QtWidgets.QVBoxLayout()
test2label = QtWidgets.QLabel('text 2')
test_layout_2.addWidget(test2label)
layout_more_main.addLayout(test_layout_2)
test2label.setAlignment(QtCore.Qt.AlignCenter)

first_window.show()
sys.exit(app.exec())
