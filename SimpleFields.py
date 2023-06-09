from os.path import isfile
import copy
# # import textwrap
# # import json
# # from collections import OrderedDict
import GlobalVariables
import otherFunctions
# import FunctionalWindow
# import Edit_Data_Window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem, QAbstractItemView, QSize, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal


"""pyqt widges"""
"""simple fields contains 1 widget, so display and create has not much difference, so display inherits from create.
 display adds option to lock and ulock fields"""


class CustomWidget:
    def __init__(self, master_widget=None, field_name=None, label_pos='H'):
        super().__init__()
        if label_pos == 'H':
            self.custom_layout = QtWidgets.QHBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        else:
            self.custom_layout = QtWidgets.QVBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        if field_name:
            self.label_custom = CustomLabel(master_widget, field_name)
            self.custom_layout.addWidget(self.label_custom)

    def set_up_widget(self, outside_layout, insert_for_optional=False):
        """insert for optional is mostly for optional fields to insert widget before last stretch"""
        if insert_for_optional:
            outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
        else:
            outside_layout.addLayout(self.custom_layout)

    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()
        self.custom_layout.deleteLater()

class CustomLabel(QtWidgets.QLabel):
    # doubleClicked = pyqtSignal()
    def __init__(self, master, label_text):
        super().__init__(parent=master, text=label_text)
        self.setAlignment(QtCore.Qt.AlignRight)

    def update_label(self, new_label):
        self.setText(new_label)

    def change_position(self, position='C/L/R'):
        if position == 'C':
            self.setAlignment(QtCore.Qt.AlignCenter)
        elif position == 'L':
            self.setAlignment(QtCore.Qt.AlignLeft)
        elif position == 'R':
            self.setAlignment(QtCore.Qt.AlignRight)

    def change_background_color(self):
        self.setStyleSheet("background-color: red")
    def clear_color(self):
        self.setStyleSheet("")

class CustomButton(QtWidgets.QPushButton):
    def __init__(self, master, label_text, class_connector=None):
        super().__init__(parent=master, text=label_text)
        self.connector_to_outside_complex_class = class_connector

    def update_label(self, new_label):
        self.setText(new_label)



class SimpleEntry(QtWidgets.QLineEdit):
    def __init__(self, master_widget, field_name=None, field_data=None, template_name=None, class_connector=None
                 , edit=True, main_data_treeview=None, label_pos='H'):
        super().__init__(parent=master_widget)
        if label_pos == 'H':
            self.custom_layout = QtWidgets.QHBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        else:
            self.custom_layout = QtWidgets.QVBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        if field_name:
            # if len(field_name) < 2:
            if isinstance(field_name, int):
                field_name = 'Amount'
            self.label_custom = CustomLabel(master_widget, field_name)
            self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addWidget(self)
        self.template_name = template_name
        self.title = field_name
        self.type = 'text'
        self.old_value = ''
        self.default_value = ''
        self.addition = False
        self.setMinimumWidth(70)
        self.setMaximumWidth(220)
        self.row_size = 1
        """this is for multilist display. in case multilist class accepts only 1 value, no points in making entire tree.
        so intead, just make simple text field, which is created in another class"""
        self.connector_to_outside_complex_class = class_connector
        self.treeview_with_main_and_mod_data = main_data_treeview
        if field_data:
            if 'tooltip' in field_data:
                self.setToolTip(field_data['tooltip'])
            if 'default' in field_data:
                self.default_value = field_data['default']
            if 'options' in field_data:
                if 'addition' in field_data['options']:
                    self.addition = True

        # self.temp_master = master
        self.shortcuts = []
        self.setObjectName('entry')
        if edit:
            self.field_modified_check()

    def clear_val(self):
        self.clear()

    def cancel(self):
        self.setReadOnly(True)
        return

    def get_val(self, temp_dict_container=None):
        return_val = self.text()
        if return_val == "":
            return_val = self.default_value
        if temp_dict_container is not None:
            temp_dict_container[self.title] = return_val
        else:
            return return_val

    def set_val(self, new_value):
        self.setText(new_value)

    def set_up_widget(self, outside_layout, insert_for_optional=False):
        """insert for optional is mostly for optional fields to insert widget before last stretch"""
        if insert_for_optional:
            outside_layout.insertLayout(outside_layout.count()-1, self.custom_layout)
            # outside_layout.insertWidget(outside_layout.count()-1, self.custom_layout)
        else:
            outside_layout.addLayout(self.custom_layout)

    # def set_up_shortcut(self, sequence, function):
    #     shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(sequence), self)
    #     shortcut.activated.connect(function)
    #     self.shortcuts.append(shortcut)

    # if field is in complex class and should allow access to main items, connector will be created. it should
    #  be passed to main game field. If fields does not have access, connector is NONE, so should disconnect main field
    def focusInEvent(self, event):
        if self.connector_to_outside_complex_class and self.treeview_with_main_and_mod_data:
            # GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
            self.treeview_with_main_and_mod_data.connect_multilist(self.connector_to_outside_complex_class)
        else:
            # GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
            if self.treeview_with_main_and_mod_data:
                self.treeview_with_main_and_mod_data.disconnect_multilist()
        super().focusInEvent(event)

    def field_modified_check(self):
        self.textChanged.connect(GlobalVariables.Glob_Var.edited_field)

    def function_on_modify(self, function=None):
        self.textChanged.connect(function)

    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()
    def center(self):
        self.setAlignment(QtCore.Qt.AlignCenter)
    # def focusOutEvent(self, event):
    #     print('event-focus-out:', self.objectName())
    #     super().focusOutEvent(event)


class SimpleEntryDisplay(SimpleEntry):
    doubleClicked = pyqtSignal()

    def __init__(self, master=None, field_name=None, tooltip_text=None, field_data=None, class_connector=None):
        super().__init__(master_widget=master, field_name=field_name, field_data=field_data
                         , class_connector=class_connector)
        self.setReadOnly(True)
        # self.doubleClicked.connect(self.modify_field)
        # self.doubleClicked.connect(otherFunctions.unlock_field(self))

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Escape:
            otherFunctions.lock_field(self)
            # self.cancel()
        # elif event.key() == Qt.Key_Return:
        #     self.save_field()
        return super().keyPressEvent(event)

    def event(self, event):
        if event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            self.doubleClicked.emit()
        return super().event(event)

    def modify_field(self):
        # if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
        #     if self.addition:
        #         flag = True
        #     else:
        #         flag = False
        # else:
        #     flag = True
        # if flag:
        if True:
            self.setReadOnly(False)
            self.setFocus()
        return

    def save_field(self,):
        if '-' in self.template_name:
            field_address = self.template_name.split('-')
            GlobalVariables.current_mod[field_address[0]][GlobalVariables.currentSelectedItem['text']][field_address[1]][
            self.title] = self.get_val()
        else:
            GlobalVariables.current_mod[self.template_name][GlobalVariables.currentSelectedItem['text']][
                self.title] = self.get_val()
        self.cancel()
        return


class NumericEntry(SimpleEntry):
    def __init__(self, master=None, field_name=None, wid=0, template_name=None, field_data=None
                 , class_connector=None, edit=True, label_pos='H'):
        super().__init__(master_widget=master, field_name=field_name, template_name=template_name,
                         field_data=field_data, class_connector=class_connector, edit=edit, label_pos=label_pos)
        """if field name is a number, then change it to amount"""
        # if field_name:
        #     if len(field_name) < 2:
        #         self.title = 'Amount'
        #         self.label_custom.update_label('Amount')
        #     else:
        #         self.title = field_name
        # self.type = 'text'
        # self.default_value = ''
        # if wid == 0:
        #     wid = 30
        # self.setFixedWidth(wid)
        self.setMinimumWidth(30)
        self.setMaximumWidth(30)
        self.setMaxLength(3)
        self.default_value = "0"

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        # check if key is digit or functional like tab or enter
        if 47 < event.key() < 58 or 100 < event.key():
            return super().keyPressEvent(event)


class NumericEntryDisplay(NumericEntry):
    doubleClicked = pyqtSignal()

    def __init__(self, master=None, field_name=None, wid=0, field_data=None, class_connector=None):
        super().__init__(master=master, field_name=field_name, tooltip_text=tooltip_text, wid=wid, f_data=field_data
                         , class_connector=class_connector)
        self.setReadOnly(True)
        self.doubleClicked.connect(self.modify_field)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.cancel()
        # elif event.key() == Qt.Key_Return:
        #     self.save_field()
        return super().keyPressEvent(event)

    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonDblClick:
            self.doubleClicked.emit()
        return super().event(event)

    def modify_field(self):
        # if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
        #     if self.addition:
        #         flag = True
        #     else:
        #         flag = False
        # else:
        #     flag = True
        # if flag:
        if True:
            self.setReadOnly(False)
            self.setFocus()
        return

    def save_field(self, ):
        if '-' in self.template_name:
            field_address = self.template_name.split('-')
            GlobalVariables.current_mod[field_address[0]][GlobalVariables.currentSelectedItem['text']][
                field_address[1]][
                self.title] = self.get_val()
        else:
            GlobalVariables.current_mod[self.template_name][GlobalVariables.currentSelectedItem['text']][
                self.title] = self.get_val()
        self.cancel()
        return

    # def limit_size_day(self, *args):
    #     value = self.var.get()
    #     if len(value) > 3:
    #         self.var.set(value[:3])
    #
    # def check_for_digit(self, event):
    #     v = event.char
    #     try:
    #         v = int(v)
    #     except ValueError:
    #         if v != "\x08" and v != "" and v != ".":
    #             return "break"


class AreaEntry(QtWidgets.QTextEdit):
    def __init__(self, master_window=None, label_text=None, tooltip=None, field_data=None,
                 width_i=200, height_i=70, template_name=None, class_connector=None, edit=True, label_pos='V'):
        super().__init__(parent=master_window)
        self.template_name = template_name
        if label_pos == 'H':
            self.custom_layout = QtWidgets.QHBoxLayout()
        else:
            self.custom_layout = QtWidgets.QVBoxLayout()
        self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.type = 'area'
        self.title = label_text
        self.connector_to_outside_complex_class = class_connector
        self.setFixedWidth(width_i)
        self.setFixedHeight(height_i)
        if label_text:
            self.label_custom = CustomLabel(master_window, label_text)
            self.label_custom.change_position('C')
            self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addWidget(self)
        self.setToolTip(tooltip)
        self.old_value = ''
        self.row_size = 4
        # Font_tuple = ("Comic Sans MS", 8)
        # self.field.configure(font=Font_tuple)
        # self.field.bind('<Double-Button-1>', self.modify_field)
        self.addition = False
        if field_data:
            if 'options' in field_data:
                if 'addition' in field_data['options']:
                    self.addition = True
        # self.setMinimumWidth(width_i)
        # self.setMaximumWidth(120)
        # # self.setFixedWidth(width_i)
        # self.setMinimumHeight(height_i)
        if edit:
            self.field_modified_check()

    def get_val(self, temp_dict_container=None):
        # self.data
        field_text = self.toPlainText()
        field_text = field_text.replace('\n', ' ')
        if temp_dict_container is not None:
            temp_dict_container[self.title] = field_text
        else:
            return field_text

    def set_val(self, value):
        self.setText(value)

    def clear_val(self):
        self.clear()

    def change_size(self, wide, height):
        self.setFixedWidth(wide)
        self.setFixedHeight(height)

    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()
    def focusInEvent(self, event):
        if self.connector_to_outside_complex_class:
            GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
        else:
            GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
        super().focusInEvent(event)

    def field_modified_check(self):
        self.textChanged.connect(GlobalVariables.Glob_Var.edited_field)

    def set_up_widget(self, outside_layout, insert_for_options=False):
        if insert_for_options:
            outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
        else:
            outside_layout.addLayout(self.custom_layout)
        self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)

# obsolete
# class AreaEntryDisplay(AreaEntry):
#     doubleClicked = pyqtSignal()
#
#     def __init__(self, master=None, field_name=None, tooltip_text=None, template_name=None,
#                  width_i=200, height_i=70, class_connector=None):
#         super().__init__(master_window=master, label_text=field_name, tooltip=tooltip_text, template_name=template_name,
#                          width_i=width_i, height_i=height_i, class_connector=class_connector)
#         self.setReadOnly(True)
#         # self.setText('What I would like to do is to execute an action when the text of the QLineEdit is changed programmatically, i.e. by clicking the button , doing the following:')
#         self.doubleClicked.connect(lambda arg=self: otherFunctions.lock_field(arg))
#         # self.doubleClicked.connect(otherFunctions.unlock_field(self))
#         self.shortcut_save_data = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+s'), self)
#         self.shortcut_save_data.activated.connect(self.save_field)
#         self.shortcut_save_data = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+e'), self)
#         self.shortcut_save_data.activated.connect(lambda arg=self: otherFunctions.unlock_field(arg))
#
#     def keyPressEvent(self, event: QtGui.QKeyEvent):
#         if event.key() == Qt.Key_Escape:
#             otherFunctions.lock_field(self)
#         return super().keyPressEvent(event)
#
#     def modify_field(self):
#         # if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
#         #     if self.addition:
#         #         flag = True
#         #     else:
#         #         flag = False
#         # else:
#         #     flag = True
#         # if flag:
#         if True:
#             self.setReadOnly(False)
#             self.setFocus()
#         return
#
#     def save_field(self):
#         print('teste save')
#         return
#         if '-' in self.template_name:
#             field_address = self.template_name.split('-')
#             GlobalVariables.current_mod[field_address[0]][GlobalVariables.currentSelectedItem['text']][field_address[1]][
#             self.title] = self.get_val()
#         else:
#             GlobalVariables.current_mod[self.template_name][GlobalVariables.currentSelectedItem['text']][
#                 self.title] = self.get_val()
#         self.cancel()
#         return
#     def index(self):
#         return self.field.index()


class SingleList(QtWidgets.QComboBox):
    def __init__(self, master_window=None, label_text=None, field_data=None, template_name=None,
                 list_path=None, class_connector=None, edit=True, label_pos='H'):
        super().__init__(parent=master_window)
        self.template_name = template_name
        self.type = 'singlelist'
        # self.field_frame = master
        self.title = label_text
        self.row_size = 1
        self.connector_to_outside_complex_class = class_connector
        if label_pos == 'H':
            self.custom_layout = QtWidgets.QHBoxLayout()
        else:
            self.custom_layout = QtWidgets.QVBoxLayout()
            # self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        if label_text:
            self.label_custom = CustomLabel(master_window, label_text)
            self.custom_layout.addWidget(self.label_custom)
            # self.custom_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.custom_layout.addWidget(self)

        self.addition = False
        # field "playerCanPurchase" in perks is friking  long
        # self.setMaximumWidth(60)
        if field_data:
            if 'tooltip' in field_data:
                self.label_custom.setToolTip(field_data['tooltip'])
            if 'choices' in field_data:
                self.list = otherFunctions.getListOptions(field_data['choices'], "single")
                self.set_val(self.list)
            else:
                self.list = []
                self.list.append('placeholder')
            if 'options' in field_data:
                if 'addition' in field_data['options']:
                    self.addition = True
        if edit:
            self.field_modified_check()
        # self.currentIndexChanged.connect(self.test)

    def get_val(self, temp_dict_container=None):
        if temp_dict_container:
            temp_dict_container[self.title] = self.currentText()
        else:
            return self.currentText()

    def set_val(self, value, sort=True):
        if isinstance(value, list):
            if sort:
                value.sort()
            if len(value) >= 1:
                self.list = value
                self.addItems(value)
        else:
            self.setCurrentText(value)

    def reload_options(self, options_list=list):
        if options_list:
            # self.list = options_list
            self.clear()
            self.list = otherFunctions.getListOptions(options_list, "single")
            self.set_val(self.list)
            # TODO dropdown display adjust
            """below should limit rectangle box that appeares when clicking dropdown, probably for choices, but otherwise limits view"""
            # w = self.fontMetrics().boundingRect(max(self.list, key=len)).width()
            # self.view().setFixedWidth(w + 20)
        else:
            return

    def add_items_to_skip_sort(self, items=list):
        self.list += items
        self.addItems(items)

    def clear_val(self):
        self.setCurrentIndex(0)
        # self.clear()

    def field_modified_check(self):
        self.currentIndexChanged.connect(GlobalVariables.Glob_Var.edited_field)

    def set_up_widget(self, outside_layout, insert_for_options=False):
        if self.custom_layout:
            if insert_for_options:
                outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
            else:
                outside_layout.addLayout(self.custom_layout)
        else:
            if insert_for_options:
                outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
            else:
                outside_layout.addWidget(self)

    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()

    def focusInEvent(self, event):
        if self.connector_to_outside_complex_class:
            GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
        else:
            GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
        super().focusInEvent(event)

# should be obsolete
class SingleListDisplay(SingleList):
    def __init__(self, master_window=None, label_text=None, tooltip=None, template_name=None, list_path=None):
        super().__init__(master_window=master_window, label_text=label_text, tooltip=tooltip, template_name=template_name,
                         list_path=list_path)
        # self.setEnabled(False)
        self.activated.connect(self.modify_field)
    def modify_field(self):
        return
        if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
            if self.addition:
                flag = True
            else:
                flag = False
        else:
            flag = True
        if flag:
            Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
                                                          structure_data=self.get_val(), structure_link=self)


class UniqueView(QtWidgets.QListView):
    def __init__(self, master, field_title=None, class_connector=None, data_treeview=None):
        super().__init__(parent=master)
        self.connector_to_outside_complex_class = class_connector
        self.type = 'multilist'
        self.tree_model = QStandardItemModel()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.model_index = QtCore.QModelIndex()
        self.setModel(self.tree_model)
        self.setMaximumSize(160, 100)
        self.setMinimumHeight(50)
        self.setFixedHeight(20)
        self.flag_edit = True
        self.treeview_with_main_and_mod_data = data_treeview

    def set_val(self, node=None, data=[]):
        # example data ['file',{'folder ':['file']}]
        if not node:
            # node = self.rootnode
            node = self.tree_model
        else:
            if isinstance(node, str):
                node = self.find_node(node)
                node = self.tree_model.itemFromIndex(node)
        for values in data:
            if isinstance(values, dict):
                for keys in values:
                    parent_row = QStandardItem()
                    parent_row.setText(keys)
                    if self.flag_folders:
                        parent_row.setEditable(False)
                    node.appendRow(parent_row)
                    self.add_data(parent_row, values[keys])
            else:
                bottom_row = QStandardItem()
                bottom_row.setText(values)
                if not self.flag_child_editable:
                    bottom_row.setEditable(False)
                node.appendRow(bottom_row)

    def clear_val(self):
        self.tree_model.clear()
        self.setFixedHeight(20)
    def add_data(self, node=None, data=[]):
        # example data ['file',{'folder ':['file']}]
        if not node:
            # node = self.rootnode
            node = self.tree_model
        else:
            if isinstance(node, str):
                node = self.find_node(node)
                node = self.tree_model.itemFromIndex(node)
        if isinstance(data, list):
            for values in data:
                self.add_data(node, values)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                parent_row.setEditable(False)
                node.appendRow(parent_row)
                self.add_data_to_display(parent_row, data[key])
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            bottom_row.setEditable(False)
            node.appendRow(bottom_row)
            if self.height() < 100:
                self.setFixedHeight(self.height() + 20)
        # if not node:
        #     # node = self.rootnode
        #     node = self.tree_model
        # else:
        #     if isinstance(node, str):
        #         node = self.find_node(node)
        #         node = self.tree_model.itemFromIndex(node)
        # for values in data:
        #     if isinstance(values, dict):
        #         for keys in values:
        #             parent_row = QStandardItem()
        #             parent_row.setText(keys)
        #             if self.flag_folders:
        #                 parent_row.setEditable(False)
        #             node.appendRow(parent_row)
        #             self.add_data(parent_row, values[keys])
        #     else:
        #         bottom_row = QStandardItem()
        #         bottom_row.setText(values)
        #         bottom_row.setEditable(False)
        #         node.appendRow(bottom_row)
        if self.flag_edit:
            GlobalVariables.Glob_Var.edited_field()
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            # self.delete_leaf()
            self.delete()
    def delete(self):
        selected_items_idx = self.selectedIndexes()
        selected_items = []
        for idx in selected_items_idx:
            selected_items.append(self.tree_model.itemFromIndex(idx))
        for items in selected_items:
            item = self.tree_model.indexFromItem(items)
            self.tree_model.removeRow(item.row(), item.parent())
            if self.height() > 20:
                self.setFixedHeight(self.height() - 20)
    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()
    def get_data(self, parent_index=None, root_list=None):
        """stuff are in a list, where file should be strings, while folders should be dict
        should return something like [row0, row1, {row2:[row20, row21]},[row3column0, row3column1]}"""
        if parent_index:
            row_range = self.tree_model.rowCount(parent_index)
            col_range = self.tree_model.columnCount(parent_index)
        else:
            row_range = self.tree_model.rowCount()
            col_range = self.tree_model.columnCount()
        current_row_folder = {}
        rows_list = []
        ix = None
        for i in range(row_range):
            cols_list = []
            for ii in range(col_range):
                if parent_index:
                    row_index = self.tree_model.index(i, ii, parent_index)
                else:
                    row_index = self.tree_model.index(i, ii)
                self.get_data(row_index, cols_list)
            # here i would have to check if other columns are empty, if yes, turn cols_list into a string
            for vals in cols_list:
                if not vals:
                    cols_list.remove(vals)
            if len(cols_list) == 1:
                rows_list.append(cols_list[0])
            else:
                rows_list.append(cols_list)
            if parent_index:
                current_row_folder[parent_index.data()] = rows_list
        if current_row_folder:
            root_list.append(current_row_folder)
        else:
            if parent_index:
                root_list.append(parent_index.data())
            else:
                return rows_list
    def focusInEvent(self, event):
        """when clicked on widget, connect it to main multilist, where it filters appropiate items to select and add"""
        if self.connector_to_outside_complex_class:
            # GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
            self.treeview_with_main_and_mod_data.connect_multilist(self.connector_to_outside_complex_class)
        else:
            # GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
            self.treeview_with_main_and_mod_data.disconnect_multilist()
        super().focusInEvent(event)

"""complicated fields contains more widgers, display fields should only have 1 to display,
 so here create inherits from display"""

class ElementsList(QtWidgets.QTreeView):
    def __init__(self, masterWun, listTitle=None, search_field=False, folders=False, all_edit=False, treeview_height=5,
                 delete_flag=True, class_connector=None):
        # TODO add flag to hide and show header
        # TODO ctrl up or down - move rows. Probably cut tthem out and insert
        super().__init__(parent=masterWun)
        self.layout = QtWidgets.QVBoxLayout(masterWun)
        # self.row_placement = rowPos
        # self.col_placement = colPos
        # self.col_span_placement = colspan
        self.title = listTitle
        self.type = 'element_list'
        self.flag_folders = folders
        self.parent_tag = 'folder'
        self.flag_child_editable = all_edit
        self.flag_edit = True
        self.connector_to_outside_complex_class = class_connector
        self.tree_model = QStandardItemModel()
        self.setHeaderHidden(True)
        self.setModel(self.tree_model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # self.search_var = tk.StringVar()
        # self.search_var.trace_add("write", self.searchval)
        """seach fields needs to be last as it required different model to be used and
         I dont know how to add and remove from it"""
        # for example, when limited, find top level element - items, remove other top level stuff, make proxy from it
        #  and use that proxy model
        if search_field:
            self.flag_search = True
            # self.entry_search = QtWidgets.QLineEdit(parent=self)
            self.entry_search = SimpleEntry(self, class_connector=self.connector_to_outside_complex_class)
            # self.entry_search.setMinimumWidth(200)
            self.entry_search.setMaximumSize(150, 20)
            self.entry_search.setMinimumSize(150, 20)
            self.entry_search.setAlignment(QtCore.Qt.AlignCenter)
            self.entry_search.setPlaceholderText("Search")
            self.layout.addWidget(self.entry_search, alignment=QtCore.Qt.AlignCenter)
            self.entry_search.textChanged.connect(self.search_value)
            self.sorting = QtCore.QSortFilterProxyModel()
            self.sorting.setSourceModel(self.tree_model)
            self.sorting.setRecursiveFilteringEnabled(True)
            self.setModel(self.sorting)
        else:
            self.flag_search = False
        self.layout.addWidget(self)
        self.layout.setAlignment(self, QtCore.Qt.AlignCenter)
        self.layout.addStretch(1)


        # self.treeview = QtWidgets.QTreeView(parent=masterWun)
        # if self.title:
        #     header = QtWidgets.QHeaderView()
        #     # header.se
        #     self.treeview.setHeader()
        # else:
        # self.treeview.setHeaderHidden(True)
        # self.tree_model = QStandardItemModel()
        # self.treeview.setModel(self.tree_model)
        # self.rootnode = self.tree_model.invisibleRootItem()
        # self.setHeaderHidden(True)
        # self.tree_model = QStandardItemModel()


        # self.rootnode = self.tree_model.invisibleRootItem()
        self.rootnode = None
        # self.treeview.clicked.connect(self.load_display)
        # self.treeview.doubleClicked.connect(on_tv_select)
        # self.rootnode.

        # row1 = QStandardItem()
        # row1.setEditable(False)
        # row1.setText("row 1")
        # self.rootnode.appendRow(row1)
        # row2 = QStandardItem()
        # row2.setText("row 2")
        # row1.appendRow(row2)
        # self.treeview.bind("<<TreeviewSelect>>", self.on_tv_select)  # bind event on selection
        #
        # # reszta to nudne i przyziemne podpinanie kontrolki scrollbar oraz pozycjonowanie scrollbara i kontrolki treeview
        # self.sb_treeview = tk.Scrollbar(masterWun)
        # self.sb_treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NS + tk.E)
        # # self.sb_treeview.grid(row=self.row_placement+1, column=self.col_placement + colspan, sticky=tk.NS + tk.E)
        # self.treeview.config(yscrollcommand=self.sb_treeview.set, height=treeview_height)
        # self.treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NSEW)
        # # self.treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NSEW, columnspan=colspan)
        # self.treeview.bind("<Control_L>" + "<x>", self.cut_elements)
        # self.treeview.bind("<Control_L>" + "<v>", self.paste_elements)
        # if delete_flag:
        #     # self.treeview.bind("<Delete>", lambda event: self.delete_leaf())
        #     self.treeview.bind("<Delete>", lambda event: self.delete_with_backup())
        #     self.treeview.bind("<Control_L>" + "<z>", lambda event: self.restore_deleted())
        # self.treeview.bind('<Prior>', self.move_up)
        # self.treeview.bind('<Next>', self.move_down)
        # self.treeview.bind('<Escape>', lambda event: self.cancel_selection())
        # self.sb_treeview.config(command=self.treeview.yview)
        # self.treeview.heading("#0", text=listTitle)
        # # style = Style()
        # # style.configure("Treeview",
        # #                 background="#E1E1E1",
        # #                 foreground="#000000",
        # #                 rowheight=25,
        # #                 fieldbackground="#E1E1E1")
        # # style.map('Treeview', background=[('selected', '#BFBFBF')])
        #
        # self.hidden_leafs = []
        # self.detached_elements = []
        # self.treeview.tag_configure('oddrow', background='red')
        # self.back_up_deleted = []
        # # self.sb_treeview.grid(in_=self.treeview, row=1, column=1)
        # # self.terminal_scrollbar = tk.Scrollbar(self)
        # # self.terminal_scrollbar.grid(row=2, column=5, sticky=tk.NS)
        # # self.sb_treeview.place(in_=self.treeview, relx=1., y=0, relheight=1.)
        # # self.treeview.place(x=0, y=0, relwidth=1., relheight=1., width=-18)
        # # self.treeview.pack(expand=True, fill='y')
        # # rowspan = self.row_spaning
        # can figure out how to get data from this treeview, so I put data in sepate var and this will be displayed
        self.tree_data = []
        # temp_data = ['val 1',
        #              {'keys_1': [
        #                  {'sub value 1':
        #                       ['sub sub vvalue 2']
        #                   },
        #                  {'sub value 3':
        #                       ['sub sub vvalue 4']
        #                   },
        #                  'sub value 2']
        #              }, 'val 2']
        # self.add_data(data=temp_data)

        self.setMinimumSize(100, 150)
        self.setMaximumSize(200, 350)
        self.model_index = QtCore.QModelIndex()
        self.back_up_deleted = []

        self.shortcut_restore = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+z'), self)
        self.shortcut_restore.activated.connect(self.restore_deleted)
        self.shortcut_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+x'), self)
        self.shortcut_cut.activated.connect(self.delete_with_backup)
        self.shortcut_paste = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+v'), self)
        self.shortcut_paste.activated.connect(lambda arg1=True: self.restore_deleted(arg1))
        # escapePressed = pyqtSignal(str)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            # print('pressed delete')
            self.delete_with_backup()
        super().keyPressEvent(event)


    def focusInEvent1(self, event):
        # print('event-focus-in:', self.objectName())
        if self.connector_to_outside_complex_class:
            GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
        else:
            GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
        super().focusInEvent(event)

    def hide(self):
        if self.flag_search:
            self.entry_search.hide()
        super().hide()
    def show(self):
        if self.flag_search:
            self.entry_search.show()
        super().show()


    def add_data(self, data=[], node=None, update_flag=False, insert_row=False):
        if update_flag:
            if isinstance(node, str):
                selected_branch = self.find_node(node)
            else:
                selected_branch = node
            # leaves_size = selected_branch.rowCount()
            selected_branch.removeRows(0, selected_branch.rowCount())
            # for i in range(leaves_size-1, -1, -1):
            #     selected_branch.removeRows()
            #     self.tree_model.removeRow(i, selected_branch)

        # else:
        self.add_data_to_display(data, node, insert_row)
    #     self.add_data_to_var()
    # def add_data_to_var(self, node=None, data=[], update_flag=False):
    #     if not node:
    #         self.tree_data.append(data)
    #     # else:

    def add_data_to_display_new_need_adjustment(self, data=[], node=None, insert_row=False):
        """now it either add at the end or add to the node. it would be good if there was separate for
        adding to node and above node"""
        # top level,  gather data into list. this way, if need to insert, just provide row number
        final_items_to_add = []
        selected = self.selected_element()
        if not selected:
            # node = self.rootnode
            node = self.tree_model
        else:
            node = selected
        if isinstance(data, list):
            for values in data:
                if isinstance(values, dict):
                    for key in values:
                        parent_row = QStandardItem()
                        final_items_to_add.append(parent_row)
                        parent_row.setText(key)
                        parent_row.setWhatsThis('folder')
                        if self.flag_folders:
                            parent_row.setEditable(True)
                        else:
                            parent_row.setEditable(False)
                        self.add_data_parent_item(parent_row, values[key])
                else:
                    bottom_row = QStandardItem()
                    bottom_row.setText(values)
                    final_items_to_add.append(bottom_row)
                    if not self.flag_child_editable:
                        bottom_row.setEditable(False)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                final_items_to_add.append(parent_row)
                if self.flag_folders:
                    parent_row.setEditable(True)
                else:
                    parent_row.setEditable(False)
                parent_row.setWhatsThis(self.parent_tag)
                self.add_data_parent_item(parent_row, data[key])
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            if not self.flag_child_editable:
                bottom_row.setEditable(False)
            final_items_to_add.append(bottom_row)

        if insert_row:
            for items in reversed(final_items_to_add):
                """first remove items at insertRow, then add at that place"""
                """this sound like updating, not inserting....."""
                node.removeRow(insert_row)
                node.insertRow(insert_row, items)
                """here we expand child elements of added item. Item itself will not be expanded
                but for that I need index of added element, which is created after adding"""
        else:
            for items in (final_items_to_add):
                node.appendRow(items)
        current_row_count = self.tree_model.rowCount()
        for idx in range(current_row_count):
            item = self.tree_model.item(idx)
            if item.hasChildren():
                for idx in range(item.rowCount()):
                    self.expand(self.tree_model.indexFromItem(item.child(idx)))
        if self.flag_edit:
            GlobalVariables.Glob_Var.edited_field()

    def add_data_to_display(self, data=[], node=None, insert_row=False):
        # top level,  gather data into list. this way, if need to insert, just provide row number
        final_items_to_add = []
        if not node:
            # node = self.rootnode
            node = self.tree_model
        else:
            if isinstance(node, str):
                node = self.find_node(node)
                node = self.tree_model.itemFromIndex(node)
        if isinstance(data, list):
            for values in data:
                if isinstance(values, dict):
                    for key in values:
                        parent_row = QStandardItem()
                        final_items_to_add.append(parent_row)
                        parent_row.setText(key)
                        parent_row.setWhatsThis(self.parent_tag)
                        if self.flag_folders:
                            parent_row.setEditable(True)
                        else:
                            parent_row.setEditable(False)
                        self.add_data_parent_item(parent_row, values[key])
                else:
                    bottom_row = QStandardItem()
                    bottom_row.setText(values)
                    final_items_to_add.append(bottom_row)
                    if not self.flag_child_editable:
                        bottom_row.setEditable(False)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                final_items_to_add.append(parent_row)
                if self.flag_folders:
                    parent_row.setEditable(True)
                else:
                    parent_row.setEditable(False)
                parent_row.setWhatsThis(self.parent_tag)
                self.add_data_parent_item(parent_row, data[key])
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            if not self.flag_child_editable:
                bottom_row.setEditable(False)
            final_items_to_add.append(bottom_row)

        if insert_row:
            for items in reversed(final_items_to_add):
                """first remove items at insertRow, then add at that place"""
                """this sound like updating, not inserting....."""
                node.removeRow(insert_row)
                node.insertRow(insert_row, items)
                """here we expand child elements of added item. Item itself will not be expanded
                but for that I need index of added element, which is created after adding"""
        else:
            for items in (final_items_to_add):
                node.appendRow(items)
        current_row_count = self.tree_model.rowCount()
        for idx in range(current_row_count):
            item = self.tree_model.item(idx)
            if item.hasChildren():
                for idx in range(item.rowCount()):
                    self.expand(self.tree_model.indexFromItem(item.child(idx)))
        if self.flag_edit:
            GlobalVariables.Glob_Var.edited_field()


    def add_data_parent_item(self, node=None, data=[]):
        # same as above, but without final items, just add more rows to parent node
        if isinstance(node, str):
            node = self.find_node(node)
            node = self.tree_model.itemFromIndex(node)
        if isinstance(data, list):
            for values in data:
                if isinstance(values, dict):
                    for key in values:
                        parent_row = QStandardItem()
                        parent_row.setText(key)
                        if self.flag_folders:
                            parent_row.setEditable(True)
                        else:
                            parent_row.setEditable(False)
                        parent_row.setWhatsThis(self.parent_tag)
                        self.add_data_parent_item(parent_row, values[key])
                        node.appendRow(parent_row)
                else:
                    bottom_row = QStandardItem()
                    bottom_row.setText(values)
                    if not self.flag_child_editable:
                        bottom_row.setEditable(False)
                    node.appendRow(bottom_row)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                if self.flag_folders:
                    parent_row.setEditable(True)
                else:
                    parent_row.setEditable(False)
                self.add_data_parent_item(parent_row, data[key])
                node.appendRow(parent_row)
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            if not self.flag_child_editable:
                bottom_row.setEditable(False)
            node.appendRow(bottom_row)

    def add_data_to_display_old(self, node=None, data=[]):
        # example data ['file',{'folder ':['file']}]
        if not node:
            # node = self.rootnode
            node = self.tree_model
        else:
            if isinstance(node, str):
                node = self.find_node(node)
                node = self.tree_model.itemFromIndex(node)
        if isinstance(data, list):
            for values in data:
                self.add_data_to_display(values, node)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                if self.flag_folders:
                    parent_row.setEditable(False)
                node.appendRow(parent_row)
                self.add_data_to_display(data[key], parent_row)
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            if not self.flag_child_editable:
                bottom_row.setEditable(False)
            node.appendRow(bottom_row)
        # old, did not always work, as it always required values as list
        # for values in data:
        #     """if its [{key:[val]}]"""
        #     if isinstance(values, dict):
        #         for keys in values:
        #             parent_row = QStandardItem()
        #             parent_row.setText(keys)
        #             if self.flag_folders:
        #                 parent_row.setEditable(False)
        #             node.appendRow(parent_row)
        #             self.add_data(parent_row, values[keys])
        #         """if its {key:value}"""
        #     elif isinstance(data, dict):
        #         parent_row = QStandardItem()
        #         parent_row.setText(values)
        #         bottom_row = QStandardItem()
        #         bottom_row.setText(data[values])
        #         if self.flag_folders:
        #             parent_row.setEditable(False)
        #         if not self.flag_child_editable:
        #             bottom_row.setEditable(False)
        #         parent_row.appendRow(bottom_row)
        #         node.appendRow(parent_row)
        #         """if its just string"""
        #     else:
        #         bottom_row = QStandardItem()
        #         bottom_row.setText(values)
        #         if not self.flag_child_editable:
        #             bottom_row.setEditable(False)
        #         node.appendRow(bottom_row)

    # def fill_dict_from_model(self, parent_index, root_list):
    #     current_row_folder = {}
    #     sub_level_list = []
    #     ix = None
    #     for i in range(self.tree_model.rowCount(parent_index)):
    #         ix = self.tree_model.index(i, 0, parent_index)
    #         self.fill_dict_from_model(ix, sub_level_list)
    #         current_row_folder[parent_index.data()] = sub_level_list
    #     if current_row_folder:
    #         root_list.append(current_row_folder)
    #     else:
    #         root_list.append(parent_index.data())
    #
    # def get_data(self):
    #     # stuff are in a list, where file should be strings, while folders should be dict
    #     root_list = list()
    #     for i in range(self.tree_model.rowCount()):
    #         row_index = self.tree_model.index(i, 0)
    #         self.fill_dict_from_model(row_index, root_list)
    #     return root_list
    """below is combined version of 2 above. should mostly work"""
    def get_data_single_column(self, parent_index=None, root_list=None):
        # stuff are in a list, where simple row should be strings, while folders should be dict
        if parent_index:
            row_range = self.tree_model.rowCount(parent_index)
        else:
            row_range = self.tree_model.rowCount()
        current_row_folder = {}
        values_list = []
        ix = None
        for i in range(row_range):
            if parent_index:
                row_index = self.tree_model.index(i, 0, parent_index)
            else:
                row_index = self.tree_model.index(i, 0)
            self.get_data(row_index, values_list)
            if parent_index:
                current_row_folder[parent_index.data()] = values_list
        if current_row_folder:
            root_list.append(current_row_folder)
        else:
            if parent_index:
                root_list.append(parent_index.data())
            else:
                return values_list

    """below should work if there are more columns. then it should return values in a list. if only 1 column in row,
     its string"""
    def get_data(self, parent_index=None, root_list=None, remove_title=False):
        """stuff are in a list, where file should be strings, while folders should be dict
        should return something like [row0, row1, {row2:[row20, row21]},[row3column0, row3column1]}"""
        if parent_index:
            if isinstance(parent_index, QStandardItem):
                parent_index = self.tree_model.indexFromItem(parent_index)
            row_range = self.tree_model.rowCount(parent_index)
            col_range = self.tree_model.columnCount(parent_index)
        else:
            row_range = self.tree_model.rowCount()
            col_range = self.tree_model.columnCount()
        current_row_folder = {}
        rows_list = []
        ix = None
        for i in range(row_range):
            cols_list = []
            for ii in range(col_range):
                if parent_index:
                    row_index = self.tree_model.index(i, ii, parent_index)
                else:
                    row_index = self.tree_model.index(i, ii)
                self.get_data(row_index, cols_list)
            # here i would have to check if other columns are empty, if yes, turn cols_list into a string
            for vals in cols_list:
                if not vals:
                    cols_list.remove(vals)
            if len(cols_list) == 1:
                rows_list.append(cols_list[0])
            else:
                rows_list.append(cols_list)
            if parent_index:
                current_row_folder[parent_index.data()] = rows_list
        if current_row_folder:
            # this should work if entered deeper level
            root_list.append(current_row_folder)
        else:
            if parent_index:
                # this should also work if entered deeper level
                root_list.append(parent_index.data())
            else:
                # this should return final data
                if remove_title:
                    for i in range(len(rows_list)):
                        if isinstance(rows_list[i], dict):
                            for title in rows_list[i]:
                                rows_list[i] = rows_list[i][title]
                return rows_list

    def find_node(self, node_to_find, parent_index=None):
        if parent_index:
            row_range = self.tree_model.rowCount(parent_index)
        else:
            row_range = self.tree_model.rowCount()
        for i in range(row_range):
            if parent_index:
                row_index = self.tree_model.index(i, 0, parent_index)
            else:
                row_index = self.tree_model.index(i, 0)
            if row_index.data() == node_to_find:
                found_node = self.tree_model.item(row_index.row(), row_index.column(),)
                return row_index
            search_node = self.find_node(node_to_find, row_index)
            if search_node:
                return search_node
    # def get_data_fromtreeview(self, row=0, item=None):
    #     return
    #     # cant figure this out, above methods are working nice
    #     # since here single item does not seem to have access to siblings, i need to check while i have full access
    #     #  to children. so if has children, go over children, if there is another nested inside, recurrence by that
    #     temp_list = []
    #     while True:
    #         if not item:
    #             item = self.tree_model.item(row, 0)
    #         print(item.text())
    #         if item.hasChildren():
    #             rowB = 0
    #             temp_Blist = []
    #             while item.child(rowB,0):
    #                 if item.child(rowB,0).hasChildren():
    #                     self.get_data_fromtreeview(row, item.child(rowB, 0))
    #                 else:
    #                     temp_Blist.append(item.child(rowB,0).text())
    #                 rowB += 1
    #             temp_dict = {item.text(): temp_Blist}
    #             temp_list.append(temp_dict)
    #         else:
    #             temp_list.append(item.text())
    #         row += 1
    #         item = self.tree_model.item(row, 0)
    #         if not item:
    #             break
    #     return temp_list


    def selected_element(self):
        """selected_index is indexes of items, not items themselfs
        so go over list, change each element to appropiate item and if 1 item in list, return that item
        otherwise return list of items - QStandartItem
        problem - if more than 1 columns, its always list, as each each column in rows is separate item"""
        # version 2
        selected_index = self.selectedIndexes()
        if selected_index:
            for idx in range(len(selected_index)):
                if self.flag_search:
                    selected_index[idx] = self.sorting.mapToSource(selected_index[idx])
                selected_index[idx] = self.tree_model.itemFromIndex(selected_index[idx])
            if len(selected_index) == 1:
                return selected_index[0]
            else:
                return selected_index
        else:
            return None
        # version 1
        # selected_index = self.selectedIndexes()
        # if selected_index:
        #     for selected in selected_index:
        #         if self.flag_search:
        #                 source_index = self.sorting.mapToSource(selected_index[0])
        #             else:
        #                 source_index = selected_index[0]
        #
        #     return self.tree_model.itemFromIndex(source_index)
        # else:
        #     return None

    def select_element(self, text=str, inverse_selection=False):
        if text:
            element_index = self.find_node(text)
            if inverse_selection:
                row_count = self.tree_model.rowCount()
                for idx in range(row_count):
                    if self.tree_model.index(idx,0) != element_index:
                        self.selectionModel().select(self.tree_model.index(idx,0), QtCore.QItemSelectionModel.Select)
            else:
                self.selectionModel().select(element_index, QtCore.QItemSelectionModel.Select)


    def new_prep_data_to_add(self, data=[], return_val=[]):
        """turn data, list of dictionaries and strings, into list of standard items with nexted items"""
        if not isinstance(data, list):
            data = [data]
        for values in data:
            if isinstance(values, dict):
                for key in values:
                    templist = []
                    parent_row = QStandardItem()
                    parent_row.setText(key)
                    parent_row.setWhatsThis(self.parent_tag)
                    if self.flag_folders:
                        parent_row.setEditable(True)
                    else:
                        parent_row.setEditable(False)
                    self.new_prep_data_to_add(values[key], templist)
                    # TODO probably, this append row does not append 1 after the other, but next to, as in columns, not rows
                    for item in templist:
                        parent_row.appendRow(item)
                    return_val.append(parent_row)
            else:
                bottom_row = QStandardItem()
                bottom_row.setText(values)
                return_val.append(bottom_row)
                if not self.flag_child_editable:
                    bottom_row.setEditable(False)
        # return return_val
        # elif isinstance(data, dict):
        #     for key in data:
        #         parent_row = QStandardItem()
        #         parent_row.setText(key)
        #         final_items_to_add.append(parent_row)
        #         if self.flag_folders:
        #             parent_row.setEditable(True)
        #         else:
        #             parent_row.setEditable(False)
        #         parent_row.setWhatsThis(self.parent_tag)
        #         self.add_data_parent_item(parent_row, data[key])
        # else:
        #     """if data is just string"""
        #     bottom_row = QStandardItem()
        #     bottom_row.setText(data)
        #     if not self.flag_child_editable:
        #         bottom_row.setEditable(False)
        #     final_items_to_add.append(bottom_row)

    def new_insert_data(self, values, item_above_insert=None):
        rows_to_insert = []
        self.new_prep_data_to_add(values, rows_to_insert)
        if not item_above_insert:
            selected_item = self.selected_element()
        else:
            selected_item = item_above_insert
        if selected_item:
            insert_position = selected_item.row()
            branch_to_insert = selected_item.parent()
            # branch_to_insert = self.tree_model.itemFromIndex(parent)
            # selected_item = self.currentIndex()
            # update_position = selected_item.row()
            # selected_parent = selected_item.parent()
            # branch_to_insert = self.tree_model.itemFromIndex(selected_parent)
            if not branch_to_insert:
                branch_to_insert = self.tree_model
            rows_to_insert.reverse()
            for item in rows_to_insert:
                branch_to_insert.insertRow(insert_position, item)
        else:
            self.add_data_to_display(values)

    def add_leaves_TODO(self, iid, values, update_flag=True):  # dodawanie podgałęzi do istniejącej gałęzi drzewa
        # need to find proper parent iid as root branches are normatl, but leaves are generated with index and parent name
        #might cause problems when some leaves are similar
        value = None
        if iid != '':
            iid = self.find_iid(iid)
            if not iid:
                print('something wrong with find iid - return none type')
                return
        currentleaves = self.treeview.get_children(iid)
        # if not currentleaves:
        #     print('test')
        if update_flag:
            value = None
            for i in currentleaves: #first clean all leaves
                self.treeview.delete(i)
            for i in values:
                # if i not in currentleaves:
                #     self.treeview.insert(iid, 'end', i, text=i)  # dodawanie podgałęzi drzewa
                # else:   #update branch
                self.treeview.insert(iid, 'end', i, text=i)  # dodawanie podgałęzi drzewa
        else:
            index = len(currentleaves) + 1
            for i in values:
                if i not in currentleaves:
                    value = self.treeview.insert(iid, 'end', i + '_' + iid + '_' + str(index), text=i)  # dodawanie podgałęzi drzewa
                    index += 1
        if value:
            return value

    def add_folder(self, folder_name):
        """add 1 item, which suppose to contains more items"""
        node = self.selected_element()
        if node is None:
            node = self.tree_model
        else:
            if isinstance(node, str):
                node = self.find_node(node)
                node = self.tree_model.itemFromIndex(node)
            if node.whatsThis() != 'folder':
                node = node.parent()
        new_folder = QStandardItem()
        new_folder.setText(folder_name)
        new_folder.setEditable(True)
        new_folder.setWhatsThis('folder')
        node.appendRow(new_folder)

    def add_leaf(self, list_of_strings_to_insert_in_row=[], row=None, parent=None, row_height=0):
        new_leaves = []
        for text in list_of_strings_to_insert_in_row:
            new_leaf = QStandardItem(text)
            new_leaf.setEditable(True)
            if row_height > 0:
                new_leaf.setSizeHint(QSize(0, row_height))
            new_leaves.append(new_leaf)
        if parent:
            if row:
                parent.insertRow(row, new_leaves)
            else:
                parent.appendRow(new_leaves)
        else:
            if row:
                self.tree_model.insertRow(row, new_leaves)
            else:
                self.tree_model.appendRow(new_leaves)
        """used to add single leaves with specific id, to be able to delete later without searching"""
        # return self.treeview.insert(parent_id, 'end', code, text=txt)

    def change_row_height(self, new_height, child=None):
        if child is None:
            item = self.tree_model
        else:
            item = child
        for idx in range(item.rowCount()):
            if child is not None:
                iitem = item.child(idx)
            else:
                iitem = self.tree_model.item(idx)
            if iitem.child(0, 0):
                self.change_row_height(new_height, iitem)
            iitem.setSizeHint(QSize(0, new_height))
        # for idx in range(self.tree_model.rowCount()):
        #     item = self.tree_model.item(idx)
        #     item.setSizeHint(QSize(0, new_height))
    def change_row_color(self, item, color):
        if color == 'good':
            item.setBackground(QBrush(QColor("#ffffff")))
        else:
            item.setBackground(QBrush(QColor("#ff8080")))
    def update_leaf(self, new_text):
        """just change displayed text"""
        selected_item = self.tree_model.itemFromIndex(self.currentIndex())
        selected_item.setText(new_text)
        return

    #
    # def update_branch(self, new_data):
    #     """update entire branch, so delete it and put anew. new_data should be a dictionary"""
    #     item = self.treeview.selection()[0]
    #     if item:
    #         for items in self.treeview.get_children(item):
    #             self.treeview.delete(items)
    #         for values in new_data:
    #             self.treeview.insert(item, 'end', text=values)
    #
    # def add_data(self, data, branch=''):
    #     """data here might be a dictionary with lists and stuff, so it needs to be smart"""
    #     if isinstance(data, dict):
    #         for keys in data:
    #             if isinstance(data[keys], list):
    #                 new_branch = self.treeview.insert(branch, 'end', text=keys)
    #                 # for value in data[keys]:
    #                 self.add_data(data[keys], new_branch)
    #             elif isinstance(data[keys], dict):
    #                 temp = list(data[keys].keys())
    #                 new_branch = self.treeview.insert(branch, 'end', text=temp[0])
    #                 for value in data[keys]:
    #                     self.add_data(data[keys][value], new_branch)
    #     else:
    #         for values in data:
    #             if isinstance(values, list):
    #                 new_branch = self.treeview.insert(branch, 'end', text=values)
    #                 for value in values:
    #                     self.add_data(value, new_branch)
    #             elif isinstance(values, dict):
    #                 temp = list(values.keys())
    #                 new_branch = self.treeview.insert(branch, 'end', text=temp[0])
    #                 for value in values:
    #                     self.add_data(values[value], new_branch)
    #             else:
    #                 self.treeview.insert(branch, 'end', text=values)
    #
    # def gather_data(self, branch=''):
    #     temp_list = []
    #     for leaves in self.treeview.get_children(branch):
    #         if not self.treeview.get_children(leaves):
    #             temp_list.append(self.treeview.item(leaves)['text'])
    #         else:
    #             temp_dict = {self.treeview.item(leaves)['text']: self.gather_data(leaves)}
    #             # temp_dict[leaves] = self.gather_data(leaves)
    #             temp_list.append(temp_dict)
    #     return temp_list
    #
    # def on_tv_select(self, event):
    #     # curItem = self.treeview.focus()  # element, który otrzymał fokus
    #     # curItem = self.treeview.item(curItem)["text"]
    #     # print(curItem)
    #     # print(self.treeview.item(curItem)["text"])  # wyświetlanie w konsoli tekstu z klikniętego elementu drzewa
    #     # global currentSelectedItem
    #     #        problem is, there is more then 1 tree in app, so if not main tree is clicked, global is overwritten with
    #     #        data from some other tree and button details will return error. need to check if this tree is from global pool
    #     if self.treeview.heading('#0')['text'] in ["Adventures", "Events", "Fetishes", "Items", "Locations", "Monsters",
    #                                                "Perks", "Skills", "Main Game"]:
    #         # if self.treeview.parent(self.treeview.focus()):
    #         #     curItem = self.treeview.item(self.treeview.parent(self.treeview.focus()))['text']
    #         if self.treeview.heading('#0')['text'] == 'Main Game':
    #             GlobalVariables.currentSelectedItem['type'] = self.treeview.item(self.find_root_parent(self.treeview.focus()))['text'] + '-addition'
    #         else:
    #             GlobalVariables.currentSelectedItem['type'] = self.treeview.heading('#0')['text']
    #         # GlobalVariables.currentSelectedItem['data'] = self.treeview.focus()
    #         GlobalVariables.currentSelectedItem['text'] = self.treeview.item(self.treeview.focus())["text"]
    #         GlobalVariables.currentSelectedItem['id'] = self.treeview.focus()
    #         GlobalVariables.currentSelectedItem['tags'] = self.treeview.item(self.treeview.focus())["tags"]
    #         # GlobalVariables.currentSelectedItem = self.treeview.heading('#0')['text'] + '_' + curItem
    #
    #     # msb.showinfo("Info", self.treeview.item(curItem)["text"])
    #     # print(self.treeview.selection())
    #     # if len(self.treeview.selection()) > 0:
    #     #     self.treeview.selection_remove(self.treeview.selection()[0])
    #     #     print(self.treeview.selection())
    #
    # def hide_tree(self):
    #     self.treeview.grid_forget()
    #     self.sb_treeview.grid_forget()
    #     if self.flag_search:
    #         self.label_search.grid_forget()
    #         self.entry_search.grid_forget()
    #
    # def show_tree(self):
    #     self.treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NSEW)
    #     self.sb_treeview.grid(row=self.row_placement+1, column=self.col_placement+1, sticky=tk.NS + tk.E)
    #     if self.flag_search:
    #         self.label_search.grid(row=self.row_placement, column=self.col_placement, columnspan=self.col_span_placement, sticky='W')
    #         self.entry_search.grid(row=self.row_placement, column=self.col_placement, columnspan=self.col_span_placement, sticky='E')
    #
    def delete_leaf(self, branch=None):
        # if branch is a string, need to find the item, if a list, will have compare by texts and remove
        if branch:
            if isinstance(branch, str):
                branch = [self.find_node(branch)]
        else:
            # branch = self.currentIndex()
            branch = self.selectedIndexes()
        # just in case, make list of texts and parents, if one of items is nested, then only by parent can we separate
        leaves_to_delete_by_text = []
        for leaf in branch:
            # if treeview has more column, then selecting one row selects all columns as well, each being separate item
            # so here it gathers all items, each having row the same. need to check if row is same, skip
            if leaves_to_delete_by_text:
                if leaves_to_delete_by_text[-1].row() == leaf.row():
                    continue
            leaves_to_delete_by_text.append(self.tree_model.itemFromIndex(leaf))
        for leaf in leaves_to_delete_by_text:
            item = self.tree_model.indexFromItem(leaf)
            # item_in_sort = self.sorting.mapToSource(item)
            self.tree_model.removeRow(item.row(), item.parent())
            # self.sorting.removeRow(item_in_sort.row(),item_in_sort.parent())
        return

    def delete_with_backup(self):
        # this is list of indexes for selected items
        items_to_delete = self.selectedIndexes()
        # item_to_delete = self.find_node('sub value 3')
        # this data is for any childs of selected item
        leaves_data = []
        # if selected 1 or more items, always put in list
        items_list = []
        for item in items_to_delete:
            if item.child(0, 0).data():
                self.get_data(item, leaves_data)
                leaves_data = leaves_data[0][item.data()]
            delete_element_data = {'index': item.row(), 'parent': item.parent(),
                                   'text': item.data(), 'leaves':leaves_data}
            items_list.append(delete_element_data)
        self.delete_leaf(items_to_delete)
        if items_list:
            if len(self.back_up_deleted) > 10:
                self.back_up_deleted.pop(0)
            self.back_up_deleted.append(items_list)
        return
    #
    # def delete_with_backup(self):
    #     this is for single item
    #     item_to_delete = self.currentIndex()
    #     temp = self.selectedIndexes()
    #     # item_to_delete = self.find_node('sub value 3')
    #     leaves_data = []
    #     if item_to_delete.child(0,0).data():
    #         self.get_data(item_to_delete, leaves_data)
    #         # leaves_data = leaves_data[0][item_to_delete.data()]
    #     delete_element_data = {'index': item_to_delete.row(), 'parent': item_to_delete.parent(),
    #                             'text': item_to_delete.data(), 'leaves':leaves_data}
    #     if delete_element_data:
    #         if len(self.back_up_deleted) > 5:
    #             self.back_up_deleted.pop(0)
    #         self.back_up_deleted.append(delete_element_data)
    #     self.delete_leaf(item_to_delete)
    #     return

    def restore_deleted(self, paste=False):
        if self.back_up_deleted:
            items_to_restore = self.back_up_deleted.pop(-1)
            for item in items_to_restore:
                if paste:
                    branch_to_insert = self.tree_model.itemFromIndex(self.currentIndex())
                    item['index'] = 0
                    if not branch_to_insert.isEditable():
                        # if not editable, then its a file, cannot paste into file.
                        branch_to_insert = self.tree_model.itemFromIndex(self.currentIndex().parent())
                        if not branch_to_insert.parent():
                            # if there is no parent, its root item.
                            branch_to_insert = self.tree_model
                else:
                    branch_to_insert = self.tree_model.itemFromIndex(item['parent'])
                new_item = QStandardItem()
                new_item.setText(item['text'])
                new_item.setEditable(False)
                if not branch_to_insert:
                    branch_to_insert = self.tree_model
                branch_to_insert.insertRow(item['index'], new_item)
                if item['leaves']:
                    self.add_data(item['leaves'], new_item)
    # def restore_deleted(self):
    #     if self.back_up_deleted:
    #         element_to_restore = self.back_up_deleted.pop(-1)
    #         branch_to_insert = self.tree_model.itemFromIndex(element_to_restore['parent'])
    #         new_item = QStandardItem()
    #         new_item.setText(element_to_restore['text'])
    #         new_item.setEditable(False)
    #         if not branch_to_insert:
    #             branch_to_insert = self.tree_model
    #         branch_to_insert.insertRow(element_to_restore['index'], new_item)
    #         if element_to_restore['leaves']:
    #             self.add_data(new_item, element_to_restore['leaves'])
    #         return
    # # TODO add moving selection up and down
    # def move_up(self):
    #     return
    # #     selected_items = self.treeview.selection_get()
    # def move_down(self):
    #     return
    def insert_row(self, new_rows):
        # might need to add if for values, as they probably should be standardItems
        rows_to_insert = []
        for row in new_rows:
            newr = QStandardItem(row)
            rows_to_insert.append(newr)
        selected_item = self.currentIndex()
        update_position = selected_item.row()
        selected_parent = selected_item.parent()
        branch_to_insert = self.tree_model.itemFromIndex(selected_parent)
        if not branch_to_insert:
            branch_to_insert = self.tree_model
        rows_to_insert.reverse()
        for item in rows_to_insert:
            branch_to_insert.insertRow(update_position, item)

    def clear_tree(self):
        row_count = self.tree_model.rowCount()
        self.tree_model.removeRows(0, row_count)
        # for leaves in range(row_count,-1,-1):
        #     self.tree_model.remov

    def change_title(self, new_title):
        self.title = new_title
        self.setHeaderHidden(False)
        self.tree_model.setHorizontalHeaderLabels([new_title])
    #
    # def filter_leafs(self, item, branch):
    #     # it might works, returning from reversed hidden leafs. this way we put them back in order they were taken away
    #     # if not work, will have to change to one list as main, filter it and copy to display
    #     # branches = self.treeview.get_children()
    #     for leaves in branch:
    #         leafs = list(self.treeview.get_children(leaves))
    #         if leafs:
    #             self.filter_leafs(item, self.treeview.get_children(leaves))
    #             if not self.treeview.get_children(leaves):
    #                 # if no more leaves in this branch, hide branch too. we can only interact with leaves.
    #                 # print('koniec lisci na = ' + leaves)
    #                 item_parent = self.treeview.parent(leaves)
    #                 item_no = self.treeview.index(leaves)
    #                 self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': leaves})
    #                 self.treeview.detach(leaves)
    #     # for branch in branches:
    #     #     leafs = list(self.treeview.get_children(branch))
    #     #
    #     #     for leaf in leafs:
    #     #
    #     #         lvl_2_leaf = self.treeview.get_children(leaf)
    #     #         if lvl_2_leaf:
    #     #             print(leaf)
    #     #     if "_" not in leaves:
    #     #         continue
    #         else:
    #             if item.lower() not in leaves[:leaves.find('_')].lower():
    #                 item_parent = self.treeview.parent(leaves)
    #                 item_no = self.treeview.index(leaves)
    #                 self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': leaves})
    #                 self.treeview.detach(leaves)
    #     # check if branch still has leaves. if not, hide branch
    #
    #         # if item.lower() not in branch[:branch.find('_')].lower():
    #         #     item_parent = self.treeview.parent(branch)
    #         #     item_no = self.treeview.index(branch)
    #         #     self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': branch})
    #         #     self.treeview.detach(branch)
    #
    # def display_all(self):
    #     for hiddenleafs in reversed(self.hidden_leafs):
    #         self.treeview.reattach(hiddenleafs['itemID'], hiddenleafs['itemParent'], hiddenleafs['itemNumber'])
    #
    # def selected_item(self, value='name'):
    #     # curItem = self.treeview.selection()  # element, który otrzymał fokus
    #     if self.treeview.selection():
    #         cur_item = self.treeview.selection()[0]
    #     else:
    #         cur_item = ''
    #     cur_item_name = self.treeview.item(cur_item)["text"]
    #     if value == 'name':
    #         return cur_item_name
    #     else:
    #         return cur_item
    def search_value(self, name='', index='', mode=''):
        # self.setModel(self.sorting)
        search_val = self.entry_search.text()
        self.sorting.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.sorting.setFilterWildcard(search_val)
        # self.setModel(self.tree_model)
        return

    def open_tree(self):
        self.expandAll()

    def find_root_parent(self, child=QStandardItem):
        # child here should be item from index so QStandardItem
        parent = child.parent()
        if parent:
            higher_parent = self.find_root_parent(parent)
            return higher_parent
        else:
            return child

    def current_folder(self):
        leaf_index = self.currentIndex()
        if self.tree_model.itemFromIndex(leaf_index).isEditable():
            return self.tree_model.itemFromIndex(leaf_index)
        else:
            return self.tree_model.itemFromIndex(leaf_index).parent()

    def set_up_widget(self, outside_layout, insert_for_options=False):
        if insert_for_options:
            outside_layout.insertLayout(outside_layout.count() - 1, self.layout)
        else:
            outside_layout.addLayout(self.layout)
        outside_layout.setAlignment(self, QtCore.Qt.AlignCenter)
    #

    #
    # def on_click(self, event):
    #     return
    #     #     """Set tag for selected datasets."""
    #     #
    #     # # # Remove 'plotted' tag if existent
    #     # # if 'plotted' in self.treeview.item(self.treeview.selection())['tags']:
    #     # #     self.treeview.item(self.treeview.selection(), tags=())
    #     # #
    #     # # # Select only items that have no children
    #     # # elif not self.treeview.get_children(self.treeview.selection()):
    #     #     self.treeview.item(self.treeview.selection(), tags='plotted')
    #     # # self.treeview.column('#0', anchor=tk.E)
    # def cancel_selection(self):
    #     self.treeview.selection_remove(self.treeview.selection()[0])

class MultiList_old:
    def __init__(self, master=None, field_name=None, tooltip_text=None,
                 field_options=[], template_name=None):
        self.title = field_name
        self.type = 'multilist'
        self.template_name = template_name
        # self.label_custom = custom_label(master, field_name) # cant make doouble click on label, switched to button
        self.label_custom = CustomButton(master, field_name)
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.custom_layout.addWidget(self.label_custom)
        self.label_custom.setToolTip(tooltip_text)
        # self.label_custom.change_position('center')
        # self.label_custom.button_transform()
        self.field_frame = master
        """ there should be 3 versions:
        unique - can add multiple items, cannot duplicate
        multi_item - items can be duplicated
        single_item - can only select 1 item  
        multi_item means if it should be possible to select one item multiple times. this means separate treeview
         for adding items."""
        if 'single_item' in field_options:
            self.version = 'single'
            self.displayed_value_field = SimpleEntryDisplay(self)
            self.custom_layout.addWidget(self.displayed_value_field)
            self.displayed_value_field.doubleClicked.connect(self.on_double_click_edit_field)
            # self.field.bind("<Double-Button-1>", self.on_double_click_edit_field)
            # self.field.grid(row=1, column=0, columnspan=3)
        else:
            self.version = 'unique'
            self.final_data_tree = ElementsList(master, field_name)
            self.custom_layout.addWidget(self.final_data_tree)
            # self.set_row_size(6)
            # self.data_tree = ElementsList(self, 3, 0, 'Double Click to Edit', colspan=3, treeview_height=3)
            # self.data_tree.treeview.configure(selectmode='extended')
            # self.data_tree.treeview.bind("<Double-Button-1>", self.on_double_click_edit_field)
            # self.data_tree.treeview.unbind("<Delete>")
            # self.data_tree.treeview.unbind("<Control_L>")

        self.addition = False
        if field_options:
            if 'addition' in field_options:
                self.addition = True

        # self.set_row_size(5)
        # self.tree_options_choose = ElementsList(self, 1, 1, field_name, 2, delete_flag=False)
        # self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
        # self.label_custom.doubleClicked.connect(self.edit_value)
        # self.label_custom.doubleClicked.connect(self.edit_value)
        self.label_custom.clicked.connect(self.edit_value)


    def set_val(self, values):
        """might not be good, because it only adds. when updating, it should first clear val."""
        if self.version != 'single':
            for value in values:
                if value:
                    self.data_tree.add_branch(value, [], update_flag=False)
        else:
            self.var.set(values)
    def get_val(self, temp_dict_container=None):
        if self.version == 'single':
            temp = self.var.get()
            if 'CLICK' in temp:
                temp = ''
        else:
            temp = []
            all_vals = self.data_tree.treeview.get_children()
            for value in all_vals:
                temp.append(self.data_tree.treeview.item(value)['text'])
            # this might be important if there is a problem with values returned somewhere
            # if len(temp) == 0:
            #     temp.append('')
        if temp_dict_container is not None:
            temp_dict_container[self.title] = temp
        else:
            return temp

    def clear_val(self):
        # self.selected_items.clear()
        self.var.set('no values')
        if self.version != 'single':
            for item in self.data_tree.treeview.get_children():
                self.data_tree.treeview.delete(item)
    def on_double_click_edit_field(self, event):
        # TODO this looks exactly the same?
        if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
            if self.addition:
                flag = True
            else:
                flag = False
        else:
            flag = True
        if flag:
            if self.version == 'single':
                Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
                                                   structure_data=self.get_val(), structure_link=self)
            else:
                region = self.data_tree.treeview.identify("region", event.x, event.y)
                if region == "heading":
                    Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
                                                       structure_data=self.get_val(), structure_link=self)
    def edit_value(self):
        print('test edit value miltilist)')
        item_win = QtWidgets.QDialog(parent=self.field_frame)
        item_visual = MainGameItemsInNewWindow()
        item_visual.setupUi(Dialog=item_win)
        item_win.show()

    def set_up_widget(self, outside_layout):
        outside_layout.addLayout(self.custom_layout)
# below is newer version
class MultiListDisplay:
    """there are 3 types of data here.
    single item - only 1 item allowed, so it could be an input field, where you can type text to autosearch for
     available values from main multilist, also limited to type of items to seachs
    several items - this allows several items with no duplication. will be a treeview and maybe add something like above
    multiple items - several with duplicates."""
    def __init__(self, master=None, field_name=None,
                 field_data=None, template_name=None, main_data_treeview=None):
        self.title = field_name
        self.type = 'multilist'
        self.template_name = template_name
        self.label_custom = CustomLabel(master, field_name)
        # self.label_custom = custom_button(master, field_name)
        self.addition = False
        self.row_size = 4
        # field_data = {'options':['unique'], 'choices':['Items']}
        if 'options' in field_data:
            if 'single_item' in field_data['options']:
                self.version = 'single'
                self.row_size = 1
            elif 'unique' in field_data['options']:
                self.version = 'unique'
            else:
                self.version = 'multi_item'
            if 'addition' in field_data['options']:
                self.addition = True
        if 'tooltip' in field_data:
            self.label_custom.setToolTip(field_data['tooltip'])
        # self.label_custom.change_position('center')
        # self.label_custom.button_transform()
        self.field_frame = master
        self.selection_type = ''
        if 'choices' in field_data:
            for choice in field_data['choices']:
                if 'Items' in choice:
                    self.selection_type += 'Items'
                elif 'Skills' in choice:
                    self.selection_type += 'Skills'
                elif 'Perks' in choice:
                    self.selection_type += 'Perks'
                elif 'Monsters' in choice:
                    self.selection_type += 'Monsters'
                elif 'Fetishes' in choice:
                    self.selection_type += 'Fetishes Addictions'
                else:
                    self.selection_type += choice
                    # self.selection_type += field_data['choices'][0]
        """
        unique - can add multiple items, cannot duplicate
        multi_item - items can be duplicated
        single_item - can only select 1 item  
        """
        self.custom_layout = QtWidgets.QVBoxLayout()
        if self.version == 'single':
            self.final_data = SimpleEntry(master, None, class_connector=self, main_data_treeview=main_data_treeview)
            self.label_custom.change_position('R')
            self.custom_layout = QtWidgets.QHBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        elif self.version == 'unique':
            # self.final_data = QtWidgets.QListWidget(parent=master)
            self.final_data = UniqueView(master=master, class_connector=self, data_treeview=main_data_treeview)
            self.label_custom.change_position('center')
        else:
            self.final_data = UniqueView(master=master, class_connector=self, data_treeview=main_data_treeview)
            # self.final_data = ElementsList(master, field_name, class_connector=self)
            self.label_custom.change_position('center')
        self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addWidget(self.final_data)
        self.custom_layout.addStretch(1)

            # self.set_row_size(6)
            # self.data_tree = ElementsList(self, 3, 0, 'Double Click to Edit', colspan=3, treeview_height=3)
            # self.data_tree.treeview.configure(selectmode='extended')
            # self.data_tree.treeview.bind("<Double-Button-1>", self.on_double_click_edit_field)
            # self.data_tree.treeview.unbind("<Delete>")
            # self.data_tree.treeview.unbind("<Control_L>")
        # self.label_custom.doubleClicked.connect(self.edit_value)
        # self.label_custom.doubleClicked.connect(self.edit_value)
        # self.label_custom.clicked.connect(self.edit_value)

    def set_val(self, values):
        if self.version == 'single':
            self.final_data.set_val(values)
        else:
            if self.version == 'unique':
                if isinstance(values, str):
                    values = [values]
                current_count = self.final_data.tree_model.rowCount()
                current_values = []
                for idx in range(current_count):
                    item = self.final_data.tree_model.item(idx)
                    current_values.append(item.text())
                for value in values:
                    if value not in current_values:
                        # self.final_data.addItem(value)
                        self.final_data.add_data('',[value])
            #             TODO maybe add warning?
            else:
                self.final_data.add_data(data=[values])
    def get_val(self, temp_dict_container=None):
        # if self.version == 'single':
        #     temp = self.var.get()
        #     if 'CLICK' in temp:
        #         temp = ''
        # else:
        #     temp = []
        #     all_vals = self.data_tree.treeview.get_children()
        #     for value in all_vals:
        #         temp.append(self.data_tree.treeview.item(value)['text'])
        #     # this might be important if there is a problem with values returned somewhere
        #     # if len(temp) == 0:
        #     #     temp.append('')
        if self.version == 'single':
            return_data = self.final_data.get_val()
        elif self.version == 'unique':
            return_data = []
            current_count = self.final_data.count()
            for idx in range(current_count):
                item = self.final_data.item(idx)
                return_data.append(item.text())
        else:
            return_data = self.final_data.get_data()
        if temp_dict_container is not None:
            temp_dict_container[self.title] = return_data
        else:
            return return_data

    def clear_val(self):
        if self.version == 'unique':
            self.final_data.clear()
        else:
            self.final_data.clear_val()
    def hide(self):
        self.label_custom.hide()
        self.final_data.hide()
    def show(self):
        self.final_data.show()
        if self.label_custom.text():
            self.label_custom.show()
    def edit_value(self):
        # this is for editing in new window
        print('test edit value miltilist)')
        item_win = QtWidgets.QDialog(parent=self.field_frame)
        item_visual = MainGameItemsInNewWindow()
        item_visual.setupUi(Dialog=item_win)
        item_win.show()
    def destroy(self):
        # self.custom_layout.deleteLater()
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            if temp:
                if not isinstance(temp, QtWidgets.QSpacerItem):
                    temp.widget().deleteLater()
        self.custom_layout.deleteLater()
    def set_up_widget(self, outside_layout, insert_for_options=False):
        if insert_for_options:
            outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
        else:
            outside_layout.addLayout(self.custom_layout)
        outside_layout.setAlignment(self.custom_layout,QtCore.Qt.AlignCenter)

# this is multilist with main item data.
class Main_MultiList:
    def __init__(self, master=None, field_name=None, tooltip_text=None, main_label_flag=True):
        # super().__init__(master=master, label=field_name, tooltip=tooltip_text, label_pos=label_position)
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.title = field_name
        self.type = 'main_multilist'
        self.edit_flag = False
        select_mode = 'extended'
        # self.field_frame = master
        """ this contains necessary mod and game items. so Always display treeview and need
         to be updated when adding new mod items."""
        # self.label_info = custom_label(master, 'NOT Editing')
        self.label_info_flag = main_label_flag
        if self.label_info_flag:
            self.label_info = CustomButton(None, 'NOT Editing', class_connector=self)
            self.label_info.setMinimumWidth(150)
            self.label_info.clicked.connect(self.add_item_to_multilist)
            # self.label_info.change_position('center')
            self.label_info.setToolTip('CTRL A or double click lowest element to add to selected field')
            self.custom_layout.addWidget(self.label_info)

        self.main_data = ElementsList(None, 'Available element', search_field=True,
                                      folders=False, all_edit=False, class_connector=self)
        # """testing global model"""
        # self.main_data.tree_model = GlobalVariables.Glob_Var.main_game_tree_model
        # self.main_data.sorting = GlobalVariables.Glob_Var.main_game_sorting
        # self.main_data.setModel(GlobalVariables.Glob_Var.main_game_sorting)
        # """"""
        self.main_data.entry_search.type = ''
        self.main_data.set_up_widget(self.custom_layout)
        self.connected_multilist = None
        self.main_data.shortcut_restore.disconnect()
        self.main_data.shortcut_cut.disconnect()
        self.main_data.shortcut_paste.disconnect()
        self.main_data.doubleClicked.connect(self.add_item_to_multilist)
        # # if 'multi_item' in field_options:
        # #     self.version = 'multi'
        # #     self.set_row_size(6)
        # # elif 'single_item' in field_options:
        # #     self.version = 'single'
        # #     select_mode = 'browse'
        # # else:
        # #     self.version = 'unique'
        # #     self.set_row_size(6)
        # #  if 'multi_item' in field_options:
        # #     self.multi_value_flag = True
        # # else:
        # #     self.multi_value_flag = False
        # # if 'single_item' in field_options:
        # #     self.single_item = 1
        # #     select_mode = 'browse'
        # # else:
        # #     self.single_item = 0
        # # self.self_button_main = tk.Button(self, text='Click to select values', wraplength=150, textvariable=self.var,
        # #                                   command=self.open_tree)
        # self.self_button_main = tk.Button(self, wraplength=150, textvariable=self.var,
        #                                   command=self.open_tree, text='test')
        # self.self_button_main.grid(row=1, column=0, columnspan=3)
        # self.button_done = tk.Button(self, text='DONE', command=self.done)
        #
        # """for multi and unique, need buttons to add and delete"""
        # self.button_select = tk.Button(self, text='ADD', command=self.add_multi_value)
        # # self.button_select.grid(row=rowposition, column=colpos)
        # self.button_clear = tk.Button(self, text='DELETE', command=self.delete_multi_value)
        # self.button_clear.bind('<Shift-c>', self.clear_selected)

        # self.list = otherFunctions.getListOptions(list_path, 'multi')
        # self.var.set('CLICK')
        # if 'search' in field_options:
        #     flag_search_field = True
        # else:
        #     flag_search_field = False
        # self.tree_options_choose = ElementsList(self, 2, 1, field_name, 2,flag_search_field, delete_flag=False)
        # # masterWun, rowPos, colPos, listTitle, colspan = 1,
        # for element_name in self.list:
        #     self.tree_options_choose.add_branch(element_name, self.list[element_name])
        # self.tree_options_choose.hide_tree()
        # self.tree_options_choose.treeview.configure(selectmode=select_mode)
        # self.tree_options_choose.treeview.tag_configure('selected', background='red')
        # if self.multi_value_flag:
        #     self.tree_options_choose.treeview.bind('<s>', lambda event: self.add_multi_value())
        # else:
        #     self.tree_options_choose.treeview.bind('<s>', lambda event: self.select_row())
        # self.selected_items = []
        # self.get, self.set = self.var.get, self.var.set
        # self.display_flag = True
        # # if self.multi_value_flag:
        # # temp = tk.StringVar
        # # self.self_button_main.configure(textvariable=temp)
        # # self.button_select['text'] = 'Add'
        # # self.button_select.configure(command=self.add_multi_value)
        # # self.button_clear['text'] = 'Delete'
        # # self.button_clear.configure(command=self.delete_multi_value)
        # self.data_tree = ElementsList(self, 3, 1, 'Selected values', colspan=2, treeview_height=3)
        # self.data_tree.treeview.configure(selectmode='extended')
        # self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
        # # if self.version == 'single':
        # self.data_tree.hide_tree()
        # self.data_tree_display = False
        # # else:
        # if self.version != 'single':
        #     self.tree_options_choose.treeview.bind('<a>', lambda event: self.add_multi_value())
        # for key in self.list.keys():
        #     if 'Mod' in key:
        #         # if key.find('/') < 0:
        #         #     end_val_index = len(key)
        #         # else:
        #         #     end_val_index = key.find('/')
        #         element = key[4:]
        #         GlobalVariables.multi_lists_to_refresh[element].append(self.tree_options_choose)
        #         break
        # self.shortcut_restore = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+a'), self)
        # self.shortcut_restore.activated.connect(self.add_value_to_field)
        self.data_for_display = GlobalVariables.Glob_Var.display_elements_game_and_mod
        """scene source is for functions jump to scene. if its 'current', get data from global-template-field.
        if something else, it should be event name, get also from global-events-search for scenes"""
        self.scene_source = ''
        self.current_scene_list = None

    def set_up_widget(self, outside_layout, if_grid=None):
        if if_grid:
            if self.label_info_flag:
                outside_layout.addWidget(self.label_info, 7, 0, 1, 1)
            outside_layout.addWidget(self.main_data, 8, 0, 1, 1)
        else:
            outside_layout.addLayout(self.custom_layout)
    def connect_multilist(self, multilist):
        # print('connected')
        if self.connected_multilist == multilist or multilist == self:
            # print('clicked same field again')
            return
        self.connected_multilist = multilist
        self.main_data.clear_tree()
        if self.label_info_flag:
            self.label_info.update_label('Add to ' + self.connected_multilist.title)
        self.filter_options(multilist.selection_type)
        # print(multilist.selection_type)
    def disconnect_multilist(self):
        # print('disconnected')
        if self.connected_multilist:
            self.connected_multilist = None
            if self.label_info_flag:
                self.label_info.update_label('NOT editing')
            # self.label_info.clicked.disconnect()
            # self.main_data.restore_deleted()
            self.filter_options([])

    def filter_options(self, filter):
        """filter should be list of values"""
        # self.main_data.clear_tree()
        """here add scenes. this might change while making events, so it needs to reload each time."""
        """and the rest of stuff"""
        if 'Scenes' in filter:
            """if current, need to load from field in templates"""
            if self.scene_source == 'current' or 'current' in filter:
                # if self.connected_multilist.selection_type:
                #     if self.connected_multilist.selection_type == 'EventText':
                #         element = 'Events'
                #     else:
                #         element = 'Monsters'
                list_of_dictionary_scenes = self.current_scene_list
                # list_of_dictionary_scenes = GlobalVariables.Glob_Var.access_templates['Events'].frame_fields['EventText'].get_val()
                # list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates[element].frame_fields[self.connected_multilist.selection_type].get_val()
                scene_names = []
                for scene in list_of_dictionary_scenes:
                    for a in list_of_dictionary_scenes[scene]:
                        scene_names.append(list_of_dictionary_scenes[scene][a]['NameOfScene'])
                self.main_data.add_data(scene_names)
                # GlobalVariables.Glob_Var.access_templates['Events'].frame_fields[]
            # if flag_current_event:
            #     if self.event == 'EventText':
            #         element = 'Events'
            #     else:
            #         element = 'Monsters'
            #     # list_of_dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
            #     list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates[element].frame_fields[self.event].get_val()
                """else, load from data in modvar from event set in scene source"""
                return
            else:
                """problem is, here i got only event title, so i need to search both events and monsters"""
                if self.scene_source in list(GlobalVariables.Mod_Var.mod_data['Events'].keys()):
                    """search events. there scenes are in EventText"""
                    scenes_list = GlobalVariables.Mod_Var.mod_data['Events'][self.scene_source]['EventText']
                    """each scene is a dictionary of keys, where we need NameOfScene"""
                    scene_names = []
                    for scene in scenes_list:
                        scene_names.append(scene['NameOfScene'])
                    self.main_data.add_data(scene_names)
                elif self.scene_source in list(GlobalVariables.Mod_Var.mod_data['Monsters'].keys()):
                    """search events. there scenes are in EventText"""
                    scenes_list = GlobalVariables.Mod_Var.mod_data['Events']['lossScenes'] + GlobalVariables.Mod_Var.mod_data['Events']['victoryScenes']
                    """each scene is a dictionary of keys, where we need lossScenes and victoryScenes"""
                    scene_names = []
                    for scene in scenes_list:
                        scene_names.append(scene['NameOfScene'])
                    self.main_data.add_data(scene_names)
        elif 'speaker' in filter:
            speaker_data = GlobalVariables.Glob_Var.access_templates['Events'].frame_fields['Speakers'].get_val()
            speaker_display_list = []
            for speaker in speaker_data:
                speaker_id = QtGui.QStandardItem(str(speaker_data.index(speaker)))
                speaker_id.setEditable(False)
                speaker_name = QtGui.QStandardItem(speaker['name'])
                speaker_name.setEditable(False)
                speaker_display_list.append([speaker_id, speaker_name])
            for speakers in speaker_display_list:
                self.main_data.tree_model.appendRow(speakers)
        elif 'limit' in filter:
            """this is probably limit skills, i hope there is not much else like this"""
            data_to_filter = copy.copy(self.data_for_display['Skills'])
            skills_to_display = []
            """first get rid of skills from mod"""
            for idx in range(len(data_to_filter)):
                check_skill = data_to_filter.pop(0)
                if isinstance(check_skill, dict):
                    """this is main game dictionary"""
                    for skills in check_skill:
                        filtered_data = {skills: self.skill_limit(check_skill)}
                        skills_to_display.append(filtered_data)
                else:
                    if check_skill in GlobalVariables.Mod_Var.mod_data['Skills']:
                        mod_data = GlobalVariables.Mod_Var.mod_data['Skills'][check_skill]
                        if mod_data['targetType'] == 'single':
                            skills_to_display.append(check_skill)

            self.main_data.add_data(skills_to_display)
        else:
            for element in self.data_for_display:
                # if isinstance(element, str):
                #     value_to_check = element
                # else:
                #     value_to_check = list(element.keys())[0]
                if element in filter:
                    self.main_data.add_data(self.data_for_display[element])
    def add_item_to_multilist(self):
        selected_item = self.main_data.selected_element()
        if selected_item and self.connected_multilist:
            if not selected_item.child(0, 0):
                # selected_item_type = self.main_data.find_root_parent(selected_item)
                # selection_type = self.connected_multilist.selection_type
                # if selection_type:
                #     if selected_item_type.text() in selection_type:
                self.connected_multilist.set_val(selected_item.text())
    def block_tree(self, parent_index=None):
        # need to block edition on all fields
        if parent_index:
            row_range = self.main_data.tree_model.rowCount(parent_index)
        else:
            row_range = self.main_data.tree_model.rowCount()
        for i in range(row_range):
            if parent_index:
                row_index = self.main_data.tree_model.index(i, 0, parent_index)
            else:
                row_index = self.main_data.tree_model.index(i, 0)
            item = self.main_data.tree_model.itemFromIndex(row_index)
            item.setEditable(False)
            self.block_tree(row_index)
    def add_main_game_items(self):
        main_game_items = GlobalVariables.Glob_Var.main_game_items
        for element in main_game_items:
            if main_game_items[element]:  #{Adventures:[stuff]}
                if element == 'Fetishes':
                    self.data_for_display['Fetish'] = [{'main game': list(main_game_items[element]['Fetish'].keys())}]
                    self.data_for_display['Addiction'] = [{'main game': list(main_game_items[element]['Addiction'].keys())}]

                else:
                    self.data_for_display[element] = [{'main game': main_game_items[element]['path']}]
                # self.data_for_display
                # self.main_data.add_data(data=temp_dict)
        for trigger in GlobalVariables.Glob_Var.line_trigger_display_data:
            self.data_for_display[trigger] = GlobalVariables.Glob_Var.line_trigger_display_data[trigger]
        # self.main_data.add_data(data=[GlobalVariables.Glob_Var.line_trigger_display_data])
        skill_tags = ["Sex","displaySex","Ass","displayAss","Breasts","displayBreasts","Mouth","displayMouth",
                      "Seduction","displaySeduction","Magic","displayMagic","Pain","displayPain","Holy","displayHoly",
                      "Unholy","displayUnholy"]
        self.data_for_display['Sesitivity'] = skill_tags
        """old approach below"""
        # self.main_data.add_data(data='MOD')
        # # self.main_data.add_data(data={'MOD':[{'Events':[]},{'Items':[]},{'Fetishes':[]},{'Monsters':[]},{'Perks':[]},{'Skills':[]}]})
        # main_game_items = GlobalVariables.Glob_Var.main_game_items
        # for element in main_game_items:
        #     if main_game_items[element]:
        #         if element == 'Fetishes':
        #             temp_dict = {'Fetish': list(main_game_items[element]['Fetish'].keys()),
        #                          'Addiction': list(main_game_items[element]['Addiction'].keys())}
        #
        #         else:
        #             temp_dict = {element: main_game_items[element]['path']}
        #         self.main_data.add_data(data=[temp_dict])
        # """for main multilist, it works different. it is created one, loads main game items"""
        # for element in GlobalVariables.Glob_Var.lineTriggers:
        #     temp_dict = {element:GlobalVariables.Glob_Var.lineTriggers[element]['path']}
        #     self.main_data.add_data(data=[temp_dict])
        # self.main_data.add_data(data=[GlobalVariables.Glob_Var.line_trigger_display_data])
        # skill_tags = ["Sex","displaySex","Ass","displayAss","Breasts","displayBreasts","Mouth","displayMouth",
        #               "Seduction","displaySeduction","Magic","displayMagic","Pain","displayPain","Holy","displayHoly",
        #               "Unholy","displayUnholy"]
        # self.main_data.add_data(data={'Sesitivity': skill_tags})
        self.filter_options([])
        return
    def get_val(self, temp_dict_container=None):
        if self.version == 'single':
            temp = self.var.get()
            # for some reason i had to lower text here?
            # temp = self.var.get().lower()
            if temp in ['click', 'CLICK']:
            # if 'click' in temp or 'CLICK' in temp:
                temp = ''
        # elif self.version == 'multi':
        #     all_vals = self.data_tree.treeview.get_children()
        #     for value in all_vals:
        #         temp.append(self.data_tree.treeview.item(value)['text'])
        else:
            temp = []
            all_vals = self.data_tree.treeview.get_children()
            for value in all_vals:
                temp.append(self.data_tree.treeview.item(value)['text'])
            # this might be important if there is a problem with values returned somewhere
            # if len(temp) == 0:
            #     temp.append('')
        if temp_dict_container is not None:
            temp_dict_container[self.title] = temp
        else:
            return temp

    def clear_val(self):
        # self.selected_items.clear()
        self.var.set('Click to select values')
        # self.clear_all_tags()
        # if self.single_item != 0:
        #     self.single_item = 1
        for item in self.tree_options_choose.treeview.selection():
            self.tree_options_choose.treeview.selection_remove(item)
        if self.version != 'single':
            for item in self.data_tree.treeview.get_children():
                self.data_tree.treeview.delete(item)
        if self.data_tree_display:
            self.data_tree.hide_tree()
            self.data_tree_display = False

    def open_tree(self):
        # print('open tree')
        if self.version != 'single':
            self.button_select.grid(row=1, column=1, sticky='W')
            self.button_clear.grid(row=1, column=1)
        else:
            selected_values = self.var.get()
            if len(selected_values) > 1:
                # self.selected_items = selected_values[1:]
                self.select_loaded_items_in_tree()
                # self.selected_items = selected_values[1:]
        self.button_done.grid(row=1, column=1, sticky='E')

        # print(selected_values)
        self.self_button_main.grid_forget()
        """for now, there is usually word OPTION in list, so if there is something selected, there will be more
        since selectItemsInTree removes items from the selectedItems list, i make a temp list, which later is
        copied back to the selectedItems. This way, when done selecting, no need to iterate over the treeview to check
        for selected tags, just display what is in the selectedItems list"""
        # if len(selected_values) > 1:
        #     self.selected_items = selected_values[1:]
        #     self.select_loaded_items_in_tree()
        #     self.selected_items = selected_values[1:]
        # self.var.set("                                                              ")
        # self.button_select.grid(row=self.start_pos_row, column=self.start_pos_col)
        # self.button_clear.grid(row=self.start_pos_row, column=self.start_pos_col + 1)
        # self.button_done.grid(row=self.start_pos_row, column=self.start_pos_col + 2)

        self.tree_options_choose.show_tree()
    def select_row_notused(self):
        # print(self.selected_items)
        # print(str(self.treeview_optionstochoose.treeview.selection()))
        user_selection = self.tree_options_choose.treeview.selection()
        if not user_selection:
            return
        if self.single_item and len(user_selection)>1:
            messagebox.showwarning('only single item allowed','Please select only 1 item', parent=self)
            return
        for selection in user_selection:
            if self.tree_options_choose.treeview.get_children(selection) == ():
                if 'selected' in self.tree_options_choose.treeview.item(selection)['tags']:
                    self.tree_options_choose.treeview.item(selection, tags=())
                    self.selected_items.remove(self.tree_options_choose.treeview.item(selection)['text'])
                    if self.single_item > 0:
                        self.single_item -= 1
                else:
                    if self.single_item > 0:
                        if self.single_item > 1:
                            messagebox.showwarning('only single item allowed', 'Please deselect previous item', parent=self)
                            return
                        else:
                            self.single_item += 1
                    self.tree_options_choose.treeview.item(selection, tags='selected')
                    self.selected_items.append(self.tree_options_choose.treeview.item(selection)['text'])
        self.tree_options_choose.treeview.selection_remove(self.tree_options_choose.treeview.selection()[0])
        # self.edit_flag = True
    def clear_selected_notused(self):
        warning = messagebox.askokcancel("clearing all items", "are you sure you want to clear all selected items?", parent=self)
        if warning:
            self.clear_all_tags()
            self.selected_items = []
            if self.single_item > 1:
                self.single_item -= 1
        self.edit_flag = True
    def clear_all_tags_notused(self, item=''):
        # print('test')
        # recursivly search all lowest levels and clear tags
        children_of_item = self.tree_options_choose.treeview.get_children(item)
        if children_of_item:
            for items in children_of_item:
                self.clear_all_tags(items)
        else:
            if 'selected' in self.tree_options_choose.treeview.item(item)['tags']:
                self.tree_options_choose.treeview.item(item, tags=())

    def select_loaded_items_in_tree(self, item_to_check=''):
        children_of_item = self.tree_options_choose.treeview.get_children(item_to_check)
        if children_of_item:
            for items in children_of_item:
                if self.select_loaded_items_in_tree(items):
                    break
        else:
            if self.var.get() == self.tree_options_choose.treeview.item(item_to_check)['text']:
                # self.tree_options_choose.treeview.item(item_to_check, tags='selected')
                self.tree_options_choose.treeview.selection_set(item_to_check)
                return True
            # for select in self.selected_items:
                # if select == self.tree_options_choose.treeview.item(item_to_check)['text']:
                #     self.tree_options_choose.treeview.item(item_to_check, tags='selected')
                #     self.selected_items.remove(select)
                # break

    def done(self):
        # print('done in multilist')
        """similar to function display list tree, hide buttons, treeview and update main button with items from
        selectedItems list"""
        # self.treeview_optionstochoose.hide_tree()
        # print(str(self.treeview_optionstochoose.treeview.item(self.treeview_optionstochoose.treeview.focus())))
        if self.tree_options_choose.treeview.winfo_ismapped():
            self.tree_options_choose.hide_tree()
        if self.version != 'single':
            self.button_select.grid_forget()
            self.button_clear.grid_forget()
        self.button_done.grid_forget()
        if self.version == 'single':
            selected = self.tree_options_choose.selected_item()
            if selected:
                self.var.set(selected)
                self.self_button_main['text'] = 'Selected ' + selected
        # if self.edit_flag:
        #         if self.multi_value_flag:
        #             for branches in self.data_tree.treeview.get_children():
        #                 self.selected_items.append(self.data_tree.treeview.item(branches)['text'])
        #         final_selected_items_text = 'OPTIONS'
        #         for selected in self.selected_items:
        #             final_selected_items_text += '\n' + selected
        #         self.var.set(final_selected_items_text)
        self.self_button_main.grid(row=1, column=0, columnspan=2)
        # self.edit_flag = False

    def display(self, flag=None):
        if flag is None:
            flag = self.display_flag
        if flag:
            self.grid_forget()
            self.tree_options_choose.hide_tree()
            self.display_flag = False
        else:
            self.self_button_main.grid(row=self.start_pos_row + 1, column=0, columnspan=2)
            self.tree_options_choose.show_tree()
            self.display_flag = True

    def add_multi_value(self, single_value=None):
        if not self.data_tree_display:
            self.data_tree.show_tree()
            self.data_tree_display = True
        if single_value:
            item = single_value
        else:
            item = self.tree_options_choose.selected_item()
        if self.version == 'unique':
            temp = self.tree_options_choose.selected_item(value='name')
            current_added = self.data_tree.treeview.get_children()
            for child in current_added:
                if temp == self.data_tree.treeview.item(child)['text']:
                    messagebox.showerror('Only unique', 'No points in repeating data', parent=self)
                    return
            # if temp in current_added:
        # self.data_tree.add_branch(item, [], update_flag=False)
        self.data_tree.add_leaves_simple('', [item])
        # self.data_tree.add_leaf('', self.tree_options_choose.selected_item(value='code'), item)
        self.edit_flag = True
        # self.selected_items.append(item)
        # self.var.set(self.var.get() + '\n' + item)

    def delete_multi_value(self):
        item = self.data_tree.selected_item(value='code')
        self.data_tree.delete_leaf(item)
        if not self.data_tree.treeview.get_children():
            self.data_tree.hide_tree()
        self.edit_flag = True

    def deselect_row(self):
        self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])

    def update_with_mod_item(self, mod_tree_copy):
        """new approach - spread it to appropiate branches"""
        """remake list of dictionaries into dictionary"""
        temp_dict = {}
        for mod_item in mod_tree_copy:
            if isinstance(mod_item, str):
                continue
            for item in mod_item:
                if item in 'Adventures Locations':
                    continue
                temp_dict[item] = mod_item[item]
        for mod_item in temp_dict:
            for i in temp_dict[mod_item]:
                self.data_for_display[mod_item].insert(-1,i)
        # for idx in range(self.main_data.tree_model.rowCount()):
        #     element = self.main_data.tree_model.item(idx)
        #     for items in temp_dict:
        #         """if found something in mod data, append it to element on last place, before main game branch"""
        #         if items == element.text():
        #             self.main_data.new_insert_data(temp_dict[items], element.child(0, 0))

            # if element.text() in mod_tree_copy:

        # """just add copy of mod elements to mod item - first item in tree."""
        # mod_item = self.main_data.tree_model.item(0, 0)
        # mod_tree_copy.pop(4)
        # mod_tree_copy.pop(0)
        # for idx in range(len(mod_tree_copy), 0, -1):
        #     if isinstance(mod_tree_copy[idx-1], str):
        #         mod_tree_copy.pop(idx-1)
        # self.main_data.add_data(mod_tree_copy, mod_item, True)


        # for idx in range(mod_item.rowCount()):
        #     if mod_item.child(idx).text() == item_type:
        #         if add:
        #             new_item = QStandardItem(item_name)
        #             mod_item.child(idx).appendRow(new_item)
        #         else:
        #             item_type_item = mod_item.child(idx)
        #             for idxy in range(item_type_item.rowCount()):
        #                 if item_type_item.child(idx).text() == item_name:
        #                     item_type_item.takeChild(idxy)
        #                     break
        #     else:
        #         item_parent = QStandardItem(item_type)
        #         new_item = QStandardItem(item_name)
        #         item_parent.appendRow(new_item)
        #         mod_item.appendRow(item_parent)
        #
        #
        # return

    def reload_mod_data(self, new_values):
        mod_item = self.main_data.tree_model.item(0, 0)
        mod_item.removeRows(0,mod_item.rowCount())
        new_values_without_empty_items = {}
        for items in new_values:

            if len(new_values[items]) > 0:
                new_values_without_empty_items[items] = new_values[items]
        self.main_data.add_data_to_display(new_values_without_empty_items, mod_item)

    def skill_limit(self, main_game_dict):
        """this checks over dictionary of main game skills, if skill has targetType single"""
        temp_data = []
        for item_list in main_game_dict:
            for a in main_game_dict[item_list]:
                if isinstance(a, dict):
                    for b in a:
                        temp_data_2 = {b: self.skill_limit(a)}
                        temp_data.append(temp_data_2)
                else:
                    if a in GlobalVariables.Mod_Var.mod_data['Skills']:
                        data = GlobalVariables.Mod_Var.mod_data['Skills'][a]
                    elif a in GlobalVariables.Glob_Var.main_game_items['Skills']['data']:
                        data = GlobalVariables.Glob_Var.main_game_items['Skills']['data'][a]
                    if data['targetType'] == 'single':
                        temp_data.append(a)
        return temp_data


    def add_folder(self, parent_text, folder_name):
        # mod_item = self.main_data.tree_model.item(0, 0)
        node = self.main_data.find_node(parent_text, self.main_data.tree_model.index(0, 0))
        if node == None:
            node = self.main_data.tree_model.item(0, 0)
            add_element_type_as_folder = QStandardItem()
            add_element_type_as_folder.setText(parent_text)
            add_element_type_as_folder.setEditable(True)
            add_element_type_as_folder.setWhatsThis('folder')
            node.appendRow(add_element_type_as_folder)
            node = add_element_type_as_folder
        else:
            node = self.main_data.tree_model.itemFromIndex(node)
            if node.whatsThis() != 'folder':
                node = node.parent()
        new_folder = QStandardItem()
        new_folder.setText(folder_name)
        new_folder.setEditable(True)
        new_folder.setWhatsThis('folder')
        node.appendRow(new_folder)

    def hide(self):
        self.main_data.clear_tree()
        self.main_data.hide()
        self.main_data.entry_search.hide()

    def show(self):
        self.main_data.show()
        self.main_data.entry_search.show()
# class MultiListDisplay(SimpleField):
#     def __init__(self, master=None, field_name=None, tooltip_text=None, label_position='U',
#                  field_options=[], template_name=None):
#         super().__init__(master=master, label=field_name, tooltip=tooltip_text, label_pos=label_position)
#         self.var = tk.StringVar()
#         self.title = field_name
#         self.type = 'multilist'
#         self.template_name = template_name
#         # self.field_frame = master
#         """ there should be 3 versions:
#         unique - can add multiple items, cannot duplicate
#         multi_item - items can be duplicated
#         single_item - can only select 1 item
#         multi_item means if it should be possible to select one item multiple times. this means separate treeview
#          for adding items."""
#         if 'single_item' in field_options:
#             self.version = 'single'
#             self.field = tk.Entry(self, textvariable=self.var, state='disabled')
#             self.field.bind("<Double-Button-1>", self.on_double_click_edit_field)
#             self.field.grid(row=1, column=0, columnspan=3)
#         else:
#             self.version = 'unique'
#             self.set_row_size(6)
#             self.data_tree = ElementsList(self, 3, 0, 'Double Click to Edit', colspan=3, treeview_height=3)
#             self.data_tree.treeview.configure(selectmode='extended')
#             self.data_tree.treeview.bind("<Double-Button-1>", self.on_double_click_edit_field)
#             self.data_tree.treeview.unbind("<Delete>")
#             self.data_tree.treeview.unbind("<Control_L>")
#
#         self.addition = False
#         if field_options:
#             if 'addition' in field_options:
#                 self.addition = True
#         self.set_row_size(5)
#         # self.tree_options_choose = ElementsList(self, 1, 1, field_name, 2, delete_flag=False)
#         # masterWun, rowPos, colPos, listTitle, colspan = 1,
#         self.get, self.set = self.var.get, self.var.set
#         # self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
#
#     def set_val(self, values):
#         """might not be good, because it only adds. when updating, it should first clear val."""
#         if self.version != 'single':
#             for value in values:
#                 if value:
#                     self.data_tree.add_branch(value, [], update_flag=False)
#         else:
#             self.var.set(values)
#     def get_val(self, temp_dict_container=None):
#         if self.version == 'single':
#             temp = self.var.get()
#             if 'CLICK' in temp:
#                 temp = ''
#         else:
#             temp = []
#             all_vals = self.data_tree.treeview.get_children()
#             for value in all_vals:
#                 temp.append(self.data_tree.treeview.item(value)['text'])
#             # this might be important if there is a problem with values returned somewhere
#             # if len(temp) == 0:
#             #     temp.append('')
#         if temp_dict_container is not None:
#             temp_dict_container[self.title] = temp
#         else:
#             return temp
#
#     def clear_val(self):
#         # self.selected_items.clear()
#         self.var.set('no values')
#         if self.version != 'single':
#             for item in self.data_tree.treeview.get_children():
#                 self.data_tree.treeview.delete(item)
#     def on_double_click_edit_field(self, event):
#         # TODO this looks exactly the same?
#         if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
#             if self.addition:
#                 flag = True
#             else:
#                 flag = False
#         else:
#             flag = True
#         if flag:
#             if self.version == 'single':
#                 Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
#                                                    structure_data=self.get_val(), structure_link=self)
#             else:
#                 region = self.data_tree.treeview.identify("region", event.x, event.y)
#                 if region == "heading":
#                     Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
#                                                        structure_data=self.get_val(), structure_link=self)
#
#     def bind_control(self, binding):
#         if binding:
#             self.data_tree.bind('<Double-Button-1>', self.on_double_click_edit_field)
#         else:
#
#             self.data_tree.unbind('<Double-Button-1>')
#
# class MultiList(SimpleField):
#     def __init__(self, master=None, field_name=None, tooltip_text=None, label_position='U',
#                  list_path=['test'], field_options=[]):
#         super().__init__(master=master, label=field_name, tooltip=tooltip_text, label_pos=label_position)
#         self.start_pos_row = 1
#         self.start_pos_col = 1
#         self.var = tk.StringVar()
#         self.title = field_name
#         self.type = 'multilist'
#         self.edit_flag = False
#         select_mode = 'extended'
#         # self.field_frame = master
#         """ there should be 3 versions:
#         unique - can add multiple items, cannot duplicate
#         multi_item - items can be duplicated
#         single_item - can only select 1 item
#         multi_item means if it should be possible to select one item multiple times. this means separate treeview
#          for adding items."""
#
#         self.set_row_size(2)
#         if 'multi_item' in field_options:
#             self.version = 'multi'
#             self.set_row_size(6)
#         elif 'single_item' in field_options:
#             self.version = 'single'
#             select_mode = 'browse'
#         else:
#             self.version = 'unique'
#             self.set_row_size(6)
#         #  if 'multi_item' in field_options:
#         #     self.multi_value_flag = True
#         # else:
#         #     self.multi_value_flag = False
#         # if 'single_item' in field_options:
#         #     self.single_item = 1
#         #     select_mode = 'browse'
#         # else:
#         #     self.single_item = 0
#         # self.self_button_main = tk.Button(self, text='Click to select values', wraplength=150, textvariable=self.var,
#         #                                   command=self.open_tree)
#         self.self_button_main = tk.Button(self, wraplength=150, textvariable=self.var,
#                                           command=self.open_tree, text='test')
#         self.self_button_main.grid(row=1, column=0, columnspan=3)
#         self.button_done = tk.Button(self, text='DONE', command=self.done)
#
#         """for multi and unique, need buttons to add and delete"""
#         self.button_select = tk.Button(self, text='ADD', command=self.add_multi_value)
#         # self.button_select.grid(row=rowposition, column=colpos)
#         self.button_clear = tk.Button(self, text='DELETE', command=self.delete_multi_value)
#         # self.button_clear.bind('<Shift-c>', self.clear_selected)
#
#         self.list = otherFunctions.getListOptions(list_path, 'multi')
#         self.var.set('CLICK')
#         if 'search' in field_options:
#             flag_search_field = True
#         else:
#             flag_search_field = False
#         self.tree_options_choose = ElementsList(self, 2, 1, field_name, 2,flag_search_field, delete_flag=False)
#         # masterWun, rowPos, colPos, listTitle, colspan = 1,
#         for element_name in self.list:
#             self.tree_options_choose.add_branch(element_name, self.list[element_name])
#         self.tree_options_choose.hide_tree()
#         self.tree_options_choose.treeview.configure(selectmode=select_mode)
#         # self.tree_options_choose.treeview.tag_configure('selected', background='red')
#         # if self.multi_value_flag:
#         #     self.tree_options_choose.treeview.bind('<s>', lambda event: self.add_multi_value())
#         # else:
#         #     self.tree_options_choose.treeview.bind('<s>', lambda event: self.select_row())
#         # self.selected_items = []
#         self.get, self.set = self.var.get, self.var.set
#         self.display_flag = True
#         # if self.multi_value_flag:
#         # temp = tk.StringVar
#         # self.self_button_main.configure(textvariable=temp)
#         # self.button_select['text'] = 'Add'
#         # self.button_select.configure(command=self.add_multi_value)
#         # self.button_clear['text'] = 'Delete'
#         # self.button_clear.configure(command=self.delete_multi_value)
#         self.data_tree = ElementsList(self, 3, 1, 'Selected values', colspan=2, treeview_height=3)
#         self.data_tree.treeview.configure(selectmode='extended')
#         self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
#         # if self.version == 'single':
#         self.data_tree.hide_tree()
#         self.data_tree_display = False
#         # else:
#         if self.version != 'single':
#             self.tree_options_choose.treeview.bind('<a>', lambda event: self.add_multi_value())
#         for key in self.list.keys():
#             if 'Mod' in key:
#                 # if key.find('/') < 0:
#                 #     end_val_index = len(key)
#                 # else:
#                 #     end_val_index = key.find('/')
#                 element = key[4:]
#                 GlobalVariables.multi_lists_to_refresh[element].append(self.tree_options_choose)
#                 break
#
#     def set_val(self, values):
#         if self.version != 'single':
#             for value in values:
#                 if value:
#                     self.data_tree.add_branch(value, [], update_flag=False)
#                     if not self.data_tree_display:
#                         self.data_tree.show_tree()
#                         self.data_tree_display = True
#         else:
#             # temp = 'OPTIONS'
#             # if not isinstance(values, list):
#             #     values = [values]
#             # for value in values:
#             #     if value == '':
#             #         continue
#             #     temp = temp + '\n' + value
#             self.var.set(values)
#             self.self_button_main['text'] = 'Selected ' + values
#     def get_val(self, temp_dict_container=None):
#         if self.version == 'single':
#             temp = self.var.get()
#             # for some reason i had to lower text here?
#             # temp = self.var.get().lower()
#             if temp in ['click', 'CLICK']:
#             # if 'click' in temp or 'CLICK' in temp:
#                 temp = ''
#         # elif self.version == 'multi':
#         #     all_vals = self.data_tree.treeview.get_children()
#         #     for value in all_vals:
#         #         temp.append(self.data_tree.treeview.item(value)['text'])
#         else:
#             temp = []
#             all_vals = self.data_tree.treeview.get_children()
#             for value in all_vals:
#                 temp.append(self.data_tree.treeview.item(value)['text'])
#             # this might be important if there is a problem with values returned somewhere
#             # if len(temp) == 0:
#             #     temp.append('')
#         if temp_dict_container is not None:
#             temp_dict_container[self.title] = temp
#         else:
#             return temp
#
#     def clear_val(self):
#         # self.selected_items.clear()
#         self.var.set('Click to select values')
#         # self.clear_all_tags()
#         # if self.single_item != 0:
#         #     self.single_item = 1
#         for item in self.tree_options_choose.treeview.selection():
#             self.tree_options_choose.treeview.selection_remove(item)
#         if self.version != 'single':
#             for item in self.data_tree.treeview.get_children():
#                 self.data_tree.treeview.delete(item)
#         if self.data_tree_display:
#             self.data_tree.hide_tree()
#             self.data_tree_display = False
#
#     def open_tree(self):
#         # print('open tree')
#         if self.version != 'single':
#             self.button_select.grid(row=1, column=1, sticky='W')
#             self.button_clear.grid(row=1, column=1)
#         else:
#             selected_values = self.var.get()
#             if len(selected_values) > 1:
#                 # self.selected_items = selected_values[1:]
#                 self.select_loaded_items_in_tree()
#                 # self.selected_items = selected_values[1:]
#         self.button_done.grid(row=1, column=1, sticky='E')
#
#         # print(selected_values)
#         self.self_button_main.grid_forget()
#         """for now, there is usually word OPTION in list, so if there is something selected, there will be more
#         since selectItemsInTree removes items from the selectedItems list, i make a temp list, which later is
#         copied back to the selectedItems. This way, when done selecting, no need to iterate over the treeview to check
#         for selected tags, just display what is in the selectedItems list"""
#         # if len(selected_values) > 1:
#         #     self.selected_items = selected_values[1:]
#         #     self.select_loaded_items_in_tree()
#         #     self.selected_items = selected_values[1:]
#         # self.var.set("                                                              ")
#         # self.button_select.grid(row=self.start_pos_row, column=self.start_pos_col)
#         # self.button_clear.grid(row=self.start_pos_row, column=self.start_pos_col + 1)
#         # self.button_done.grid(row=self.start_pos_row, column=self.start_pos_col + 2)
#
#         self.tree_options_choose.show_tree()
#     def select_row_notused(self):
#         # print(self.selected_items)
#         # print(str(self.treeview_optionstochoose.treeview.selection()))
#         user_selection = self.tree_options_choose.treeview.selection()
#         if not user_selection:
#             return
#         if self.single_item and len(user_selection)>1:
#             messagebox.showwarning('only single item allowed','Please select only 1 item', parent=self)
#             return
#         for selection in user_selection:
#             if self.tree_options_choose.treeview.get_children(selection) == ():
#                 if 'selected' in self.tree_options_choose.treeview.item(selection)['tags']:
#                     self.tree_options_choose.treeview.item(selection, tags=())
#                     self.selected_items.remove(self.tree_options_choose.treeview.item(selection)['text'])
#                     if self.single_item > 0:
#                         self.single_item -= 1
#                 else:
#                     if self.single_item > 0:
#                         if self.single_item > 1:
#                             messagebox.showwarning('only single item allowed', 'Please deselect previous item', parent=self)
#                             return
#                         else:
#                             self.single_item += 1
#                     self.tree_options_choose.treeview.item(selection, tags='selected')
#                     self.selected_items.append(self.tree_options_choose.treeview.item(selection)['text'])
#         self.tree_options_choose.treeview.selection_remove(self.tree_options_choose.treeview.selection()[0])
#         # self.edit_flag = True
#     def clear_selected_notused(self):
#         warning = messagebox.askokcancel("clearing all items", "are you sure you want to clear all selected items?", parent=self)
#         if warning:
#             self.clear_all_tags()
#             self.selected_items = []
#             if self.single_item > 1:
#                 self.single_item -= 1
#         self.edit_flag = True
#     def clear_all_tags_notused(self, item=''):
#         # print('test')
#         # recursivly search all lowest levels and clear tags
#         children_of_item = self.tree_options_choose.treeview.get_children(item)
#         if children_of_item:
#             for items in children_of_item:
#                 self.clear_all_tags(items)
#         else:
#             if 'selected' in self.tree_options_choose.treeview.item(item)['tags']:
#                 self.tree_options_choose.treeview.item(item, tags=())
#
#     def select_loaded_items_in_tree(self, item_to_check=''):
#         children_of_item = self.tree_options_choose.treeview.get_children(item_to_check)
#         if children_of_item:
#             for items in children_of_item:
#                 if self.select_loaded_items_in_tree(items):
#                     break
#         else:
#             if self.var.get() == self.tree_options_choose.treeview.item(item_to_check)['text']:
#                 # self.tree_options_choose.treeview.item(item_to_check, tags='selected')
#                 self.tree_options_choose.treeview.selection_set(item_to_check)
#                 return True
#             # for select in self.selected_items:
#                 # if select == self.tree_options_choose.treeview.item(item_to_check)['text']:
#                 #     self.tree_options_choose.treeview.item(item_to_check, tags='selected')
#                 #     self.selected_items.remove(select)
#                 # break
#
#     def done(self):
#         # print('done in multilist')
#         """similar to function display list tree, hide buttons, treeview and update main button with items from
#         selectedItems list"""
#         # self.treeview_optionstochoose.hide_tree()
#         # print(str(self.treeview_optionstochoose.treeview.item(self.treeview_optionstochoose.treeview.focus())))
#         if self.tree_options_choose.treeview.winfo_ismapped():
#             self.tree_options_choose.hide_tree()
#         if self.version != 'single':
#             self.button_select.grid_forget()
#             self.button_clear.grid_forget()
#         self.button_done.grid_forget()
#         if self.version == 'single':
#             selected = self.tree_options_choose.selected_item()
#             if selected:
#                 self.var.set(selected)
#                 self.self_button_main['text'] = 'Selected ' + selected
#         # if self.edit_flag:
#         #         if self.multi_value_flag:
#         #             for branches in self.data_tree.treeview.get_children():
#         #                 self.selected_items.append(self.data_tree.treeview.item(branches)['text'])
#         #         final_selected_items_text = 'OPTIONS'
#         #         for selected in self.selected_items:
#         #             final_selected_items_text += '\n' + selected
#         #         self.var.set(final_selected_items_text)
#         self.self_button_main.grid(row=1, column=0, columnspan=2)
#         # self.edit_flag = False
#
#     def display(self, flag=None):
#         if flag is None:
#             flag = self.display_flag
#         if flag:
#             self.grid_forget()
#             self.tree_options_choose.hide_tree()
#             self.display_flag = False
#         else:
#             self.self_button_main.grid(row=self.start_pos_row + 1, column=0, columnspan=2)
#             self.tree_options_choose.show_tree()
#             self.display_flag = True
#
#     def add_multi_value(self, single_value=None):
#         if not self.data_tree_display:
#             self.data_tree.show_tree()
#             self.data_tree_display = True
#         if single_value:
#             item = single_value
#         else:
#             item = self.tree_options_choose.selected_item()
#         if self.version == 'unique':
#             temp = self.tree_options_choose.selected_item(value='name')
#             current_added = self.data_tree.treeview.get_children()
#             for child in current_added:
#                 if temp == self.data_tree.treeview.item(child)['text']:
#                     messagebox.showerror('Only unique', 'No points in repeating data', parent=self)
#                     return
#             # if temp in current_added:
#         # self.data_tree.add_branch(item, [], update_flag=False)
#         self.data_tree.add_leaves_simple('', [item])
#         # self.data_tree.add_leaf('', self.tree_options_choose.selected_item(value='code'), item)
#         self.edit_flag = True
#         # self.selected_items.append(item)
#         # self.var.set(self.var.get() + '\n' + item)
#
#     def delete_multi_value(self):
#         item = self.data_tree.selected_item(value='code')
#         self.data_tree.delete_leaf(item)
#         if not self.data_tree.treeview.get_children():
#             self.data_tree.hide_tree()
#         self.edit_flag = True
#
#     def deselect_row(self):
#         self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])
#
#     # def reload_options(self, new_values):
#     #     self.list = new_values
#     #     for element_name in self.list:
#     #         self.tree_options_choose.add_branch(element_name, self.list[element_name])

class FileField:
    def __init__(self, master=None, field_name=None, field_data=None, mode=1, template_name=None):
        self.flag_list = False
        self.files_container = {}
        self.mode = mode
        self.master = master
        self.title = field_name
        self.type = 'fileData'
        self.type_image = True
        self.templateName = template_name
        self.path_cut = '../../'
        self.row_size = 1
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.button_file_field = CustomButton(master, field_name + '\nClick to select file or files')
        self.button_file_field.clicked.connect(self.select_file)
        self.file_display = QtWidgets.QListWidget(parent=master)
        self.file_display.setFixedHeight(20)
        self.file_display.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.filter_list = "Image Files (*.png *.jpg *.bmp)"
        if field_data:
            if 'tooltip' in field_data:
                self.button_file_field.setToolTip(field_data['tooltip'])
            if 'notmap' in field_data['options']:
                self.path_cut = '../'
            if 'list' in field_data['options']:
                self.flag_list = True
                self.file_display.setFixedHeight(70)
                self.shortcut_del = QtWidgets.QShortcut(QtGui.QKeySequence('Delete'), self.file_display)
                self.shortcut_del.activated.connect(self.delete)
            if 'music' in field_data['options']:
                self.type_image = False
                self.filter_list = "Music Files (*.mp3 *.wav)"

        self.flag_edit = True
        # self.custom_layout.addWidget(self.label_custom)
        self.custom_layout.addWidget(self.button_file_field)
        self.custom_layout.addWidget(self.file_display)

    def set_val(self, values):
        if values:
            if isinstance(values, str):
                values = [values]
            for val in values:
                file_name = val.split('/')[-1]
                self.files_container[file_name] = val
                self.file_display.addItem(file_name)

            if self.flag_edit:
                GlobalVariables.Glob_Var.edited_field()

    def get_val(self, temp_dict_container=None):
        return_list = []
        for val in self.files_container:
            return_list.append(self.files_container[val])
        # if return_list:
        if self.flag_list:
            return_value = return_list
        else:
            if len(return_list) == 0:
                return_value = return_list
            else:
                return_value = return_list[0]
        if temp_dict_container is not None:
            temp_dict_container[self.title] = return_value
        else:
            return return_value

    def clear_val(self):
        self.files_container.clear()
        self.file_display.clear()

    def select_file(self):
        prep_data = []
        if self.flag_list:
            files = QtWidgets.QFileDialog.getOpenFileNames(self.master, "Select files", filter=self.filter_list)
            if files[0]:
                """this is similar to set val, so rework file path to cut out most out and pass to set val"""
                for file in files[0]:
                    file_path_start = file.find('Mods/')
                    file_path = self.path_cut + file[file_path_start:]
                    prep_data.append(file_path)
        else:
            file = QtWidgets.QFileDialog.getOpenFileName(self.master, "Select files")
            if file:
                file_path_start = file[0].find('Mods/')
                file_path = self.path_cut + file[0][file_path_start:]
                prep_data.append(file_path)

        self.set_val(prep_data)
        # return
        # if self.flag_list:
        #     file = QtWidgets.QFileDialog.getOpenFileNames(self.master, "Select files", filter=self.filter_list)
        #     if file[0]:
        #         """this is similar to set val, so rework file path to cut out most out and pass to set val"""
        #         prep_data = []
        #         for files in file[0]:
        #             temp = files.split('/')
        #             filename = temp[-1]
        #             file_path_start = files.find('Mods/')
        #             file_path = self.path_cut + files[file_path_start:]
        #             # self.files_container[filename] = file_path
        #             # self.file_display.addItem(filename)
        # else:
        #     file = QtWidgets.QFileDialog.getOpenFileName(self.master, "Select files")
        #     if file:
        #         temp = file[0].split('/')
        #         filename = temp[-1]
        #         file_path_start = file[0].find('Mods/')
        #         file_path = self.path_cut + file[0][file_path_start:]
        #         self.files_container.clear()
        #         self.files_container[filename] = file_path
        #         self.file_display.clear()
        #         self.file_display.addItem(filename)


    def set_up_widget(self, outside_layout, insert_for_options=False):
        if insert_for_options:
            outside_layout.insertLayout(outside_layout.count() - 1, self.custom_layout)
        else:
            outside_layout.addLayout(self.custom_layout)

    def destroy(self):
        for idx in range(self.custom_layout.count()):
            temp = self.custom_layout.takeAt(0)
            self.custom_layout.removeWidget(temp.widget())
            temp.widget().deleteLater()

    def delete(self):
        items_indexes = self.file_display.selectedIndexes()
        items_to_delete = []
        for items in items_indexes:
            items_to_delete.append(items.row())
        items_to_delete.sort(reverse=True)
        for item in items_to_delete:
            item_to_delete_from_container = self.file_display.takeItem(item)
            self.files_container.pop(item_to_delete_from_container.text())
        return

    def focusInEvent(self, event):
        if self.connector_to_outside_complex_class:
            GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
        else:
            GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
        super().focusInEvent(event)


class InputList(CustomWidget):
    def __init__(self, master=None, flag_delete=False, field_name=None, pass_tooltip=None, field_data={}):
        super().__init__(master_widget=master, field_name=field_name, label_pos='H')
        """here i attempt to test the other way of making customer widget, which is with 
        default customer widget with defs instead of making customer Entry, list etc and each having same defs
        and here specific widget should be named self.field"""
        self.label_custom.setToolTip(pass_tooltip)
        self.label_custom.change_position('L')
        self.title = field_name
        self.type = 'text_list'
        self.field = QtWidgets.QComboBox()
        self.field.setEditable(True)
        self.custom_layout.addWidget(self.field)
        self.row_size = 1
        self.displayed_list = False
        if 'choices' in field_data:
            self.list_values = field_data['choices']
            self.field.addItems(self.list_values)
        if flag_delete:
            self.del_button = CustomButton(None, label_text='X')
            self.del_button.clicked.connect(self.delete_val)
            self.del_button.setFixedWidth(30)
            self.custom_layout.addWidget(self.del_button)
            self.delete_place = None
            self.choice_no_field = None
            self.event_name = None

    def get_val(self, temp_dict_container=None):
        if temp_dict_container is not None:
            temp_dict_container[self.title] = self.field.currentText()
        else:
            return self.field.currentText()

    def set_val(self, value):
        self.field.setCurrentText(value)

    def clear_val(self, mode=''):
        # TODO somehow disconnect
        self.field.setCurrentText("")
        if mode:
            for idx in range(len(self.list_values)):
                self.field.removeItem(0)
            self.list_values.clear()

    def reload_options(self, new_values_list):
        self.list_values = new_values_list
        for idx in range(self.field.count()):
            self.field.removeItem(0)
        self.field.addItems(self.list_values)

    def limit_options(self, limit_list):
        """this is for """
        self.field.clear()
        if limit_list:
            self.field.addItems(limit_list)
        elif 'empty' in limit_list:
            return
        else:
            self.field.addItems(self.list_values)

    def select_val(self, *args):
        """get selected item from displayed list, put it in the entry(var) and hide the list"""
        val = self.field_list.get(self.field_list.curselection())
        self.var.set(val)
        self.field_list.grid_forget()
        self.displayed_list = False
        """if selected entry is file, it should trigger file load, get file path and put the path instead."""
        if val == 'file':
            temp = otherFunctions.browse_files(False, False)[0]
            file_path = temp[temp.find('game'):]
            file_path = file_path.replace('game', '...')
            self.var.set(file_path)

    def delete_val(self):
        """for now, deleting will be mainly for choices and maybe displayed characters."""
        val_to_delete = self.field.currentText()
        val_idx = self.field.currentIndex()
        if val_to_delete not in self.list_values:
            return
        self.list_values.remove(val_to_delete)
        self.field.removeItem(val_idx)
        if self.delete_place:
            mod_temp_data.delete_val(self.delete_place, val_to_delete, self.choice_no_field)


class CheckBox(QtWidgets.QCheckBox):
    def __init__(self, master_window, field_name, return_value):
        super().__init__(parent=master_window)
        self.return_value = return_value
        self.setText(field_name)
        # self.stateChanged.connect(self.test)

    def test(self):
        print('checkbox clicked')
        print(str(self.isChecked()))

    def get_val(self):
        if self.isChecked():
            return self.return_value
        else:
            return ''

    def set_val(self, value=None):
        if value:
            self.setChecked(True)

    def clear_val(self):
        self.setChecked(False)

    def change_f(self, new_function):
        self.stateChanged.connect(new_function)

    def change_label(self, new_label):
        self.setText(new_label)

    def set_up_widget(self, outside_layout):
        outside_layout.addWidget(self)

    # def focusInEvent(self, event):
    #     if self.connector_to_outside_complex_class:
    #         GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
    #     else:
    #         GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
    #     super().focusInEvent(event)

    # def pack(self):
    #     self.pack(side=tk.LEFT)
    #
    # def destroy(self):
    #     self.destroy()


"""game temp data. should contains info about choices and displayed characters.like this
{events:{eventname: {choices:{int:[string], int:[string]}, DisplayCharacters:{scenename:[characters], scenename:[characters]}}, girls:{same as in events}}"""


class ModTempData:
    def __init__(self):
        # self.mod_data = {'choices': {}, 'displaycharacters': {}}
        self.mod_data = {'events': {}, 'girls': {}}
        self.current_editing_event = ''
        self.data_filename = ''
        self.templates_access = None
        self.temp_chara_list = []
        # print('test creation modtempdata')
        # with open('files/temp_data/' + mod_name + '_temp_data.json', 'r', encoding='utf-8-sig') as event_data:
        #     self.mod_data = json.load(event_data, object_hook=OrderedDict)
        from os import access, F_OK, mkdir
        if not access('files/modsTempData', F_OK):
            mkdir('files/modsTempData')

    def prepare_data_new_event(self, event_name):
        """prepare dictionary for this event."""
        self.mod_data['events'][event_name] = {}
        """in this dictionary for entire event will be choices - number:[text1, text2]"""
        self.mod_data['events'][event_name]['choices'] = {}
        """and displayed characters, divided by scenes"""
        self.mod_data['events'][event_name]['DisplayCharacters'] = {}

    def prepare_data_load_mod(self, mod_name):
        # return
        self.data_filename = 'files/modsTempData/' + mod_name + '_mod_temp_data.json'
        if isfile(self.data_filename):
            self.mod_data = otherFunctions.load_json_data(self.data_filename)
        else:
            """need to go over all events and write up all choices and displayed chara
            this should be used after all is loaded, so everything is in globabl in current mode"""
            for event in GlobalVariables.Mod_Var.mod_data['Events']:  # this is all data
                self.prepare_data_new_event(event)
                temp_dict_list_dischara = {}
                for event_text in GlobalVariables.Mod_Var.mod_data['Events'][event]['EventText']:  # this is list
                    """also remember, if not found this function, copy data from previous scene"""
                    # self.mod_data['events'][event]['DisplayCharacters'][scene['NameOfScene']] = []
                    scene_len = len(event_text['theScene'])
                    text_no = 0
                    current_chara = []
                    prev_chara = []
                    """go over all rows in the text"""
                    while text_no < scene_len:
                    # for texts in scene['theScene']:
                        # self.mod_data['events'][event]['DisplayCharacters'] = {scene['NameOfScene']: []}
                        if event_text['theScene'][text_no] == 'SetChoice':
                            # index function get first match, so the text "setchoice" index will always return first val
                            text_no += 1
                            if event_text['theScene'][text_no] not in self.mod_data['events'][event]['choices']:
                                self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]] = []
                            if event_text['theScene'][text_no+1] not in self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]]:
                                self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]].append(event_text['theScene'][text_no+1])
                            text_no += 1
                            """need explanation how change layers works"""
                        elif event_text['theScene'][text_no] == 'DisplayCharacters':
                            for idx in range(1, 12):
                                text_no += 1
                                if event_text['theScene'][text_no] == 'EndLoop':
                                    break
                                if event_text['theScene'][text_no] not in current_chara:
                                    current_chara.append(event_text['theScene'][text_no])
                            temp_dict_list_dischara[event_text['NameOfScene']] = current_chara
                        text_no += 1
                        """now check if there was no displaychara, copy data from previous listdischara"""
                    if prev_chara:
                        if not current_chara:
                            temp_dict_list_dischara[event_text['NameOfScene']] = prev_chara
                        else:
                            temp_dict_list_dischara[event_text['NameOfScene']] = current_chara
                            prev_chara = current_chara
                    # this not working still
                self.mod_data['events'][event]['DisplayCharacters'] = temp_dict_list_dischara
    # TODO when closing program, this should run
    def save_file(self):
        if self.data_filename:
            otherFunctions.write_json_data(self.data_filename, self.mod_data)

    def add_choice(self, choice_number, choice_text):
        """first get current event name"""
        event_name = self.templates_access['Events'].input_filename.get_val()
        if event_name not in self.mod_data['events']:
            self.prepare_data_new_event(event_name)
            self.current_editing_event = event_name
        if choice_number in self.mod_data['events'][event_name]['choices']:
            if choice_text not in self.mod_data['events'][event_name]['choices'][choice_number]:
                self.mod_data['events'][event_name]['choices'][choice_number].append(choice_text)
        else:
            self.mod_data['events'][event_name]['choices'][choice_number] = [choice_text]

    def get_choices(self, get_val, event_name=None):
        if not event_name:
            event_name = self.current_editing_event
        if event_name in self.mod_data['events']:
            choices_list = list(self.mod_data['events'][event_name]['choices'].keys())
            if get_val == 'gate':
                return choices_list
            else:
                if get_val in choices_list:
                    # return list(self.mod_data['events'][event_name]['choices'][get_val])
                    return self.mod_data['events'][event_name]['choices'][get_val]
                else:
                    return []
        else:
            return []

    def get_gates(self, choice, event_name=None):
        if not event_name:
            event_name = self.current_editing_event
        if event_name in self.mod_data['events']:
            for gate in self.mod_data['events'][event_name]['choices']:
                if choice in self.mod_data['events'][event_name]['choices'][gate]:
                    return gate

    def get_all_choices_text(self, event_name=None):
        if not event_name:
            event_name = self.current_editing_event
        temp_list = []
        if event_name in self.mod_data['events']:
            for gate in self.mod_data['events'][event_name]['choices']:
                for choice_text in self.mod_data['events'][event_name]['choices'][gate]:
                    temp_list.append(choice_text)
        return temp_list

    def update_chara(self, characters_list_or_scene_name):
        """since i messed up, as always, i cant add characters from function directly. too much work and wasted 2 hours on thinking
        instead, make temporary list of characters. then, when saving scene, if there is a temporary list,
         get scene name and add chara to the data"""
        """if just list, add to temporary data"""
        if isinstance(characters_list_or_scene_name, list):
            for chara in characters_list_or_scene_name:
                self.temp_chara_list.append(chara)
        else:
            """if not list, then it should be scene name, so add temp to main data and clear it"""
            event_name = self.current_editing_event
            self.mod_data['events'][event_name]['DisplayCharacters'][characters_list_or_scene_name] = self.temp_chara_list
        return

    def delete_val(self, del_place, target_val, choice_number=None):
        event_name = self.current_editing_event
        if del_place == 'choice':
            choice_no = choice_number.get_val()
            self.mod_data['events'][event_name]['choices'][choice_no].remove(target_val)
        elif del_place == 'gate':
            self.mod_data['events'][event_name]['choices'].pop(target_val)
        elif del_place == 'chara':
            self.mod_data['events']['DisplayCharacters'].remove(target_val)

    """Below def are specific for fields that should display choices data"""
    def prepare_fields_for_choice_set_up(self, field_choice_no, field_choice_text, event_field_source=None):
        if event_field_source:
            event_field_source.var.trace_id = event_field_source.var.trace("w", lambda *args, arg1=field_choice_no,
                                                                                       arg2=field_choice_text,
                                                                                       arg3=event_field_source: self.set_up_event_source(field_choice_no=arg1, field_choice_text=arg2, event_field_source=arg3))
        else:
            """what if creating event? then inputfilename might be empty"""
            """dont know what this is for"""
            # self.event_source = GlobalVariables.templates['Events'].input_filename.get_val()
            self.set_up_event_source(field_choice_no=field_choice_no, field_choice_text=field_choice_text)
        field_choice_no.field.currentTextChanged.connect(lambda arg1=field_choice_no,
                                                           arg2=field_choice_text: self.set_up_choices_text(field_choice_no=arg1, field_choice_text=arg2))

        field_choice_no.delete_place = 'gate'
        field_choice_text.delete_place = 'choice'
        field_choice_text.choice_no_field = field_choice_no
        """this connects second with first field, but app breaks since first field is already connected, it kinda loops"""
        # field_choice_text.field.currentTextChanged.connect(lambda arg1=field_choice_no, arg2=field_choice_text:
        #                                                     self.set_up_choices_no(arg1, arg2))


    def set_up_event_source(self, field_choice_no, field_choice_text, event_field_source=None):
        if event_field_source:
            self.current_editing_event = event_field_source.get_val()
        else:
            self.current_editing_event = self.templates_access['Events'].input_filename.get_val()
        """first field should be choice number, second field should be choice text"""
        choice_list = self.get_choices(get_val='gate', event_name=self.current_editing_event)
        field_choice_no.reload_options(choice_list)
        # self.field_choice_no.event_name = event_name
        choice_list = self.get_all_choices_text(event_name=self.current_editing_event)
        field_choice_text.reload_options(choice_list)
        # self.field_choice_text.event_name = event_name

    def set_up_choices_text(self, field_choice_no, field_choice_text):
        """get choice number and load choices text"""
        """in PYQT, connected combobox passes already selected value, so no need to get_val again"""
        # choice_gate = field_choice_no.get_val()
        choice_gate = field_choice_no
        if choice_gate:
            choices_list = self.get_choices(get_val=choice_gate, event_name=self.current_editing_event)
            field_choice_text.limit_options(choices_list)

    def set_up_choices_no(self,field_choice_no, field_choice_text):
        # if event.keysym == "Return":
        #     """get choice text and load its number"""
        choice_text = field_choice_text.get_val()
        if choice_text:
            choices_no = self.get_gates(choice=choice_text, event_name=self.current_editing_event)
            field_choice_no.set_val(choices_no)
        # field_choice_text.handle_keyrelease_list(event)
        """here might be problems, since i have to add simple function to event binding for list field"""
mod_temp_data = ModTempData()

# class MainGameItemsInNewWindow(object):
#     # obsolete, but might be usefull elsewhere
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(310, 299)
#         self.widget = QtWidgets.QWidget(Dialog)
#         self.widget.setGeometry(QtCore.QRect(0, 10, 301, 281))
#         self.widget.setObjectName("widget")
#
#         self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
#         self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout_2.setObjectName("verticalLayout_2")
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.lcdNumber = QtWidgets.QLCDNumber(self.widget)
#         self.lcdNumber.setObjectName("lcdNumber")
#         self.verticalLayout_2.addWidget(self.lcdNumber)
