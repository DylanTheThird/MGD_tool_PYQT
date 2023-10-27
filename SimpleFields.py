from os.path import isfile
import copy
import GlobalVariables
import otherFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem, QAbstractItemView, QSize, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal


"""pyqt widges"""
"""simple fields contains mostly 1 widget"""


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

    def set_up_widget(self, outside_layout, insert_for_optional=False, insert_pos=0):
        """insert is mostly for optional fields to insert widget before last stretch"""
        if insert_for_optional:
            if insert_pos == 0:
                insert_pos = outside_layout.count() - 1
            outside_layout.insertLayout(insert_pos, self.custom_layout)
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

    def change_background_color(self):
        self.setStyleSheet("background-color: red")

    def clear_color(self):
        self.setStyleSheet("")


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
            if len(field_name) < 2:
            # if isinstance(field_name, int):
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
        so instead, just make simple text field, which is created in another class"""
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
                if 'function' in field_data['options']:
                    but_markup = CustomButton(None, 'F')
                    but_markup.setMaximumWidth(20)
                    but_markup.clicked.connect(self.open_text_editor)
                    self.custom_layout.addWidget(but_markup)
        # self.shortcuts = []
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
        """insert is mostly for optional fields to insert widget before last stretch"""
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
        # TODO this not always working

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
    def open_text_editor(self):
        import MarkUpDialog
        markup_win = MarkUpDialog.MarkUp_Window(target_field=self, scenes_flag=False)
        markup_win.show()

class SimpleEntryDisplay(SimpleEntry):
    # TODO might be obsolete
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
        self.setPlaceholderText('0')

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        # check if key is digit or functional like tab or enter
        if 47 < event.key() < 58 or 100 < event.key():
            return super().keyPressEvent(event)


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
        self.addition = False
        if field_data:
            if 'options' in field_data:
                if 'addition' in field_data['options']:
                    self.addition = True
        if edit:
            self.field_modified_check()

    def get_val(self, temp_dict_container=None):
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


class SingleList(QtWidgets.QComboBox):
    def __init__(self, master_window=None, label_text=None, field_data=None, template_name=None,
                 class_connector=None, edit=True, label_pos='H'):
        super().__init__(parent=master_window)
        self.template_name = template_name
        self.type = 'singlelist'
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
                list = otherFunctions.getListOptions(field_data['choices'], "single")
                self.set_val(list)
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
            # if sort:
            #     value.sort()
            if len(value) >= 1:
                self.list = value
                self.addItems(value)
        else:
            self.setCurrentText(value)

    def clear_val(self):
        self.setCurrentIndex(0)

    def set_up_widget(self, outside_layout, insert_for_options=False, insert_pos=0):
        if self.custom_layout:
            if insert_for_options:
                if insert_pos == 0:
                    insert_pos = outside_layout.count() - 1
                outside_layout.insertLayout(insert_pos, self.custom_layout)
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

    def add_items_to_skip_sort(self, items=list):
        self.list += items
        self.addItems(items)

    def field_modified_check(self):
        self.currentIndexChanged.connect(GlobalVariables.Glob_Var.edited_field)

    def reload_options(self, options_list=list):
        if options_list:
            self.clear()
            self.list = otherFunctions.getListOptions(options_list, "single")
            self.set_val(self.list)
            # TODO dropdown display adjust
            """below should limit rectangle box that appeares when clicking dropdown, probably for choices, but otherwise limits view"""
            # w = self.fontMetrics().boundingRect(max(self.list, key=len)).width()
            # self.view().setFixedWidth(w + 20)
        else:
            return

    # it sometimes causes error when opening function designer. I don't remember where it was needed.
    # if something else does not work, enable it
    # def focusInEvent(self, event):
    #     print(self.list)
    #     print(self.title)
    #     if self.connector_to_outside_complex_class:
    #         GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
    #     else:
    #         GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
    #     try:
    #         super().focusInEvent(event)
    #     except:
    #         print(
    #             'error sometimes when loading event designer wrapped C/C++ object of type SingleList has been deleted')
    #         print(self.title)
    #         print(self.list)


class UniqueView(QtWidgets.QListView):
    def __init__(self, master, field_title=None, class_connector=None, data_treeview=None):
        super().__init__(parent=master)
        """this is used for multilist display, to show items that should not repeat"""
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
        if self.flag_edit:
            GlobalVariables.Glob_Var.edited_field()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            # self.delete_leaf()
            self.delete()
        super().keyPressEvent(event)

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
        if self.flag_edit:
            GlobalVariables.Glob_Var.edited_field()

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
        self.title = listTitle
        self.type = 'element_list'
        self.flag_folders = folders
        self.flag_focus = True
        self.parent_tag = 'folder'
        self.flag_child_editable = all_edit
        self.flag_edit = True
        self.connector_to_outside_complex_class = class_connector
        self.tree_model = QStandardItemModel()
        self.setHeaderHidden(True)
        self.setModel(self.tree_model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        """seach fields needs to be last as it required different model to be used and
         I dont know how to add and remove from it"""
        if search_field:
            self.flag_search = True
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
        self.rootnode = None
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
        self.flag_delete = delete_flag

        self.shortcut_restore = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+z'), self)
        self.shortcut_restore.activated.connect(self.restore_deleted)
        self.shortcut_cut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+x'), self)
        self.shortcut_cut.activated.connect(self.delete_with_backup)
        self.shortcut_paste = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+v'), self)
        self.shortcut_paste.activated.connect(lambda arg1=True: self.restore_deleted(arg1))
        # escapePressed = pyqtSignal(str)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        # print('clicked')
        if event.key() == Qt.Key_Delete:
            # print('pressed delete')
            if self.flag_delete:
                # print('pressed delete')
                self.delete_with_backup()
        elif event.key() == Qt.Key_Escape:
            # self.selection_cancel()
            self.selectionModel().clear()
        super().keyPressEvent(event)

    def focusInEvent(self, event):
        # might be problems with it, if something, change name and figure out field custom>monster groups
        # print('event-focus-in:', self.objectName())
        if self.flag_focus:
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

    def add_data(self, data=[], node=None, update_flag=False, insert_row=False, data_info = ''):
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
        self.add_data_to_display(data, node, insert_row, data_info)
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

    def add_data_to_display(self, data=[], node=None, insert_row=False, data_info=''):
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
            if data_info:
                bottom_row.setWhatsThis(data_info)
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
        # same as above, but without final items, just add more rows to parent node. This is recursive.
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
                # found_node = self.tree_model.item(row_index.row(), row_index.column(),)
                return row_index
            search_node = self.find_node(node_to_find, row_index)
            if search_node:
                return search_node

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
                else:
                    temp = self.model()
                    selected_index[idx] = temp.itemFromIndex(selected_index[idx])
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
        """this is to select element in treeview. Used in pair with restore selected"""
        if isinstance(text, str):
            element_index = self.find_node(text)
        else:
            element_index = text
        if element_index:
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

    def add_branch(self, row_text, row=None, parent=None, row_height=0):
        # this returns added item, in case to use with add leaves-next
        new_branch = QStandardItem(row_text)
        new_branch.setEditable(True)
        if row_height > 0:
            new_branch.setSizeHint(QSize(0, row_height))
        if parent:
            if row:
                parent.insertRow(row, new_branch)
            else:
                parent.appendRow(new_branch)
        else:
            if row:
                self.tree_model.insertRow(row, new_branch)
            else:
                self.tree_model.appendRow(new_branch)
        return new_branch

    def add_folder(self, folder_name, node=None):
        """add 1 item, which suppose to contains more items"""
        if node is None:
            """for adding element, need to add folder to existing items"""
            node = self.selected_element()
        if node is None:
            # node = self.tree_model
            node = self.model()
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
        return new_folder

    def add_leaf(self, list_of_strings_to_insert_in_row=[], row=None, parent=None, row_height=0, additional_data=''
                 , editable=False):
        new_leaves = []
        for text in list_of_strings_to_insert_in_row:
            new_leaf = QStandardItem(text)
            if editable:
                new_leaf.setEditable(True)
            else:
                new_leaf.setEditable(False)
            if additional_data:
                new_leaf.setWhatsThis(additional_data)
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

    def change_selection(self, selection='S/M'):
        if selection == 'S':
            self.setSelectionMode(QAbstractItemView.SingleSelection)
        elif selection == 'M':
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
    #         I think there is at least 1 more type, but its not used anywhere


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
            # leaves_to_delete_by_text.append(self.tree_model.itemFromIndex(leaf))
            leaves_to_delete_by_text.append(leaf)
        for item in leaves_to_delete_by_text:
            # item = self.tree_model.indexFromItem(leaf)
            # item_in_sort = self.sorting.mapToSource(item)
            self.tree_model.removeRow(item.row(), item.parent())
            # self.sorting.removeRow(item_in_sort.row(),item_in_sort.parent())
        return

    def delete_with_backup(self):
        """this is used with shortcuts, to be able to restore deleted items."""
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

    def clear_val(self):
        self.clear_tree()

    def change_title(self, new_title):
        self.title = new_title
        self.setHeaderHidden(False)
        self.tree_model.setHorizontalHeaderLabels([new_title])

    def search_value(self, name='', index='', mode=''):
        # self.setModel(self.sorting)
        search_val = self.entry_search.text()
        self.sorting.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.sorting.setFilterWildcard(search_val)
        # self.setModel(self.tree_model)

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

    def transform_index_to_item(self, element_index_to_item):
        if self.flag_search:
            element_index_to_item = self.sorting.mapToSource(element_index_to_item)
        element_index_to_item = self.tree_model.itemFromIndex(element_index_to_item)
        return element_index_to_item

    def set_up_widget(self, outside_layout, insert_for_options=False):
        if insert_for_options:
            outside_layout.insertLayout(outside_layout.count() - 1, self.layout)
        else:
            outside_layout.addLayout(self.layout)
        outside_layout.setAlignment(self, QtCore.Qt.AlignCenter)

    def set_val(self, data):
        self.add_data_to_display(data)


class MultiListDisplay:
    """there are 3 types of data here.
    single item - only 1 item allowed, so it could be an input field, where you can type text to autosearch for
     available values from main multilist, also limited to type of items to seachs
    several items - this allows several items with no duplication. will be a treeview and maybe add something like above
    multiple items - several with duplicates."""
    def __init__(self, master=None, field_name=None,
                 field_data=None, template_name=None, main_data_treeview=None, single_edit=True):
        self.title = field_name
        self.type = 'multilist'
        self.template_name = template_name
        self.label_custom = CustomLabel(master, field_name)
        self.addition = False
        self.row_size = 4
        self.limit = 0
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
            if 'limit' in field_data['options']:
                self.limit = field_data['limit']
        if 'tooltip' in field_data:
            self.label_custom.setToolTip(field_data['tooltip'])
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
            self.final_data = SimpleEntry(master, None, class_connector=self, main_data_treeview=main_data_treeview, edit=single_edit)
            self.label_custom.change_position('R')
            self.custom_layout = QtWidgets.QHBoxLayout()
            self.custom_layout.setAlignment(QtCore.Qt.AlignCenter)
        elif self.version == 'unique':
            # self.final_data = QtWidgets.QListWidget(parent=master)
            self.final_data = UniqueView(master=master, class_connector=self, data_treeview=main_data_treeview)
            self.label_custom.change_position('C')
        else:
            # well, this last should probably be simple element list.
            self.final_data = UniqueView(master=master, class_connector=self, data_treeview=main_data_treeview)
            # self.final_data = ElementsList(master, field_name, class_connector=self)
            self.label_custom.change_position('C')
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
                if self.limit:
                    if current_count > self.limit:
                        otherFunctions.show_message('Warning',' Reached limit. Please remove some before adding more'
                                                    ,'Warning')
                        return
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
        if self.version == 'single':
            return_data = self.final_data.get_val()
        else:
        # elif self.version == 'unique':
            # since both unique and normal are uniqueView, just get_data should work in both cases
            return_data = self.final_data.get_data()
        # else:
        # since final data is separate custom field, it should have get_data()
        # return_data = self.final_data.get_data()
        if temp_dict_container is not None:
            temp_dict_container[self.title] = return_data
        else:
            return return_data

    def clear_val(self):
        if self.version == 'unique':
            # self.final_data.clear()
            # should work the same
            self.final_data.clear_val()
        else:
            self.final_data.clear_val()

    def hide(self):
        self.label_custom.hide()
        self.final_data.hide()

    def show(self):
        self.final_data.show()
        if self.label_custom.text():
            self.label_custom.show()

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


# this is multilist with main item data. Customized.
class Main_MultiList:
    def __init__(self, master=None, field_name=None, main_label_flag=True):
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.title = field_name
        self.type = 'main_multilist'
        self.edit_flag = False
        select_mode = 'extended'
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

        self.main_data = ElementsList(None, 'Available element', search_field=True, delete_flag=False,
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
                    self.data_for_display['Fetishes'] = [{'main game': list(main_game_items[element]['Fetish'].keys())}]
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
        """stances"""
        self.data_for_display['Stances'] = GlobalVariables.Glob_Var.stances
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

    # def get_val(self, temp_dict_container=None):
    #     if self.version == 'single':
    #         temp = self.var.get()
    #         if temp in ['click', 'CLICK']:
    #         # if 'click' in temp or 'CLICK' in temp:
    #             temp = ''
    #     # elif self.version == 'multi':
    #     #     all_vals = self.data_tree.treeview.get_children()
    #     #     for value in all_vals:
    #     #         temp.append(self.data_tree.treeview.item(value)['text'])
    #     else:
    #         temp = []
    #         all_vals = self.data_tree.treeview.get_children()
    #         for value in all_vals:
    #             temp.append(self.data_tree.treeview.item(value)['text'])
    #         # this might be important if there is a problem with values returned somewhere
    #         # if len(temp) == 0:
    #         #     temp.append('')
    #     if temp_dict_container is not None:
    #         temp_dict_container[self.title] = temp
    #     else:
    #         return temp

    def clear_val(self):
        """when creating new mod, this should be called to remove stuff from previous mod"""
        """temporary solution - manually clear stuff. take out last item which are main game stuff from 
        basic mod element, clear variable and put it back"""
        items = ['Events', 'Skills', 'Fetishes', 'Addiction', 'Items', 'Monsters', 'Perks']
        for item in items:
            temp = self.data_for_display[item][-1]
            self.data_for_display[item] = []
            self.data_for_display[item].append(temp)
        self.data_for_display['Stances']['Custom'] = []

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
            # current_elements = list(self.data_for_display[mod_item].keys())
            """temporary solution - pop everything but last item and insert mod items"""
            for idx in range(len(self.data_for_display[mod_item])-1):
                self.data_for_display[mod_item].pop(0)
            for i in temp_dict[mod_item]:
                # FUCK, in data display its FETISH, while normally its FETISHES
                # if i not in current_elements:
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

    def hide(self):
        self.file_display.hide()
        self.button_file_field.hide()

    def show(self):
        self.file_display.show()
        self.button_file_field.show()

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

    # def focusInEvent(self, event):
    #     if self.connector_to_outside_complex_class:
    #         GlobalVariables.Glob_Var.main_game_field.connect_multilist(self.connector_to_outside_complex_class)
    #     else:
    #         GlobalVariables.Glob_Var.main_game_field.disconnect_multilist()
    #     super().focusInEvent(event)


class InputList(CustomWidget):
    def __init__(self, master=None, flag_delete=False, field_name=None, pass_tooltip=None, field_data={}):
        super().__init__(master_widget=master, field_name=field_name, label_pos='H')
        """here i attempt to test the other way of making custom widget, which is with 
        default custom widget with defs instead of making custom Entry, list etc and each having same defs
        and here specific widget should be named self.field"""
        self.label_custom.setToolTip(pass_tooltip)
        # self.label_custom.change_position('L')
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

        if 'options' in field_data:
            if "file" in field_data['options']:
                self.field.currentTextChanged.connect(self.file_open)
            if 'delete' in field_data['options']:
            # if flag_delete:
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

    def file_open(self, selected_option):
        if selected_option == 'file':
            file = QtWidgets.QFileDialog.getOpenFileNames(None, "Select files")
            if file[0]:
                # file here is a tuple of ([filenames],types of files)
                self.field.setEditText(file[0][0])

    def limit_options(self, limit_list):
        """this is for """
        self.field.clear()
        if limit_list:
            self.field.addItems(limit_list)
        elif 'empty' in limit_list:
            return
        else:
            self.field.addItems(self.list_values)

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
        # outside_layout.addWidget(self.custom_widget)

    def destroy(self):
        self.deleteLater()


"""game temp data. should contains info about choices and displayed characters.like this
{events:{eventname: {choices:{int:[string], int:[string]}, DisplayCharacters:{scenename:[characters], scenename:[characters]}}, girls:{same as in events}}"""


class ModTempData:
    def __init__(self):
        self.mod_data = {'events': {}, 'girls': {}, 'stances': [], "last_update": ""}
        """events: contains information about choices
        girls - probably was something, now its empty
        stances - custom mod stance
        last update - when mod folder was modified with outside source, go over updating all"""
        self.current_editing_event = ''
        self.current_mod = ''
        self.data_filename = ''
        self.templates_access = None
        self.temp_chara_list = []
        # print('test creation modtempdata')
        # with open('files/temp_data/' + mod_name + '_temp_data.json', 'r', encoding='utf-8-sig') as event_data:
        #     self.mod_data = json.load(event_data, object_hook=OrderedDict)
        otherFunctions.check_if_folder_exists('files/modsTempData')
        # from os import access, F_OK, mkdir
        # if not access(, F_OK):
        #     mkdir('files/modsTempData')

    def start_new_mod(self, text):
        self.current_mod = text

    def prepare_data_new_event(self, event_name):
        """prepare dictionary for this event."""
        self.mod_data['events'][event_name] = {}
        """in this dictionary for entire event will be choices - number:[text1, text2]"""
        self.mod_data['events'][event_name]['choices'] = {}
        """and displayed characters, divided by scenes"""
        self.mod_data['events'][event_name]['DisplayCharacters'] = {}
        self.mod_data['events'][event_name]['Functionized'] = {}

    def prepare_data_load_mod(self, mod_name, mod_path):
        self.current_mod = mod_name
        rewrite_flag = False
        data_filename = 'files/modsTempData/' + mod_name + '_mod_temp_data.json'
        # if isfile(data_filename):
        if otherFunctions.check_if_file_exists(data_filename):
            """first check if mod folder was updated. this is in case user load same mod from 2 different places"""
            # TODO move to to if rewrite flag else after cleaning. no point in loading if need to rewrite after
            self.mod_data = otherFunctions.load_json_data(data_filename)
            mod_folder_time_date = otherFunctions.get_file_time_modification(data_filename)
            if 'last_update' in list(self.mod_data.keys()):
                if self.mod_data['last_update'] != mod_folder_time_date:
                    rewrite_flag = True
            else:
                self.mod_data['last_update'] = mod_folder_time_date
                rewrite_flag = True
        else:
            rewrite_flag = True
        if rewrite_flag:
            """need to go over all events and write up all choices and displayed chara
            this should be used after all is loaded, so everything is in global in current mode"""
            self.mod_data['stances'].clear()
            self.mod_data['girls'].clear()
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
                    # stance_temp_list = []
                    """go over all rows in the text"""
                    while text_no < scene_len:
                    # for texts in scene['theScene']:
                        # self.mod_data['events'][event]['DisplayCharacters'] = {scene['NameOfScene']: []}
                        scene = event_text['theScene']
                        if scene[text_no] == 'SetChoice':
                            # index function get first match, so the text "setchoice" index will always return first val
                            text_no += 1
                            if scene[text_no] not in self.mod_data['events'][event]['choices']:
                                self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]] = []
                            if scene[text_no+1] not in self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]]:
                                self.mod_data['events'][event]['choices'][event_text['theScene'][text_no]].append(event_text['theScene'][text_no+1])
                            text_no += 1
                            """need explanation how change layers works"""
                        elif scene[text_no] == 'DisplayCharacters':
                            for idx in range(1, 12):
                                text_no += 1
                                if scene[text_no] == 'EndLoop':
                                    break
                                if scene[text_no] not in current_chara:
                                    current_chara.append(scene[text_no])
                            temp_dict_list_dischara[event_text['NameOfScene']] = current_chara
                        elif scene[text_no] == 'ApplyStance':
                            """custom stances to add. this might repeat many times, so check if already exists"""
                            text_no += 1
                            temp = [scene[text_no]]
                            """check with main game stances"""
                            GlobalVariables.Glob_Var.check_stances(temp)
                            if temp:
                                """check if already in mod stances"""
                                if scene[text_no] not in self.mod_data['stances']:
                                    self.mod_data['stances'].append(scene[text_no])
                        text_no += 1
                        """now check if there was no displaychara, copy data from previous listdischara"""
                    if prev_chara:
                        if not current_chara:
                            temp_dict_list_dischara[event_text['NameOfScene']] = prev_chara
                        else:
                            temp_dict_list_dischara[event_text['NameOfScene']] = current_chara
                            prev_chara = current_chara
                    # this not working still # TODO
                self.mod_data['events'][event]['DisplayCharacters'] = temp_dict_list_dischara
                mod_folder_time_date = otherFunctions.get_file_time_modification(mod_path)
                self.mod_data['last_update'] = mod_folder_time_date

    def save_file(self):
        if self.current_mod:
            data_filename = 'files/modsTempData/' + self.current_mod + '_mod_temp_data.json'
            otherFunctions.write_json_data(data_filename, self.mod_data)

    def add_stances(self, stance_list):
        self.mod_data['stances'] = stance_list

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
        # issues - seems to run when reloading list of choices for each choice. should run only once
        if not event_name:
            event_name = self.current_editing_event
        # for event in self.mod_data['events']:
        #     if self.mod_data['events'][event]['name'] == event_name:
        if event_name in self.mod_data['events']:
            choices_list = list(self.mod_data['events'][event_name]['choices'].keys())
            if get_val == 'gate':
                return choices_list
            else:
                if get_val in choices_list:
                    return self.mod_data['events'][event_name]['choices'][get_val]
                else:
                    return []
        else:
            return []

    def get_gates(self, choice, event_name=None):
        """as gates i understand number assigned to choice. As it is a gate to different choices"""
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
        """not used, probably need seperate field in scene window to view currect characters in scene
        for future"""
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
        # TODO choices from event - this is with choice fields are simple imput file, not custom class
        if event_field_source:
            event_field_source.final_data.function_on_modify(self.set_up_event_source)
            # event_field_source.var.trace_id = event_field_source.var.trace("w", lambda *args, arg1=field_choice_no,
            #                                                                            arg2=field_choice_text,
            #                                                                            arg3=event_field_source: self.set_up_event_source(field_choice_no=arg1, field_choice_text=arg2, event_field_source=arg3))
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
            scene_source = event_field_source.get_val()
        else:
            scene_source = self.current_editing_event
        """first field should be choice number, second field should be choice text"""
        choice_list = self.get_choices(get_val='gate', event_name=scene_source)
        field_choice_no.reload_options(choice_list)
        # self.field_choice_no.event_name = event_name
        choice_list = self.get_all_choices_text(event_name=scene_source)
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
