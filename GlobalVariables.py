import copy

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.Qt import QStandardItemModel

# TODO there will be problem with functions loading for:
# ChangeImageLayer
# 'AddMonsterToEncounter'
#
#

elements = {
    "Adventures": {},
    "Events": {},
    "Fetishes": {},
    "Items": {},
    "Locations": {},
    "Monsters": {},
    "Perks": {},
    "Skills": {}
}
# start_path = ''
# main_modification_date = ''

currentSelectedItem = {}
currentSelectedItem['text'] = ''
currentSelectedItem['type'] = ''
currentSelectedItem['tags'] = []
# type - should be adv, event or other element type
# data - data from treeview
modified_flag = False

class GlobalVariable:
    def __init__(self):
        self.access_templates = None
        self.edit_element = False
        self.edit_status_icon = None
        self.save_element_action = None
        self.cancel_element_action = None
        self.file_log = False
        self.test_flag = False
        self.functions_display = {}
        self.functions_data = {}
        self.game_hard_data = {'statusEffects':{},
                               'core stats':{
                                   'simple': ['Power', 'Technique', 'Intelligence', 'Allure', 'Willpower', 'Luck'],
                                   'percente': ['%Power', '%Technique', '%Intelligence', '%Allure', '%Willpower', '%Luck'],
                                   'sensitivity': ["Sex", "Ass", "Breasts", "Mouth", "Seduction", "Magic", "Pain",
                                                   "Energy", "Holy", "Unholy"]}}
        self.line_trigger_display_data = {}
        self.lineTriggers = {}
        """mainGameItems is expected to be: 
        "Adventures": {files:[]},
        "Events": {foldername1:[], folder2:{insidefolderagain:[]}, files:[]},
        "Items": {keyitesm:[], consumables:[], files:[]},
        where files dictionary  is usually stuff in main folders
        """
        self.main_game_items = {'Events': {},
                                'Skills': {},
                                'Fetishes': {'Fetish': {},
                                             'Addiction': {}}
                                }
        self.main_game_field = None
        self.main_game_data = {'Girls': {}, 'Items': {}, "Perks": {}, "Skills": {}}
        self.main_game_additions = ['Events', 'Monsters', 'Skills']
        """main game tree model. it's used in main window and function window, essentialy should have same data"""
        self.main_game_tree_model = QStandardItemModel()
        self.main_game_sorting = QSortFilterProxyModel()
        self.main_game_sorting.setSourceModel(self.main_game_tree_model)
        self.main_game_sorting.setRecursiveFilteringEnabled(True)
        self.display_elements_game_and_mod = {}  # its this one for main game display. each main game have its own list separate, so same model tree does not make sense
        """"""
        self.main_modification_date = '0'
        self.mod_main_switch = 'game/Mods/'
        self.perks_and_stats = {'PerkType': {},
                                'StatReq': {}}
        self.skill_type_fields = {}
        self.skills_single_target = []
        self.stances = {}
        self.start_path = ''
        # self.status_effects2 = {}
        self.optional_fields = {}
        self.optional_frame = None
        self.optional_field = None

        self.current_label_font_type = 'Ariel'
        self.current_label_font_size = 14
        self.current_text_font_type = 'Ariel'
        self.current_text_font_size = 14

        self.flag_skip_functions = False
        """flag addition - used when clicking button to display maingame files. then, when clicking to modify fields,
         it checks global flag. if no, will not allow to edit fields that does not have flag addition"""
        self.flag_addition = False
        self.flag_modify_addition = False
        self.flag_window_edit_data = False



        # self.List_buttons = []
        # self.list_elementlists = []
        self.list_dataFrames = {}
        # self.current_mod = {
        #     "Adventures": {},
        #     "Events": {},
        #     "Fetishes": {},
        #     "Items": {'test123': {'name': 'test123', 'descrip': '123123', 'itemType': 'Rune'},
        #               'testKey': {'name': 'testKey', 'descrip': '123123', 'itemType': 'Key'}},
        #     # "Items": {},
        #     "Locations": {},
        #     "Monsters": {},
        #     "Perks": {},
        #     "Skills": {}
        # }

        # load line triggers
        # temp = load_json_data('files/_lineTriggers.json')
        # for val1 in temp:
        #     temp_list = list(temp[val1].keys())
        #     self.line_trigger_display_data[val1] = temp_list
            # for val2 in temp[val1]:
            #     self.lineTriggers[val2] = temp[val1][val2]
        # load stances
        # temp = load_json_data('files/_stances.json')
        # self.stances = temp

        #

    def get_functions(self, function_name):
        function_data = copy.copy(self.functions_data[function_name])
        print('retrievieg function data')
        print(function_data)
        return function_data
    def edited_field(self):
        # print('test if edited field - global variable def')
        if self.edit_element:
            self.save_element_action.setEnabled(True)
            self.cancel_element_action.setEnabled(True)
            self.edit_status_icon.setEnabled(False)

    def check_stances(self, custom_stance_list=list):
        for stance_type in self.stances:
            for stance in self.stances[stance_type]:
                if stance in custom_stance_list:
                    custom_stance_list.remove(stance)

    def function_steps_no(self, function_name):
        if function_name in self.functions_data:
            if len(self.functions_data[function_name]['steps']) > 2:
                temp = self.functions_data[function_name]['steps'].split('-')
                if len(temp) > 1:
                    """there is number which should mean which field from the ending should have endloop
                    i need this as minus number, and counting from last, last element
                     start at -1 so need to increase by 1"""
                    return (int(temp[1]) + 1) * -1
                else:
                    return temp[0]
            else:
                return int(self.functions_data[function_name]['steps']) - 1
        """if function not found, return 0"""
        return 0
    # def load_functions(self):
    #     file_data = load_json_data('files/_textfunction_all_2.json')
    #     if self.flag_skip_functions:
    #         temp = file_data.copy()
    #         for lvl1 in list(file_data.keys()):
    #             for lvl2 in list(file_data[lvl1].keys()):
    #                 temp_list = []
    #                 if '-done' in lvl2:
    #                     temp[lvl1].pop(lvl2)
    #                 else:
    #                     for lvl3 in file_data[lvl1][lvl2]:
    #                         if '-done' in lvl3['title']:
    #                             # temp[lvl1][lvl2].pop(data[lvl1][lvl2].index(lvl3))
    #                             # temp[lvl1][lvl2].remove(lvl3)
    #                             temp_list.append(file_data[lvl1][lvl2].index(lvl3))
    #                 if len(temp_list)>0:
    #                     temp_list.reverse()
    #                     for titles in temp_list:
    #                         temp[lvl1][lvl2].pop(titles)
    #         self.functions_data = temp
    #     else:
    #         for root_function in file_data:
    #             self.functions_display[root_function] = {}
    #             for function_type in file_data[root_function]:
    #                 self.functions_display[root_function][function_type] = []
    #                 for idx in range(function_type.length()):
    #                     function_title = file_data[root_function][function_type][idx].title
    #                     self.functions_display[root_function][function_type].append(function_title)
    #                     self.functions_data[function_title] = file_data[root_function][function_type][idx]


Glob_Var = GlobalVariable()

# class for holding mod data. Here it will load files data into mod variable as dictionary with filename as keys.
# each filename must be unique. Folders are just for visibility, so as in other aspects, keep it separate in display var
class ModVariable(object):
    def __init__(self):
        self.clear_mod = {
                "Adventures": {},
                "Events": {},
                "Fetishes": {},
                # "Items": {'test123': {'name': 'test123', 'descrip':'123123', 'itemType': 'Rune'}, 'testKey': {'name': 'testKey', 'descrip':'123123', 'itemType': 'Key'}},
                "Items": {},
                "Locations": {},
                "Monsters": {},
                "Perks": {},
                "Skills": {}
            }
        # self.mod_data.copy = mod
        self.mod_data = copy.copy(self.clear_mod)
        self.mod_display = copy.copy(self.clear_mod)
        self.mod_file_names = copy.copy(self.clear_mod)
        # self.mod_display = {
        #         "Adventures": {},
        #         "Events": {},
        #         "Fetishes": {},
        #         "Items": [{'folder 1':['file a','file b']}, {'folder 2':['file c','file d']}, 'test123', 'testKey'],
                # "Items": {},
                # "Locations": {},
                # "Monsters": {},
                # "Perks": {},
                # "Skills": {}
            # }

    def clear_mod(self):
        # for element in self.mod_data:
        self.mod_data = copy.copy(self.clear_mod)
        self.mod_display = copy.copy(self.clear_mod)
    # def load_mod_data_part1(self):
        # for element in self.mod_data:
        #     if element == 'Fetishes':
        #         if access(mod_path + '/Fetishes/0fetishList.json', F_OK):
        #             with open(mod_path + '/Fetishes/0fetishList.json', encoding='utf-8-sig') as file:
        #                 temp_dict = json.load(file, object_hook=OrderedDict)
        #                 for fetishes_dictionary in temp_dict['FetishList']:
        #                     GlobalVariables.current_mod['Fetishes'][
        #                         fetishes_dictionary['Name']] = fetishes_dictionary
        #                     GlobalVariables.list_elementlists[2].add_leaves('', [fetishes_dictionary['Name']],
        #                                                                     update_flag=False)
        #         if access(mod_path + '/Fetishes/addictionList.json', F_OK):
        #             with open(mod_path + '/Fetishes/addictionList.json', encoding='utf-8-sig') as file:
        #                 temp_dict = json.load(file, object_hook=OrderedDict)
        #                 for fetishes_dictionary in temp_dict['FetishList']:
        #                     GlobalVariables.current_mod['Fetishes'][
        #                         fetishes_dictionary['Name']] = fetishes_dictionary
        #                     GlobalVariables.list_elementlists[2].add_leaves('', [fetishes_dictionary['Name']],
        #                                                                     update_flag=False)
        #     else:
        #         if access(mod_path + '/' + element + '/', F_OK):
        #             for index in range(len(GlobalVariables.list_elementlists)):
        #                 # get list heading and thus number in order of visible list
        #                 listName = GlobalVariables.list_elementlists[index].treeview.heading('#0')['text']
        #                 # GlobalVariables.list_elementlists[index].clear_tree()
        #                 if listName == element:
        #                     list_No = index
        #                     break
        #             # GlobalVariables.list_elementlists[list_No].clear_tree()
        #             load_item(mod_path + '/' + element + '/', element, list_number=list_No)

Mod_Var = ModVariable()
# Mod_Var.clear_mod()
# print('loaded mod var')
