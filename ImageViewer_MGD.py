from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QDockWidget, QWidget\
    , QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
# from SimpleFields import ElementsList
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem, QAbstractItemView, QSize, QBrush, QColor

# TODO maybe double click on bottom image path field to load it to view.
# TODO fix so it works with main program

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

# class CheckBoxDelegate(QtGui.QStyledItemDelegate):
#     def __init__(self, parent = None):
#         QtGui.QStyledItemDelegate.__init__(self, parent)
#     def createEditor(self, parent, option, index):
#         return None
#     def paint(self, painter, option, index):
#         checked = bool(index.model().data(index, QtCore.Qt.DisplayRole))
#         check_box_style_option = QtGui.QStyleOptionButton()
#         if (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
#             check_box_style_option.state |= QtGui.QStyle.State_Enabled
#         else:
#             check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
#         if checked:
#             check_box_style_option.state |= QtGui.QStyle.State_On
#         else:
#             check_box_style_option.state |= QtGui.QStyle.State_Off
#         check_box_style_option.rect = self.getCheckBoxRect(option)
#         QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_CheckBox, check_box_style_option, painter)
#     def editorEvent(self, event, model, option, index):
#         if not (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
#             return False
#         # Do not change the checkbox-state
#         if event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.MouseButtonDblClick:
#             if event.button() != QtCore.Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
#                 return False
#             if event.type() == QtCore.QEvent.MouseButtonDblClick:
#                 return True
#         elif event.type() == QtCore.QEvent.KeyPress:
#             if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
#                 return False
#         else:
#             return False
#         # Change the checkbox-state
#         self.setModelData(None, model, index)
#         return True
#     def setModelData (self, editor, model, index):
#         newValue = not bool(index.model().data(index, QtCore.Qt.DisplayRole))
#         model.setData(index, newValue, QtCore.Qt.EditRole)
#     def getCheckBoxRect(self, option):
#         check_box_style_option = QtGui.QStyleOptionButton()
#         check_box_rect = QtGui.QApplication.style().subElementRect(QtGui.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
#         check_box_point = QtCore.QPoint (option.rect.x() +
#                              option.rect.width() / 2 -
#                              check_box_rect.width() / 2,
#                              option.rect.y() +
#                              option.rect.height() / 2 -
#                              check_box_rect.height() / 2)
#         return QtCore.QRect(check_box_point, check_box_rect.size())

# later
#PUT THE CHECKBOX IN COLUMN 2
# myDelegate = CheckBoxDelegate()
# treeView.setItemDelegateForColumn(2, myDelegate)

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
        self.flag_focus = True
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

    def clear_val(self):
        self.clear_tree()

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

    def set_val(self, data):
        self.add_data_to_display(data)

class QImageViewer(QMainWindow):
    def __init__(self, pictures_tree=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)
        self.createActions()
        self.createMenus()

        self.bottom_widgets = QDockWidget('Data')
        self.bottom_widgets.setMaximumHeight(200)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.bottom_widgets)

        self.pictures_model = None
        if pictures_tree:
            self.pictures_model = pictures_tree
        self.prepare_widgets()
        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    def prepare_widgets(self):
        bot_widgets = QWidget()
        # bot_widgets.setMaximumHeight(100)
        """first horizontal. this is main layout"""
        bot_lay = QHBoxLayout()
        bot_widgets.setLayout(bot_lay)
        # label = QLabel('Pictures menu')
        # label.setMaximumHeight(100)
        # bot_lay.addWidget(label)
        self.bottom_widgets.setWidget(bot_widgets)

        """add stuff for organizing pictures"""
        if self.pictures_model:
            """first set, vertical, button to add set and main pictures fields"""
            max_width = 200
            lay_pictures_data = QVBoxLayout()
            lay_pictures_data.setAlignment(QtCore.Qt.AlignCenter)
            bot_lay.addLayout(lay_pictures_data)
            """first, field for setting.....sets"""
            button_set = QPushButton('Add SET')
            button_set.setMaximumWidth(max_width)
            button_set.clicked.connect(self.add_set)
            lay_pictures_data.addWidget(button_set)
            """under it, add fields for pictures main data"""
            button_pictures = QPushButton('Add PICTURES')
            button_pictures.setMaximumWidth(max_width)
            button_pictures.clicked.connect(self.add_pictures)
            lay_pictures_data.addWidget(button_pictures)
            button_images = QPushButton('Add IMAGES')
            button_images.setMaximumWidth(max_width)
            button_images.clicked.connect(self.add_images)
            lay_pictures_data.addWidget(button_images)
            """fields for image"""
            temp = ['Name', 'File', 'setXalign', 'setYalign']
            self.image_fields = {}
            for field in temp:
                temp_a = QLineEdit()
                temp_a.setPlaceholderText(field)
                temp_a.setMaximumWidth(max_width)
                self.image_fields[field] = temp_a
                lay_pictures_data.addWidget(temp_a)
            self.tree_pictures = ElementsList(None, 'Pictures', all_edit=True)
            self.tree_pictures.flag_focus = False
            self.tree_pictures.tree_model = self.pictures_model
            self.tree_pictures.setModel(self.pictures_model)
            self.tree_pictures.setMaximumWidth(800)
            self.tree_pictures.setFixedWidth(300)
            self.tree_pictures.setColumnWidth(0, 180)
            self.tree_pictures.setColumnWidth(1, 80)
            self.tree_pictures.set_up_widget(bot_lay)
            bot_lay.addStretch(1)

    def add_set(self):
        main_set = QStandardItem('placeholder')
        main_set.setEditable(False)
        temp_a = QStandardItem('Name')
        temp_a.setEditable(False)
        temp_b = QStandardItem('Set')
        temp_b.setEnabled(False)
        main_set.appendRow([temp_a, QStandardItem('placeholder')])
        main_set.child(0, 1).setWhatsThis('name')
        main_set.appendRow([temp_b, QStandardItem()])
        self.pictures_model.appendRow([main_set, QStandardItem()])
        # self.pictures_model.appendRow([main_set, temp_a])

    def add_pictures(self):
        main_set = QStandardItem('placeholder')
        main_set.setEditable(False)
        data = {
            "Name": "placeholder",
            "StartOn": "1",
            "AlwaysOn": "1",
            "IsScene": "1",
            "TheBody": "1",
            "Overlay": "No",
            "setXalign": "0.0",
            "setYalign": "0.0"}
        for col_1 in data:
            temp = [QStandardItem(col_1), QStandardItem(data[col_1])]
            temp[0].setEnabled(False)
            if temp[1].text() == '1':
                temp[1].setText('')
                temp[1].setCheckable(True)
            main_set.appendRow([temp[0], temp[1]])
        main_set.child(0, 1).setWhatsThis('name')
        temp_a = QStandardItem('Images')
        temp_a.setEditable(False)
        main_set.appendRow([temp_a, QStandardItem('')])
        """now, picture are either top level or inside SET"""
        current_select = self.tree_pictures.selected_element()
        if isinstance(current_select, list):
            current_select = current_select[0]
        """if nothing selected, add to model, else, it should search from selected to top to find SET item"""
        if current_select:
            main_row_to_add = self.find_main_parent_to_add('Set', current_select)
            main_row_to_add.appendRow(main_set)
        else:
            """if nothing selected, just add to main model"""
            self.pictures_model.appendRow(main_set)

    def add_images(self):
        # temp = self.tree_pictures.selected_element()
        # try:
        #     print(temp.data())
        # except:
        #     print('not data')
        # try:
        #     print(temp.text())
        # except:
        #     print('not text')
        # try:
        #     if temp.isCheckable():
        #         print(temp.checkState())
        # except:
        #     print('not text')
        # return
        file_path = self.image_fields['File'].text()
        if not file_path or file_path == 'missing':
            self.image_fields['File'].setText('missing')
            return
        selected = self.tree_pictures.selected_element()
        if selected:
            """images only to images row"""
            if isinstance(selected, list):
                selected = selected[0]
            if selected.text() == 'Images':
                image_title = self.image_fields['Name'].text()
                images_parent_row = QStandardItem(image_title)
                images_parent_row.setEditable(False)
                for field in self.image_fields:
                    temp_a = QStandardItem(field)
                    temp_a.setEnabled(False)
                    temp_b = QStandardItem(self.image_fields[field].text())
                    if field == 'File':
                        temp_b.setWhatsThis(self.image_fields[field].text())
                        temp = self.image_fields[field].text().split('/')[-1]
                        temp_b.setText(temp)
                    images_parent_row.appendRow([temp_a, temp_b])
                images_parent_row.child(0, 1).setWhatsThis('name')
                selected.appendRow(images_parent_row)
            else:
                return
                # TODO show warning

    def find_main_parent_to_add(self, node_to_find, child=QStandardItem):
        """similar to find root parent, but should stop on node to find"""
        if child.text() == node_to_find:
            return child
        parent = child.parent()
        if parent:
            higher_parent = self.find_main_parent_to_add(node_to_find, parent)
            return higher_parent
        else:
            return child



    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.image_fields['File'].setText(f)
            self.open(fileName=f)


    def open(self, fileName=None):
        if fileName is None:
            options = QFileDialog.Options()
            # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
            fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                      'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        # self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


# if __name__ == '__main__':
#     import sys
#     from PyQt5.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#     imageViewer = QImageViewer()
#     imageViewer.show()
#     sys.exit(app.exec_())
    # TODO QScrollArea support mouse
    # base on https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py
    #
    # if you need Two Image Synchronous Scrolling in the window by PyQt5 and Python 3
    # please visit https://gist.github.com/acbetter/e7d0c600fdc0865f4b0ee05a17b858f2