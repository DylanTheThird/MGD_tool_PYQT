import sys
from os import access, F_OK
from os.path import getmtime
import json

from PyQt5 import QtWidgets
import MGUPrototype1
import LoadMod
from GlobalVariables import Glob_Var, Mod_Var


def config_setup(label_widget, on_off, main_window=None):
    if on_off:
        label_widget.mousePressEvent = lambda event, arg1=label_widget, arg2=main_window: load_config_data(arg1, arg2)
        label_widget.setText("Game folder not found.\nClick me and select game folder")
    else:
        label_widget.mousePressEvent = None
        prototype.change_icon()


def load_config_data(label_widget, main_window=None):
    if not Glob_Var.start_path:
        file = str(QtWidgets.QFileDialog.getExistingDirectory(main_window, "Select Directory"))
        if not file:
            return
        Glob_Var.start_path = file + '/'
    label_widget.setText("Loading")
    # Glob_Var.start_path = file + '/'
    main_file_time_date = getmtime(Glob_Var.start_path + 'game/Json')
    if Glob_Var.main_modification_date == main_file_time_date:
        with open('files/_main_game_items.json', encoding='utf-8') as file:
            Glob_Var.main_game_items = json.load(file)
        with open('files/_main_game_data.json', encoding='utf-8') as file:
            Glob_Var.main_game_data = json.load(file)
    else:
        load_data = ["Events", "Items", "Monsters", "Perks", "Skills"]
        for elements in load_data:
            Glob_Var.main_game_items[elements] = {'data': {}, 'path': []}
            LoadMod.load_main_game_item_2(main_path=Glob_Var.start_path + 'game/Json/' + elements,
                                          element_type=elements,
                                          main_var=Glob_Var.main_game_items[elements]['path'])
        with open('files/_main_game_items.json', 'w', encoding='utf-8') as file:
            json.dump(Glob_Var.main_game_items, file)
        with open('files/_main_game_data.json', 'w', encoding='utf-8') as file:
            json.dump(Glob_Var.main_game_data, file)
        # LoadMod.load_main_game_item(main_path=GlobalVariables.startPath + 'game/Json')
        with open('config.ini', 'w', encoding='utf-8') as file2:
            temp_dict = {
                'path': Glob_Var.start_path,
                'log': Glob_Var.file_log,
                'main_modification': main_file_time_date,
                "label_font_type": Glob_Var.current_label_font_type,
                "label_font_size": Glob_Var.current_label_font_size,
                "text_font_type": Glob_Var.current_text_font_type,
                "text_font_size": Glob_Var.current_text_font_size,
                "testing": False
            }
            json.dump(temp_dict, file2)
    if not Glob_Var.test_flag:
        LoadMod.load_perks_and_stats()
        LoadMod.load_main_skill_types()
        LoadMod.load_fetishes()
        # LoadMod.load_status_effect()
        LoadMod.load_line_triggers()
        LoadMod.load_main_optional_fields()
        LoadMod.load_functions()
        # LoadMod.load_stances()
    LoadMod.load_drop_down_options()
    prototype.tree_mod_elements.setModel(prototype.tree_mod_elements.additions_model)
    LoadMod.load_main_game_addition(main_tree=prototype.tree_mod_elements)
    prototype.tree_mod_elements.setModel(prototype.tree_mod_elements.tree_model)
    label_widget.setText("Welcome")
    config_setup(label_widget, 0)
    prototype.tree_mod_elements.add_data(data=Mod_Var.mod_display)
    prototype.tree_mod_elements.disable_roots()
    LoadMod.new_mod()
    # prototype.prepare_same_core_elements_in_both_displayes()
    prototype.main_game_elements.add_main_game_items()


def testing():
    print('test')
    # print(str(Mod_Var.mod_display))
    # print(str(Mod_Var.mod_data))
    print(str(Glob_Var.main_game_items))
    # Mod_Var.mod_display['Items'] = {"teste1":"test2"}
    # if tmp:
    #     prototype.actionMain_Status.setEnabled(False)
    #     tmp=0
    # else:
    #     prototype.actionMain_Status.setEnabled(True)
    #     tmp=1


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        # self.setCentralWidget(QtWidgets.QLabel("I'm the Central Widget"))

    def closeEvent(self, event):
        # print('closing')
        prototype.recent_save()
        app.closeAllWindows()
        # super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    # window = QtWidgets.QMainWindow()
    prototype = MGUPrototype1.Ui_MainWindow(window)
    prototype.setupUi()
    # print('load gui')
    # window.setMinimumSize(300, 600)
    # for testing purpos
    # prototype.button_test.clicked.connect(prototype.testing)
    # prototype.button_test.clicked.connect(prototype.testing)

    if not access('config.ini', F_OK):
        prototype.actionMain_Status.setEnabled(False)
        config_setup(prototype.label_welcome, 1, prototype.centralwidget)
    else:
        with open('config.ini', 'r') as configuration:
            basic_configuration = json.load(configuration)
            Glob_Var.start_path = basic_configuration['path']
            if not access(Glob_Var.start_path, F_OK):
                """when i test it and forget to delete config"""
                prototype.actionMain_Status.setEnabled(False)
                config_setup(prototype.label_welcome, 1, prototype.centralwidget)
            else:
                Glob_Var.file_log = basic_configuration['log']
                Glob_Var.main_modification_date = basic_configuration['main_modification']
                Glob_Var.current_label_font_type = basic_configuration['label_font_type']
                Glob_Var.current_label_font_size = basic_configuration['label_font_size']
                Glob_Var.current_text_font_type = basic_configuration['text_font_type']
                Glob_Var.current_text_font_size = basic_configuration['text_font_size']
                Glob_Var.test_flag = basic_configuration['testing']
                load_config_data(prototype.label_welcome, prototype.centralwidget)
    prototype.prepare_templates_space()
    window.show()
    sys.exit(app.exec())

    # convert ui into python
    # pyuic5 xyz.ui -o xyz.py
