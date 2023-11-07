import sys
from PyQt5 import QtWidgets
import MGUPrototype1
import LoadMod
from otherFunctions import load_json_data, write_json_data, check_if_file_exists, check_if_folder_exists\
    , get_file_time_modification
from GlobalVariables import Glob_Var, Mod_Var


def config_setup(label_widget, on_off, main_window=None):
    if on_off:
        label_widget.mousePressEvent = lambda event, arg1=label_widget, arg2=main_window: load_config_data(arg1, arg2)
        label_widget.setText("Game folder not found.\nClick me and select game folder")
    else:
        label_widget.mousePressEvent = None
        mWindow.change_icon()


def load_config_data(label_widget, main_window=None):
    if not Glob_Var.start_path:
        file = str(QtWidgets.QFileDialog.getExistingDirectory(main_window, "Select Directory"))
        if not file:
            return
        Glob_Var.start_path = file + '/'
    # label_widget.setText("Loading")
    # Glob_Var.start_path = file + '/'
    main_file_time_date = get_file_time_modification(Glob_Var.start_path + 'game/Json')
    if Glob_Var.main_modification_date == main_file_time_date:
        Glob_Var.main_game_items = load_json_data('files/_main_game_items.json')
        # with open('files/_main_game_items.json', encoding='utf-8') as file:
        #     # Glob_Var.main_game_items = json.load(file)
        # with open('files/_main_game_data.json', encoding='utf-8') as file:
        #     Glob_Var.main_game_data = json.load(file)
        Glob_Var.main_game_data = load_json_data('files/_main_game_data.json')
    else:
        load_data = ["Events", "Items", "Monsters", "Perks", "Skills"]
        for elements in load_data:
            Glob_Var.main_game_items[elements] = {'data': {}, 'path': []}
            LoadMod.load_main_game_item(main_path=Glob_Var.start_path + 'game/Json/' + elements,
                                        element_type=elements,
                                        main_var=Glob_Var.main_game_items[elements]['path'])
        # with open('files/_main_game_items.json', 'w', encoding='utf-8') as file:
        #     json.dump(Glob_Var.main_game_items, file)
        write_json_data('files/_main_game_items.json', Glob_Var.main_game_items)
        # with open('files/_main_game_data.json', 'w', encoding='utf-8') as file:
        #     json.dump(Glob_Var.main_game_data, file)
        write_json_data('files/_main_game_data.json', Glob_Var.main_game_data)
        # with open('config.ini', 'w', encoding='utf-8') as file2:
        #     temp_dict = {
        #         'path': Glob_Var.start_path,
        #         'log': Glob_Var.file_log,
        #         'main_modification': main_file_time_date,
        #         "label_font_type": Glob_Var.current_label_font_type,
        #         "label_font_size": Glob_Var.current_label_font_size,
        #         "text_font_type": Glob_Var.current_text_font_type,
        #         "text_font_size": Glob_Var.current_text_font_size,
        #         "testing": False
        #     }
        #     json.dump(temp_dict, file2)
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
        write_json_data('config.ini', temp_dict)
    if not Glob_Var.test_flag:
        LoadMod.load_perks_and_stats()
        # LoadMod.load_main_skill_types()
        LoadMod.load_fetishes()
        LoadMod.load_line_triggers()
        LoadMod.load_main_optional_fields()
        LoadMod.load_functions()
    LoadMod.load_drop_down_options()
    mWindow.tree_mod_elements.setModel(mWindow.tree_mod_elements.additions_model)
    LoadMod.load_main_game_addition(main_tree=mWindow.tree_mod_elements)
    mWindow.tree_mod_elements.setModel(mWindow.tree_mod_elements.tree_model)
    label_widget.setText("Welcome")
    config_setup(label_widget, 0)
    mWindow.tree_mod_elements.add_data(data=Mod_Var.mod_display)
    mWindow.tree_mod_elements.disable_roots()
    LoadMod.new_mod()
    mWindow.main_game_elements.add_main_game_items()


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
        mWindow.recent_save()
        app.closeAllWindows()
        # super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    # window = QtWidgets.QMainWindow()
    mWindow = MGUPrototype1.Ui_MainWindow(window)
    mWindow.setupUi()
    # print('load gui')
    # window.setMinimumSize(300, 600)

    if not check_if_file_exists('config.ini'):
        mWindow.actionMain_Status.setEnabled(False)
        config_setup(mWindow.label_welcome, 1, mWindow.centralwidget)
    else:
        basic_configuration = load_json_data('config.ini')
        Glob_Var.start_path = basic_configuration['path']
        if not check_if_folder_exists(Glob_Var.start_path, create=False):
            """when i test it and forget to delete config"""
            mWindow.actionMain_Status.setEnabled(False)
            config_setup(mWindow.label_welcome, 1, mWindow.centralwidget)
        else:
            Glob_Var.file_log = basic_configuration['log']
            Glob_Var.main_modification_date = basic_configuration['main_modification']
            Glob_Var.current_label_font_type = basic_configuration['label_font_type']
            Glob_Var.current_label_font_size = basic_configuration['label_font_size']
            Glob_Var.current_text_font_type = basic_configuration['text_font_type']
            Glob_Var.current_text_font_size = basic_configuration['text_font_size']
            Glob_Var.test_flag = basic_configuration['testing']
            load_config_data(mWindow.label_welcome, mWindow.centralwidget)
        mWindow.prepare_templates_space()
    window.show()
    sys.exit(app.exec())

    # convert ui into python
    # pyuic5 xyz.ui -o xyz.py
