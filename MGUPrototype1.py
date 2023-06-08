# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MGUPrototype.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QStandardItem
import VisualOptions
import MarkUpDialog

from Function_class import FunctionTests

from LoadMod import start_loading_mod, new_mod
from otherFunctions import load_recent_mods, write_json_data, confirmation_message
from SimpleFields import ElementsList, Main_MultiList, mod_temp_data
from GlobalVariables import Mod_Var, Glob_Var
import TemplatesPreparation
# global Mod_Var

# TODO load a bit of data from eleement in mod to template display

# class Ui_MainWindow(object):
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.MainWindow = parent
        super().__init__(parent)
        # self.setMinimumSize(2000, 5000)
        parent.setObjectName("MainWindow")
        # parent.resize(300, 550)

    #     this is to check focus in entire app.
        QtWidgets.QApplication.instance().focusObjectChanged.connect(
            self.handleFocusChange)    #
    def handleFocusChange(self, source):
        return
        # this focus is working
        print(f'signal-focus-in:', source.objectName())
        print(str(source.parent()))
    def setupUi(self):

        # QtWidgets.QApplication.instance().focusChanged.connect(self.check_focus)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget = self
        self.centralwidget.setObjectName("centralwidget")
        # self.layout_widget = QtWidgets.QWidget(self.centralwidget)
        # self.layout_widget = self.centralwidget
        # self.layout_widget.setGeometry(QtCore.QRect(10, 5, 284, 453))
        # self.layout_widget.setObjectName("layoutWidget")
        # self.layout_widget.setMinimumWidth(200)
        # self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        """this is main layout, on left will be menus, on right templates"""
        self.layout_central = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.layout_central)
        """main layout - will contains mod items tree and main game items tree"""
        # self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main = QtWidgets.QVBoxLayout()
        # self.layout_main.setStretch(0,0)
        self.layout_central.addLayout(self.layout_main)
        # self.layout_central.addStretch(0)
        # main_spacer = QtWidgets.QSpacerItem(100, 100, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        # self.layout_central.addSpacerItem(main_spacer)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        # self.layout_main.set
        self.layout_main.setObjectName("layout_main_data")
        self.label_welcome = QtWidgets.QLabel(self.centralwidget)
        # self.label_welcome.setMaximumWidth(100)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_welcome.setFont(font)
        self.label_welcome.setText('what is this label?')
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_welcome.setObjectName("label")
        self.layout_main.addWidget(self.label_welcome)
        # self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.entry_mod_name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.entry_mod_name.setAlignment(QtCore.Qt.AlignCenter)
        self.entry_mod_name.setPlaceholderText("MOD NAME")
        self.entry_mod_name.setObjectName("mod_name")
        self.entry_mod_name.setMinimumWidth(200)
        self.entry_mod_name.setMaximumWidth(200)
        self.layout_main.addWidget(self.entry_mod_name)
        # self.gridLayout.addWidget(self.entry_mod_name, 1, 0, 1, 1)
        # self.treeWidget = QtWidgets.QTreeWidget(self.layoutWidget)
        self.tree_mod_elements = ElementsList(self.centralwidget, folders=True)
        self.tree_mod_elements.flag_edit = False
        self.tree_mod_elements.parent_tag = 'folder'
        self.tree_mod_elements.doubleClicked.connect(self.load_element_data)
        # self.tree_mod_elements = QtWidgets.QTreeView(self.layoutWidget)
        # self.tree_mod_elements.setDragEnabled(True)
        # self.tree_mod_elements.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.tree_mod_elements.setHeaderHidden(True)
        # self.tree_mod_elements.setObjectName("tree_mod_elements")
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # self.layout_central.addWidget(self.tree_mod_elements)
        self.tree_mod_elements.set_up_widget(self.layout_main)
        # self.layout_main.addStretch(0)
        # self.gridLayout.addWidget(self.tree_mod_elements, 2, 0, 2, 1)

        # spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.layout_main.addItem(spacerItem)
        self.main_game_elements = Main_MultiList(self.centralwidget, "Game elements")
        self.main_game_elements.main_data.flag_edit = False
        Glob_Var.main_game_field = self.main_game_elements
        # self.main_game_elements.set_val(Glob_Var.)
        self.main_game_elements.set_up_widget(self.layout_main)
        # self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        # all other menus and bars and stuff
        MainWindow = self.MainWindow
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 575, 21))
        self.menubar.setObjectName("menubar")
        self.menu_Mod_Menu = QtWidgets.QMenu(self.menubar)
        self.menu_Mod_Menu.setObjectName("menu_Mod_Menu")
        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        # self.menuVisual_Options = QtWidgets.QMenu(self.menuOption)
        self.actionVisual_Options = QtWidgets.QAction(MainWindow)
        self.actionVisual_Options.setObjectName("actionVisual_Options")
        self.actionVisual_Options.triggered.connect(self.visual_options)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setAllowedAreas(QtCore.Qt.TopToolBarArea)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew_Mod = QtWidgets.QAction(MainWindow)
        self.actionNew_Mod.setObjectName("actionNew_Mod")
        self.actionNew_Mod.triggered.connect(self.new_mod_prepare)
        self.actionSave_Mod = QtWidgets.QAction(MainWindow)
        self.actionSave_Mod.setObjectName("actionSave_Mod")
        self.actionSave_Mod.triggered.connect(self.save_mod)
        icon_save = QtGui.QIcon()
        icon_save.addPixmap(QtGui.QPixmap("resources/file-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Mod.setIcon(icon_save)
        self.actionLoad_Mod = QtWidgets.QAction(MainWindow)
        self.actionLoad_Mod.setObjectName("actionLoad_Mod")
        icon_load = QtGui.QIcon()
        icon_load.addPixmap(QtGui.QPixmap("resources/file-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Mod.setIcon(icon_load)
        self.actionLoad_Mod.triggered.connect(self.load_mod)
        self.actionStances = QtWidgets.QAction(MainWindow)
        self.actionStances.setObjectName("actionStances")
        self.actionAdd_new = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/file-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_new.setIcon(icon)
        self.actionAdd_new.setObjectName("actionAdd_new")
        self.actionDisplay_Details = QtWidgets.QAction(MainWindow)
        self.actionDisplay_Details.setObjectName("actionDisplay_Details")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")


        # self.actionRecentMods = QtWidgets.QAction(MainWindow)
        self.menuRecentMods = QtWidgets.QMenu(self.menuOption)
        # self.actionRecentMods.setObjectName("actionRecentMods")
        self.menuRecentMods.setObjectName("actionRecentMods")


        self.actionAdd_Addition = QtWidgets.QAction(MainWindow)
        self.actionAdd_Addition.setObjectName("actionAdd_Addition")
        self.actionMain_Status = QtWidgets.QAction(MainWindow)
        # icon = QtGui.QIcon()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/dot_red.jpg"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap("resources/dot_green.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMain_Status.setIcon(icon1)
        self.flag = 0
        self.actionMain_Status.setObjectName("actionMain_Status")
        Glob_Var.edit_status_icon = self.actionMain_Status
        self.actionSave_New = QtWidgets.QAction(MainWindow)
        self.actionSave_New.setObjectName("actionSave_new")
        Glob_Var.save_element_action = self.actionSave_New
        self.actionCancel_New = QtWidgets.QAction(MainWindow)
        Glob_Var.cancel_element_action = self.actionCancel_New
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("resources/file-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.actionCancel_New.setIcon(icon)
        self.actionCancel_New.setObjectName("actionCancel_new")
        self.menu_Mod_Menu.addAction(self.actionNew_Mod)
        self.menu_Mod_Menu.addSeparator()
        self.menu_Mod_Menu.addAction(self.actionLoad_Mod)
        self.menu_Mod_Menu.addAction(self.actionSave_Mod)
        self.menu_Mod_Menu.addSeparator()
        # self.menu_Mod_Menu.addAction(self.actionRecentMods)
        self.menu_Mod_Menu.addMenu(self.menuRecentMods)
        self.menuOption.addAction(self.actionVisual_Options)
        self.menuOption.addSeparator()
        self.menuOption.addAction(self.actionStances)
        # this was for adding actions to menu "actions" but it is available from menubar, so no need to show this
        # self.menuAdd_New.addAction(self.actionAdd_new)
        # self.menuAdd_New.addAction(self.actionDisplay_Details)
        # self.menuAdd_New.addAction(self.actionRemove)
        # self.menuAdd_New.addSeparator()
        self.menubar.addAction(self.menu_Mod_Menu.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        # self.menubar.addAction(self.menuAdd_New.menuAction())
        self.toolBar.addAction(self.actionAdd_new)
        self.toolBar.addAction(self.actionDisplay_Details)
        self.toolBar.addAction(self.actionAdd_Addition)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionMain_Status)
        self.toolBar.addAction(self.actionSave_New)
        self.toolBar.addAction(self.actionCancel_New)
        self.label_welcome.setBuddy(self.tree_mod_elements)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # recent mods
        # it should be list of lists [[name, path][name, path]]
        self.recent_mods = []
        self.recent_mods_actions = []
        self.recent_mod_limit = 3
        recent_mod_list = load_recent_mods()
        if recent_mod_list:
            recent_mod_list.reverse()
            for mods in recent_mod_list:
                self.recent_update(mods[0], mods[1])

        self.test_idx = 0
        self.actionStances.setEnabled(False)
        self.actionAdd_Addition.setEnabled(False)
        # self.actionAdd_new.setEnabled(False)
        self.actionRemove.setEnabled(False)
        self.actionDisplay_Details.setEnabled(False)
        self.actionCancel_New.setEnabled(False)
        self.actionSave_New.setEnabled(False)

        """set up fonts at start"""
        current_font = QtGui.QFont(Glob_Var.current_label_font_type,
                                   Glob_Var.current_label_font_size)
        QtWidgets.QApplication.setFont(current_font, "QLabel")
        current_font = QtGui.QFont(Glob_Var.current_text_font_type,
                                   Glob_Var.current_text_font_size)
        QtWidgets.QApplication.setFont(current_font, "QTextEdit")
        # self.prepare_templates_space()
        # # testing
        self.button_test = QtWidgets.QPushButton(text='trigger layout')
        self.button_test.clicked.connect(self.mark_up_dialog)
        # self.button_test.clicked.connect(self.testing)
        self.layout_main.addWidget(self.button_test)
        self.layout_main.addStretch(1)

        self.actionAdd_new.triggered.connect(self.new_element_prepare)
        self.actionSave_New.triggered.connect(self.save_new_element)
        self.actionCancel_New.triggered.connect(self.cancel)
        self.flag_creating_element = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_welcome.setText(_translate("MainWindow", "Welcome"))
        # __sortingEnabled = self.treeWidget.isSortingEnabled()
        # self.treeWidget.setSortingEnabled(False)
        # self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Adventures"))
        # self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "adv 1"))
        # self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "adv2"))
        # self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Items"))
        # self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "item 1"))
        # self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "item2"))
        # self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Events"))
        # self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "Event 1"))
        # self.treeWidget.topLevelItem(2).child(1).setText(0, _translate("MainWindow", "Event 2"))
        # self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.menu_Mod_Menu.setTitle(_translate("MainWindow", "&Mod Menu"))
        self.menuOption.setTitle(_translate("MainWindow", "&Options"))
        self.actionVisual_Options.setText(_translate("MainWindow", "Visual Options"))
        # self.menuLabels.setTitle(_translate("MainWindow", "Labels"))
        # self.menuAdd_New.setTitle(_translate("MainWindow", "Actions"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew_Mod.setText(_translate("MainWindow", "New Mod"))
        self.actionSave_Mod.setText(_translate("MainWindow", "Save Mod"))
        self.actionLoad_Mod.setText(_translate("MainWindow", "Load Mod"))
        # self.actionAdventure.setText(_translate("MainWindow", "Adventure"))
        # self.actionEvent.setText(_translate("MainWindow", "Event"))
        # self.actionFetish.setText(_translate("MainWindow", "Fetish"))
        # self.actionItem.setText(_translate("MainWindow", "Item"))
        # self.actionMonster.setText(_translate("MainWindow", "Monster"))
        # self.actionPerk.setText(_translate("MainWindow", "Perk"))
        # self.actionSkill.setText(_translate("MainWindow", "Skill"))
        # self.actionPerk_2.setText(_translate("MainWindow", "Perk"))
        # self.actionSkill_2.setText(_translate("MainWindow", "Skill"))
        # self.actionEvent_2.setText(_translate("MainWindow", "Event"))
        self.actionStances.setText(_translate("MainWindow", "Stances"))
        # self.actionFont.setText(_translate("MainWindow", "Font"))
        # self.actionSize.setText(_translate("MainWindow", "Size"))
        # self.actionFont_2.setText(_translate("MainWindow", "Font"))
        # self.actionSize_2.setText(_translate("MainWindow", "Size"))
        self.actionAdd_new.setText(_translate("MainWindow", "Add new"))
        self.actionDisplay_Details.setText(_translate("MainWindow", "Mod Elements"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))
        # self.actionRecentMods.setText(_translate("MainWindow", "Recent Mods"))
        self.menuRecentMods.setTitle(_translate("MainWindow", "Recent Mods"))
        self.actionAdd_Addition.setText(_translate("MainWindow", "Additions"))
        self.actionMain_Status.setText(_translate("MainWindow", "Main Status"))
        self.actionSave_New.setText(_translate("MainWindow", "Save"))
        self.actionCancel_New.setText(_translate("MainWindow", "Cancel"))

    def prepare_templates_space(self):
        """layered layout for templated"""
        self.layout_templates = QtWidgets.QStackedLayout()
        self.layout_templates.setAlignment(self.layout_main, QtCore.Qt.AlignCenter)
        # self.layout_central.addLayout(self.layout_templates)
        # self.layout_central.addStretch(1)
        # Create a widget and set the layout as its layout
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setLayout(self.layout_templates)
        #
        # Create a scroll area and set the widget as its widget
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        # self.layout.setStyleSheet("background-color:black;")
        # # main layout, which is at the top and contains only scroll area with all widgets inside
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        # self.main_layout.addStretch(1)
        self.layout_central.addLayout(self.main_layout)
        # self.layout_central.addStretch(1)


        # self.button_test = QtWidgets.QPushButton(text='trigger layout')
        # self.button_test.clicked.connect(self.testing)
        # self.layout_central.addWidget(self.button_test)
        # self.widgets_elements = {}
        # index = 0
        # for elements in Mod_Var.clear_mod:
        #     element_widget = QtWidgets.QWidget()
        #     # test = QtWidgets.QLabel()
        #     # test.setText('test ' + str(index))
        #     # tes2 = QtWidgets.QHBoxLayout()
        #     # tes2.addWidget(test)
        #     # element_widget.setLayout(tes2)
        #     """stacked layout changes stacked by int, in this case its index in widget elements
        #     each stack need widget, which need to be maintained by layout"""
        #     self.widgets_elements[elements] = [index, element_widget]
        #     self.layout_templates.addWidget(element_widget)
        #     # return
        #     index += 1

        # self.layout_templates.setCurrentIndex(0)
        """now we prepare instances of each class for templates. Each widget element needs its own layout.
        Intead of putting those layouts in widget_element dict, its set up
         in each template object as main_template_layout"""
        self.templates = {
            'Adventures': TemplatesPreparation.AdventureTemplate(),
            'Events': TemplatesPreparation.EventsTemplate(),
            'Fetishes': TemplatesPreparation.FetishesTemplate(),
            'Items': TemplatesPreparation.ItemTemplate(),
            'Locations': TemplatesPreparation.LocationsTemplate(),
            'Monsters': TemplatesPreparation.MonsterTemplate(),
            'Perks': TemplatesPreparation.PerkTemplate(),
            'Skills': TemplatesPreparation.SkillsTemplate()
        }
        index = 0
        Glob_Var.access_templates = self.templates
        for template in self.templates:
            # element_widget = QtWidgets.QWidget()
            # test = QtWidgets.QLabel()
            # test.setText('test ' + template)
            # tes2 = QtWidgets.QHBoxLayout(element_widget)
            # tes2.addWidget(test)
            # element_widget.setLayout(tes2)
            # self.layout_templates.addWidget(element_widget)
            self.templates[template].layer_index = index
            index += 1
            self.layout_templates.addWidget(self.templates[template].main_widget)
            self.templates[template].prepItemGui()

        self.templates['Fetishes'].prep_template()

        mod_temp_data.templates_access = Glob_Var.access_templates

    # might be changed to checking focus on each widget instead of here
    @QtCore.pyqtSlot("QWidget*", "QWidget*")
    def check_focus(self, old, now):
        # print('now is - ' + str(now))
        # if now == self.main_game_elements.main_data or now == self.main_game_elements.main_data.entry_search:
        #     print('works with self stuff')
        #     return
    # try:
        if now:
            # print(now.__class__.__name__)
            # if now.__class__.__name__ == 'ElementsList' or now.__class__.__name__ == 'UniqueView':
            if now.__class__.__name__ in ['ElementsList', 'UniqueView', 'CustomButton', 'SimpleEntry',
                                          'SimpleEntryDisplay', 'SingleList']:
                if now.connector_to_outside_complex_class:
                    if now.connector_to_outside_complex_class.type == 'main_multilist':
                        return
                    elif now.connector_to_outside_complex_class.type == 'multilist':
                        # print('now clickied multilist')
                        self.main_game_elements.connect_multilist(now.connector_to_outside_complex_class)
                        return
            # # print('type of clicked widget ' + now.type)
            # if now.connector_to_outside_complex_class:
            #     print(str(now.connector_to_outside_complex_class))
            #     if now.connector_to_outside_complex_class.type == 'main_multilist':
            #         return
            #     elif now.connector_to_outside_complex_class.type == 'multilist':
            #         # print('now clickied multilist')
            #         self.main_game_elements.connect_multilist(now.connector_to_outside_complex_class)
            #         return
        self.main_game_elements.disconnect_multilist()
    # except:
    #     print('something wrong with focus on treeview with duplicated data')
    #     pass
    #     print('old is - ' + str(old))
        return

    def change_icon(self):
        if self.flag:
            self.flag = 0
            self.actionMain_Status.setEnabled(False)
        else:
            self.flag = 1
            self.actionMain_Status.setEnabled(True)

    def visual_options(self):
        # dialog_visual = Dialog_Visual_Options(self.centralwidget)
        dialog_win = Dialog_Window(parent=self.centralwidget)
        dialog_visual = VisualOptions.Ui_Dialog()
        dialog_visual.setupUi(Dialog=dialog_win)
        dialog_win.show()

    def load_mod(self, mod_paths=None):
        if not mod_paths:
            file = str(QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Mod Directory"))
            temp = file.split('/')
            mod_name = temp[-1]
            self.recent_update(mod_name, file)
        else:
            mod_name = mod_paths[0]
            file = mod_paths[1]
        self.new_mod_prepare()
        self.entry_mod_name.setText(mod_name)
        start_loading_mod(file)
        self.update_mod_tree_start(Mod_Var.mod_display)
        mod_temp_data.prepare_data_load_mod(mod_name)

    def recent_update(self, new_recent_name, new_recent_path):
        # update variable with list
        self.recent_mods.insert(0, [new_recent_name, new_recent_path])
        if len(self.recent_mods) > self.recent_mod_limit:
            self.recent_mods.pop(-1)
        # update display
        _translate = QtCore.QCoreApplication.translate
        action_recent_mod = QtWidgets.QAction(self.centralwidget)
        action_recent_mod.setObjectName(new_recent_name)
        action_recent_mod.setText(_translate("MainWindow", new_recent_name))
        action_recent_mod.triggered.connect(lambda e: self.recent_load(action_widget=action_recent_mod))
        self.recent_mods_actions.insert(0, action_recent_mod)
        # add_action add at end, but to add at beginning, need to provide previous action and insert,
        #  so for first action need to add it
        if len(self.recent_mods_actions) < 2:
            self.menuRecentMods.addAction(action_recent_mod)
        else:
            self.menuRecentMods.insertAction(self.recent_mods_actions[1], action_recent_mod)
        if len(self.recent_mods_actions) > self.recent_mod_limit:
            action_to_remove = self.recent_mods_actions.pop(-1)
            self.menuRecentMods.removeAction(action_to_remove)
        # self.recent_save()

    def recent_load(self, action_widget=QtWidgets.QAction):
        # when clicking mod in recent list instead of "losd mod" option
        recent_mod_selected_name_no = self.recent_mods_actions.index(action_widget)
        # if selecting last mod, its value is 0, so there is no points in moving stuff
        if recent_mod_selected_name_no > 0:
            # now it need to move stuff around in recent display and in variable, and use data from var in load mod
            recent_mod = self.recent_mods_actions.pop(recent_mod_selected_name_no)
            self.recent_mods_actions.insert(0, recent_mod)
            self.menuRecentMods.removeAction(recent_mod)
            self.menuRecentMods.insertAction(self.recent_mods_actions[1], recent_mod)
            recent_mod = self.recent_mods.pop(recent_mod_selected_name_no)
            self.recent_mods.insert(0, recent_mod)
        else:
            recent_mod = self.recent_mods[recent_mod_selected_name_no]
        self.load_mod(recent_mod)

    def recent_save(self):
        # print('save recent mods list')
        temp = {'recentmods': self.recent_mods}
        write_json_data('recent_mods.json', temp)

    def new_element_prepare(self):
        """unlock button save and cancel
            check what element is prepared and clear template
            block loading details of element"""

        selected_element = self.tree_mod_elements.selected_element()
        if selected_element:
            self.actionCancel_New.setEnabled(True)
            element_type = self.tree_mod_elements.find_root_parent(selected_element)
            self.load_element_data(None, True)
            self.templates[element_type.text()].clear_template()
            self.flag_creating_element = True

            Glob_Var.edit_element = True

    def new_mod_prepare(self):
        """clean treeview with mod data"""
        new_mod()
        self.entry_mod_name.clear()
        self.tree_mod_elements.clear_tree()
        """turning of modifable folders so top elements cannot be clicked"""
        self.tree_mod_elements.flag_folders = False
        self.tree_mod_elements.add_data(data=Mod_Var.mod_display)
        # self.tree_mod_elements.flag_folders = Fal
        # """clean mod items in game data"""
        # mod_item = self.main_game_elements.main_data.tree_model.item(0, 0)
        # if mod_item:
        #     mod_item.removeRows(0, mod_item.rowCount())
        # selected_element = self.tree_mod_elements.selected_element()
        # if selected_element:
        #     element_type = self.tree_mod_elements.find_root_parent(selected_element)
        #     self.label_welcome.setText('Creating ' + element_type.text())

    def save_new_element(self):
        """change main label to reflect action"""
        self.label_welcome.setText('Displaying ')
        """get current element and root parent - element type"""
        selected_element = self.current_selected_item
        element_type = self.tree_mod_elements.find_root_parent(selected_element)
        """get element name and save data in mod var"""
        new_element = self.templates[element_type.text()].save_data_in_current_mod(Mod_Var.mod_data)
        if not new_element:
            return
        if 'folder' in new_element:
            """if folder, just add it as 1 row, editable"""
            new_element = new_element[7:]
            self.tree_mod_elements.add_folder(new_element)
        else:
            """add or update element name to main display"""
            check_if_adding_or_update = self.actionCancel_New.isEnabled()
            if_folder = selected_element.whatsThis()
            if not if_folder:
                selected_element = selected_element.parent()
            if check_if_adding_or_update:
                self.tree_mod_elements.add_data(data=new_element, node=selected_element)

        """copy treeview to game treeview"""
        self.main_game_elements.update_with_mod_item(self.tree_mod_elements.get_data())
        """clear displayed data"""
        self.templates[element_type.text()].clear_template()
        self.cancel()
        # self.actionSave_New.setEnabled(False)
        # self.actionMain_Status.setEnabled(False)

    def prepare_same_core_elements_in_both_displayes(self):
        """this should be obsolete, as instead of complicated adding and deleting, i'll just copy content of mod tree
        to mod item in game elements everytime something is added or deleted"""
        mod_item = QStandardItem('MOD')
        mod_item.setEditable(False)
        elements_to_add = Mod_Var.mod_display
        self.main_game_elements.main_data.tree_model.appendRow(mod_item)
        for element in elements_to_add:
            new_element = QStandardItem(element)
            new_element.setEditable(False)
            new_element.setWhatsThis('folder')
            self.tree_mod_elements.tree_model.appendRow(new_element)
            # self.main_game_elements.main_data.tree_model.appendRow(new_element)
            mod_item.appendRow(new_element.clone())

    def cancel(self):
        self.actionCancel_New.setEnabled(False)
        self.flag_creating_element = False
        # self.load_element_data(None, True)
        self.label_welcome.setText('Displaying ')
        self.actionMain_Status.setEnabled(True)
        self.actionSave_New.setEnabled(False)

    def save_mod(self):
        if self.entry_mod_name.text():
            """first prepare path to save mod"""
            mod_path = Glob_Var.start_path + Glob_Var.mod_main_switch + self.entry_mod_name.text()
            """elements type will be "adventures", "items", element_items should be [{"adventures":{"folder":...},Events}"""
            mod_files = self.tree_mod_elements.get_data()
            for elements_type in mod_files:
                """if its just string, its empty"""
                if isinstance(elements_type, str):
                    continue
                template_name = list(elements_type.keys())[0]
                self.create_folder_while_saving_mod(template_name, mod_path + '/' + template_name + '/', elements_type)
            # save_Mod_withfolders(self.entry_mod_name.text())

    def create_folder_while_saving_mod(self, template_name, el_path_start, el_items):
        """this is dictionary {'Items': [{'Consumables': ['ElvenHerb']}, {'KeyItems': ['JorasLetter']}]}"""
        for item in el_items:
            """item = Items"""
            for files in el_items[item]:
                """files = [0]"""
                if isinstance(files, dict):
                    """new dictionary"""
                    el_path = el_path_start + list(files.keys())[0] + '/'
                    self.create_folder_while_saving_mod(template_name, el_path, files)
                    # save_Mod_withfolders2(el_name, el_path, el_items[item])
                else:
                    if item == 'Fetishes':
                        self.templates[template_name].save_element_in_file(el_items[item], el_path_start)
                        break
                    else:
                        self.templates[template_name].save_element_in_file(files, el_path_start)
                    # save_element(el_name, item, el_path_start)

    def update_mod_tree_start(self, new_values):
        self.tree_mod_elements.clear_tree()
        self.tree_mod_elements.add_data(data=[new_values])
        """update with mod items works a bit different"""
        self.main_game_elements.update_with_mod_item(self.tree_mod_elements.get_data())

    def load_element_data(self, event, just_display=False):
        if self.flag_creating_element:
            return
        if_edited = self.actionSave_New.isEnabled()
        if if_edited:
            edit_decision = confirmation_message()
            if edit_decision == 'save':
                self.save_new_element()
            elif edit_decision == 'continue':
                self.cancel()
            elif edit_decision == 'cancel':
                return
        self.current_selected_item = self.tree_mod_elements.selected_element()
        root_parent = self.tree_mod_elements.find_root_parent(self.current_selected_item).text()
        # testing, just open correct index
        if root_parent:
            if not just_display:
                # if selected_item.child(0, 0) or selected_item.text() == root_parent:
                if self.current_selected_item.whatsThis() == 'folder' or self.current_selected_item.text() == root_parent:
                # if selected_item.text() == root_parent or selected_item.child(0, 0):
                    return
                Glob_Var.edit_element = False
                self.templates[root_parent].load_element_data(self.current_selected_item.text())
                # self.templates[root_parent].load_element_data(self.current_selected_item.text(), Mod_Var.mod_data[root_parent][self.current_selected_item.text()])
                Glob_Var.edit_element = True
            # print(str(selected_item.text()))
            self.layout_templates.setCurrentIndex(self.templates[root_parent].layer_index)
            # TODO ajust size
            if self.MainWindow.isMaximized() is False:
                if self.templates[root_parent].size:
                    # self.MainWindow.setMaximumSize(self.templates[root_parent].size[0], self.templates[root_parent].size[1])
                    self.MainWindow.resize(self.templates[root_parent].size[0], self.templates[root_parent].size[1])
                    # workaround. scroll bars disappear, so its always something
                    self.scroll_area.resize(self.templates[root_parent].size[0], self.templates[root_parent].size[1])
        # print('double clicked mod tree')

    def mark_up_dialog(self):
        # dialog_win = Dialog_Window(parent=self.centralwidget)
        # dialog_markup = MarkUpDialog.Ui_Dialog()
        # dialog_markup.setupUi(Dialog=dialog_win)
        # dialog_win.show()
        """need to gather data from main data display in this window"""
        # data_for_functions = self.main_game_elements.main_data.get_data()
        self.markup_win = MarkUpDialog.MarkUp_Window(scenes_flag=True)
        # self.markup_win = MarkUpDialog.MarkUp_Window(scenes_flag=True, data_for_functions=data_for_functions)
        self.markup_win.show()

    def testing(self):
        # TODO testing function window
        # self.test_functions = FunctionTests()
        # self.test_functions.show()
        print(mod_temp_data.current_editing_event)
        # file = str(QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Mod Directory"))
        print('testing prorotype')
        # print(Glob_Var.functions_display)
        # print(str(Glob_Var.perks_and_stats))
        # self.templates['Adventures'].frame_fields['StatReq'].load_main_data()
        example_data = ["some link to file/filename.mp3"]
        return_data = {}
        # self.templates['Adventures'].frame_fields['Optional'].set_val(example_data)
        # self.templates['Adventures'].frame_fields['optional'].get_val(return_data)
        # print(str(Mod_Var.mod_data))
        # self.recent_save()
        # self.test_idx += 1
        # self.layout_templates.setCurrentIndex(1)
        # self.widgets_elements['Adventures'][1].hide()
        # print(str(Mod))
        #TODO  testinng createfile - how does layouting works
        # example_field = {"numeric": {"type":"int",
			# 		"default":0
        # }}
        # test_layout = QtWidgets.QVBoxLayout()
        # test = QtWidgets.QLabel()
        # test.setText('test some more text here ')
        # test_layout.addWidget(test)
        # self.widgets_elements['Adventures'][1].setLayout(test_layout)

        # for field in example_field:
        #     created_field = createField(self.widgets_elements['Adventures'][1], field, example_field[field])
        #     created_field.set_up_widget(test_layout)
        # self.adjustSize()
        # self.centralwidget.adjustSize()
        # self.MainWindow.adjustSize()



# this is working, but cannot modify dialog window
# class Dialog_Visual_Options(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         loadUi("VisualOptions.ui", self)



class Dialog_Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("QMainWindow")

