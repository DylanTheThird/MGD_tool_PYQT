# from tkinter import messagebox
from os import listdir
from os import access, F_OK, mkdir, rename
from os.path import isdir, join, isfile, getmtime
import json
from collections import OrderedDict
# import GlobalVariables
from GlobalVariables import Glob_Var, Mod_Var
# from GlobalVariables import Glob_Var
from otherFunctions import wrap

# global Mod_Var


def check_if_mod_exists(mod_path):
    """check if mod exists"""
    if access(mod_path, F_OK):
        return True
    else:
        return False

def start_loading_mod(mod_path):
    for element in Mod_Var.mod_data:
        Mod_Var.mod_data[element] = {}
        Mod_Var.mod_data[element] = {}
        if element == 'Fetishes':
            Mod_Var.mod_display['Fetishes'] = []
            if access(mod_path + '/Fetishes/0fetishList.json', F_OK):
                with open(mod_path+'/Fetishes/0fetishList.json', encoding='utf-8-sig') as file:
                    temp_dict = json.load(file, object_hook=OrderedDict)
                    for fetishes_dictionary in temp_dict['FetishList']:
                        Mod_Var.mod_data['Fetishes'][fetishes_dictionary['Name']] = fetishes_dictionary
                        Mod_Var.mod_display['Fetishes'].append(fetishes_dictionary['Name'])
            if access(mod_path + '/Fetishes/addictionList.json', F_OK):
                with open(mod_path+'/Fetishes/addictionList.json', encoding='utf-8-sig') as file:
                    temp_dict = json.load(file, object_hook=OrderedDict)
                    for fetishes_dictionary in temp_dict['FetishList']:
                        Mod_Var.mod_data['Fetishes'][fetishes_dictionary['Name']] = fetishes_dictionary
                        Mod_Var.mod_display['Fetishes'].append(fetishes_dictionary['Name'])
        else:
            if access(mod_path + '/' + element + '/', F_OK):
                # temp = {}
                temp = []
                load_item(mod_path + '/' + element, element, list_parent=temp)
                Mod_Var.mod_display[element] = temp



def load_item(mod_path, element_type='', depth=0, list_parent=None):
    # list_parent should be ModVar.mod_display
    # read all items from mod path and load  json data into current mod
    # also, load data display var which later will be inserted into main treeview
    if not access(mod_path, F_OK):
        return
    mod_files = [f for f in listdir(mod_path) if isfile(join(mod_path, f))]
    mod_directories = [f for f in listdir(mod_path) if isdir(join(mod_path, f))]
    for element in mod_directories:
        # if depth is 0 -  we just entered element
        # if depth = 1, then we are scanning directories in root folders, but list is already in root folder.
        # if deeper, add folder and pass that folder recursively
        # new_parent = list_parent + '/' + element
        new_folder = {element: []}
        list_parent.append(new_folder)
        # list_parent[element] = {}
        load_item(mod_path + '/' + element, element_type, depth + 1, new_folder[element])
        # load_item(mod_path + '/' + element, element_type, depth + 1, list_parent[element])
    # if list_parent:
        # new_parent = GlobalVariables.list_elementlists[list_number].treeview.insert('', 'end', [list_parent], text=list_parent)
        # new_parent = prepare_folders(list_parent)
    # else:
    #     new_parent = ''
    if mod_files:
        # for index in range(len(mod_files)-1, -1, -1):
        #     if mod_files[index][0] == '_':
        #         mod_files.pop(index)
        # list_parent['files'] = []
        for file_names in mod_files:
            if file_names[0] == '_':
                continue
            # print(files)
            # now it names stuff in current mod var with filename, but it might be different then element name
            # lets change to take name of element and that will be the key in currentModVar.
            with open(mod_path+'/'+file_names, encoding='utf-8-sig') as file:
                file_data = json.load(file, object_hook=OrderedDict)
                # current_mod[element_type][files[:-5]] = file_data
                # name = file_names[:-5]
                if element_type == 'Monsters':
                    name = file_data['IDname']
                else:
                    name = file_data['name']
                # list_parent['files'].append(name)
                list_parent.append(name)
                Mod_Var.mod_data[element_type][name] = file_data
                Mod_Var.mod_file_names[element_type][name] = file_names[:-5]
                # new_item = GlobalVariables.list_elementlists[list_number].treeview.insert(new_parent, 'end', [name], text=name)
                # GlobalVariables.list_elementlists[list_number].add_leaves(new_parent, [name], update_flag=False)

def new_mod():
    for element in Mod_Var.mod_data:
        Mod_Var.mod_data[element] = {}
        Mod_Var.mod_display[element] = {}
        Mod_Var.mod_file_names[element] = {}

# def load_item(mod_path, element_type='', current_mod='', list_number=0, depth=0, list_parent=''):
#     # print('')
#     # read all items from mod path and load  json data into current mod
#     # also, load data into the list along with directories
#     mod_files = [f for f in listdir(mod_path) if isfile(join(mod_path, f))]
#     mod_directories = [f for f in listdir(mod_path) if isdir(join(mod_path, f))]
#     for element in mod_directories:
#         if depth == 0:
#             # get list index number. need to  check columns name  with elelemtn
#             for index in range(len(GlobalVariables.list_elementlists)):
#                 # get list heading and thus number in order of visible list
#                 listName = GlobalVariables.list_elementlists[index].treeview.heading('#0')['text']
#                 if listName == element:
#                     list_number = index
#                     break
#         # if depth is 0 -  we are at root, cant add root to root
#         # if depth = 1, then we are scanning directories in root folders, but list is already in root folder.
#         # if deeper, add folder and pass that folder recursively
#         if depth:
#             if depth > 1:
#                 new_parent = GlobalVariables.list_elementlists[list_number].treeview.insert(list_parent, 'end', [element], text=element)
#             else:
#                 new_parent = GlobalVariables.list_elementlists[list_number].treeview.insert('', 'end', [element], text=element)
#         else:
#             new_parent = ''
#         if mod_path.count('/') <= 2:
#             element_type = element
#         load_item(mod_path + '/' + element, element_type, current_mod, list_number, depth + 1, new_parent)
#     if mod_files:
#         for index in range(len(mod_files)-1, -1, -1):
#             if mod_files[index][0] == '_':
#                 mod_files.pop(index)
#         for files in mod_files:
#             # print(files)
#             # now it names stuff in current mod var with filename, but it might be different then element name
#             # lets change to take name of element and that will be the key in currentModVar.
#             with open(mod_path+'/'+files) as file:
#                 file_data = json.load(file, object_hook=OrderedDict)
#                 # current_mod[element_type][files[:-5]] = file_data
#                 name = file_data['name']
#                 current_mod[element_type][name] = file_data
#                 # if depth>1:
#                 GlobalVariables.list_elementlists[list_number].treeview.insert(list_parent, 'end', [name], text=name)
#                 # else:
#                 #     GlobalVariables.list_elementlists[list_number].treeview.insert('', 'end', [name], text=name)


def check_if_folder_exists(listNO, folders, curr_folder_iid=''):
    """get list of children, for each leaf check if it has folder tag. if yes, check if its name is same as
    the on in filepath. lets hope they wont repeat. if same, delete if from folder list, since we found it,
     check if it was last folder, if not, enter and repeat. if yes, return"""
    leaves = GlobalVariables.list_elementlists[listNO].treeview.get_children(curr_folder_iid)
    for leaf in leaves:
        if 'folder' in GlobalVariables.list_elementlists[listNO].treeview.item(leaf)['tags']:
            if folders[0] == GlobalVariables.list_elementlists[listNO].treeview.item(leaf)['text']:
                folders.pop(0)
                if len(folders)==0:
                    return leaf
                curr_folder_iid = check_if_folder_exists(listNO, folders, leaf)
                return curr_folder_iid
    return curr_folder_iid

def prepare_folders(list_no, files_path):
    """divide files path into seperate folders. value should be /folder1/folder2/ so also delete first and last element"""
    folders = files_path.split('/')
    folders.pop(0)
    # folders.pop(-1)
    curr_folder = check_if_folder_exists(list_no, folders)
    """for each folder, add that folder to list. then add folder to previous folder.
        But do so only if folder does not exists."""
    for folder in folders:
            curr_folder = GlobalVariables.list_elementlists[list_no].treeview.insert(curr_folder, 'end', [folder+'_'+curr_folder], text=folder)
            GlobalVariables.list_elementlists[list_no].treeview.item(curr_folder, tags='folder')

    return curr_folder


# obsolete?
def load_mod_elements(current_mod):
    # if loadItem works, loadMoadElements is obsolete, but might still be usefull for element types
    # load data from current_mod into the lists
    index = 0
    for element_type in current_mod:
        # print(element_type)
        for seperate_elelements in current_mod[element_type]:
            # print(current_mod[element_type][seperate_elelements])
            if element_type == 'Adventures':
                # for adventures, load name from file as branch and decription as leaf
                adventure_name = current_mod[element_type][seperate_elelements]['name']
                adventure_description = [wrap(current_mod[element_type][seperate_elelements]['Description'])]
                GlobalVariables.list_elementlists[index].add_branch(adventure_name, adventure_description)
            # if element_type == 'Events': # for event, load name from file as branch and card type as leaf
                # adventure_name = current_mod[element_type][seperate_elelements]['name']
                # adventure_description = [wrap(current_mod[element_type][seperate_elelements]['Description'])]
                # GlobalVariables.list_elementlists[index].add_branch(adventure_name, adventure_description)
            if element_type == 'Items':
                # print(current_mod[element_type][seperate_elelements]['itemType'])
                # print(current_mod[element_type][seperate_elelements]['name'])
                # for items, branch is item type, and leaf is item name
                templist = [current_mod[element_type][seperate_elelements]['name']]
                GlobalVariables.list_elementlists[index].add_branch(current_mod[element_type][seperate_elelements]['itemType'], templist)
            if element_type == 'Fetishes':
                # for fetish, only add fetish name
                GlobalVariables.list_elementlists[index].add_branch(current_mod[element_type][seperate_elelements]['name'], [])


        index+=1


def load_item_backup(mod_path, element_type='', current_mod=''):
    # print('')
    # read all items from mod path and load  json data into current mod
    mod_files = [f for f in listdir(mod_path) if isfile(join(mod_path, f))]
    mod_directories = [f for f in listdir(mod_path) if isdir(join(mod_path, f))]
    for element in mod_directories:
        if mod_path.count('/') <= 1:
            element_type = element
        load_item(mod_path + '/' + element, element_type, current_mod)
    if mod_files:
        for index in range(len(mod_files)-1, -1, -1):
            if mod_files[index][0] == '_':
                mod_files.pop(index)
    for files in mod_files:
        # print(files)
        # now it names stuff in current mod var with filename, but it might be different then element name
        # lets change to take name of element and that will be the key in currentModVar.
        with open(mod_path+'/'+files) as file:
            file_data = json.load(file, object_hook=OrderedDict)
            # current_mod[element_type][files[:-5]] = file_data
            name = file_data['name']
            current_mod[element_type][name] = file_data


def load_main_game_item_2(main_path='./../json', element_type='', main_var=None):
    """ this should load main game data into global variable, to use later in other fields where you choose items """
    mod_directories = [f for f in listdir(main_path) if isdir(join(main_path, f))]
    # print(mod_files)
    # print(mod_directories)
    # recursive go into folders until no more folder available
    for element in mod_directories:
        temp_dict = {element: []}
        main_var.append(temp_dict)
        load_main_game_item_2(main_path + '/' + element, element_type, main_var[-1][element])
    mod_files = [f for f in listdir(main_path) if isfile(join(main_path, f))]
    for file in mod_files:
        if file[0] != '_':
            main_var.append(file[:-5])
    load_main_game_files_data(main_path)


def load_main_game_files_data(file_path=''):
    mod_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    """open each file. usually only need name from file, but in some cases also need scene text or maybe something else.
    so final list usually is list of file names or dictionaries with file name and more stuff inside  to choose from """
    for file_data in mod_files:
        if file_data[0] == '_':
            continue
        # print(str(main_item_dict))
        # try:
        with open(file_path + '/' + file_data, encoding='utf-8') as file:
            files = file_data[:-5]
            file_data = json.load(file, object_hook=OrderedDict)
            if 'Fetishes' in file_path:
                continue
            # name = file_data['name']
            # if name != ' ':
            if 'Events' in file_path:
                temp_scene_list = []
                for scenes in file_data['EventText']:
                    # TODO might need to add to search to choices too
                    temp_scene_list.append(scenes['NameOfScene'])
                Glob_Var.main_game_items['Events']['data'][files] = temp_scene_list
            elif 'Monsters' in file_path:
                # name = file_data['IDname']
                scene_list = {}
                loss_scene_list = []
                victory_scene_list = []
                for scenes in file_data['lossScenes']:
                    loss_scene_list.append(scenes['NameOfScene'])
                for scenes in file_data['victoryScenes']:
                    victory_scene_list.append(scenes['NameOfScene'])
                scene_list['lossScenes'] = loss_scene_list
                scene_list['victoryScenes'] = victory_scene_list
                scene_list['generic'] = file_data['generic']
                scene_list['skillList'] = file_data['skillList']
                scene_list['pictures'] = file_data['pictures']
                # temp_file_list.append({name: scene_list})
                """new organization. file data in main_game_data. later change main_game_item_data to only have path display"""
                girl_data = {'lossScenes': loss_scene_list, 'victoryScenes': victory_scene_list,
                             'generic': file_data['generic'], 'skillList': file_data['skillList']}
                # GlobalVariables.main_game_data['Girls'][files] = girl_data
                Glob_Var.main_game_data['Girls'][file_data['IDname']] = girl_data

            elif 'Fetish' in file_path:
                continue
            elif 'Skills' in file_path:
                Glob_Var.main_game_items['Skills']['data'][files] = {'skillTags': file_data['skillTags'],
                                                                     'fetishTags': file_data['fetishTags'],
                                                                     'targetType': file_data['targetType']}
                # GlobalVariables.main_game_items['Skills_Data'][name] = {'skillTags': file_data['skillTags'],
                #                                                         'fetishTags': file_data['fetishTags']}
                # temp_file_list.append(name)

            # else:
            #     temp_file_list.append(name)
    # except UnicodeDecodeError as json_load_error:
    #     print(json_load_error.object)
    # print('something  wrong with ' + files)

    return


def load_main_skill_types():
    with open('files/_skilltypefields.json', encoding='utf-8') as file:
        file_data = json.load(file, object_hook=OrderedDict)
        for field in file_data:
            Glob_Var.skill_type_fields[field] = file_data[field]


def load_fetishes():
    # GlobalVariables.main_game_items["Fetishes"] = {}
    # GlobalVariables.main_game_items["Fetishes"]['Fetish'] = {}
    # GlobalVariables.main_game_items["Fetishes"]['Addiction'] = {}
    with open(Glob_Var.start_path + 'game/json/Fetishes/0fetishList.json', encoding='utf-8') as file:
        file_data = json.load(file, object_hook=OrderedDict)
        for element in file_data:
            for fetish in file_data[element]:
                Glob_Var.main_game_items["Fetishes"]['Fetish'][fetish['Name']] = fetish
    with open(Glob_Var.start_path + 'game/json/Fetishes/addictionList.json', encoding='utf-8') as file:
        file_data = json.load(file, object_hook=OrderedDict)
        for element in file_data:
            for fetish in file_data[element]:
                Glob_Var.main_game_items["Fetishes"]['Addiction'][fetish['Name']] = fetish
    # del GlobalVariables.main_game_items["Fetishes"]["files"]


def load_main_optional_fields():
    with open('files/_optional_fields.json', encoding='utf-8') as file:
        file_data = json.load(file, object_hook=OrderedDict)
        for field in file_data:
            Glob_Var.optional_fields[field] = file_data[field]


def load_perks_and_stats():
    # GlobalVariables.perks_and_stats
    with open('files/_perktypes.json') as file:
        file_data = json.load(file, object_hook=OrderedDict)
    Glob_Var.perks_and_stats['PerkType'] = file_data
    with open('files/_stats.json') as file:
        file_data = json.load(file, object_hook=OrderedDict)
    Glob_Var.perks_and_stats['StatReq'] = file_data


def load_status_effect():
    with open('files/_statuseffects.json') as file:
        file_data = json.load(file, object_hook=OrderedDict)
    # GlobalVariables.status_effects2 = file_data
    Glob_Var.game_hard_data['statusEffects'] = file_data


def load_functions():
    if Glob_Var.test_flag:
        functions_path = 'files/_textfunction_testing.json'
    else:
        functions_path = 'files/_textfunction.json'
    with open(functions_path) as file:
        # GlobalVariables.functions_data = json.load(file, object_hook=OrderedDict)
        # testing
        data = json.load(file, object_hook=OrderedDict)
        if Glob_Var.flag_skip_functions:
            temp = data.copy()
            for lvl1 in list(data.keys()):
                for lvl2 in list(data[lvl1].keys()):
                    temp_list = []
                    if '-done' in lvl2:
                        temp[lvl1].pop(lvl2)
                    else:
                        for lvl3 in data[lvl1][lvl2]:
                            if '-done' in lvl3['title']:
                                # temp[lvl1][lvl2].pop(data[lvl1][lvl2].index(lvl3))
                                # temp[lvl1][lvl2].remove(lvl3)
                                temp_list.append(data[lvl1][lvl2].index(lvl3))
                    if len(temp_list)>0:
                        temp_list.reverse()
                        for titles in temp_list:
                            temp[lvl1][lvl2].pop(titles)
            Glob_Var.functions_data = temp
        else:
            # GlobalVariables.functions_data = json.load(file, object_hook=OrderedDict)
            for root_function in data:
                Glob_Var.functions_display[root_function] = {}
                for function_type in data[root_function]:
                    Glob_Var.functions_display[root_function][function_type] = []
                    for idx in range(len(data[root_function][function_type])):
                        function_title = data[root_function][function_type][idx]['title']
                        Glob_Var.functions_display[root_function][function_type].append(function_title)
                        Glob_Var.functions_data[function_title] = data[root_function][function_type][idx]


def load_stances():
    with open('files/_stances.json') as file:
        Glob_Var.stances = json.load(file, object_hook=OrderedDict)


def load_line_triggers():
    with open('files/_lineTriggers.json') as file:
        # GlobalVariables.lineTriggers = json.load(file, object_hook=OrderedDict) # simple version
        temp = json.load(file, object_hook=OrderedDict)
        for val1 in temp:
            temp_list = list(temp[val1].keys())
            Glob_Var.line_trigger_display_data[val1] = temp_list
            for val2 in temp[val1]:
                Glob_Var.lineTriggers[val2] = temp[val1][val2]


def nest_folders_in_dictionary(folder_list, dictionary_to_nest, list_of_files_to_add):
    """ in case  we need to  switch from dictionary to list, but its not working."""
    # # if folder_list[0] not in dictionary_to_nest:
    # #     if len(folder_list) > 1:
    #         temp_dict = {folder_list[0]: []}
    #         # temp_dict[folder_list[0]] = []
    #         dictionary_to_nest.append(temp_dict)
    #         nest_folders_in_dictionary(folder_list[1:], dictionary_to_nest[folder_list[0]])
    #     # else:
    #     #     dictionary_to_nest[folder_list[0]] = []
    # # elif len(folder_list) > 1:
    # #     nest_folders_in_dictionary(folder_list[1:], dictionary_to_nest[folder_list[0]])
    if folder_list[0] not in dictionary_to_nest:
        if len(folder_list) > 1:
            dictionary_to_nest[folder_list[0]] = {}
            nest_folders_in_dictionary(folder_list[1:], dictionary_to_nest[folder_list[0]], list_of_files_to_add)
        else:
            # dictionary_to_nest[folder_list[0]] = list_of_files_to_add
            dictionary_to_nest[folder_list[0]] = {}
            dictionary_to_nest[folder_list[0]]['files'] = list_of_files_to_add
    elif len(folder_list) > 1:
        nest_folders_in_dictionary(folder_list[1:], dictionary_to_nest[folder_list[0]], list_of_files_to_add)
    else:
        if list_of_files_to_add:
            dictionary_to_nest[folder_list[0]]['files'] = list_of_files_to_add


def load_main_game_addition(main_path='game/json', folder='', main_tree=None):
    """ this should load main game data into global variable, to use later in other fields where you choose items """
    main_game_directories = [f for f in listdir(Glob_Var.start_path + main_path) if isdir(join(Glob_Var.start_path + main_path, f))]
    # print(mod_files)
    # print(mod_directories)
    # recursive go into folders until no more folder available
    for element in main_game_directories:
        """add folder element to treeview"""
        new_folder = main_tree.add_leaf(folder, folder + '-' + element, element)
        main_tree.treeview.item(new_folder, tags='folder')
        load_main_game_addition(main_path + '/' + element, new_folder, main_tree)
    mod_files = [f for f in listdir(Glob_Var.start_path + main_path) if isfile(join(Glob_Var.start_path + main_path, f))]
    for file in mod_files:
        if file[0] != '_':
            main_tree.add_leaf(folder, main_path + '/' + file, file[:-5])
    #         main_var.append(file[:-5])
    # load_main_game_files_data(main_path)


def load_main_game_addition_files(file_path=''):
    mod_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    """open each file. usually only need name from file, but in some cases also need scene text or maybe something else.
    so final list usually is list of file names or dictionaries with file name and more stuff inside  to choose from """
    for file_data in mod_files:
        if file_data[0] == '_':
            continue
        # print(str(main_item_dict))
        # try:
        with open(file_path + '/' + file_data, encoding='utf-8') as file:
            files = file_data[:-5]
            file_data = json.load(file, object_hook=OrderedDict)
            if 'Fetishes' in file_path:
                continue
            # name = file_data['name']
            # if name != ' ':
            if 'Events' in file_path:
                temp_scene_list = []
                for scenes in file_data['EventText']:
                    # TODO might need to add to search to choices too
                    temp_scene_list.append(scenes['NameOfScene'])
                # GlobalVariables.main_game_items['Events']['data'][files] = temp_scene_list
                Glob_Var.main_game_items['Events'][files] = temp_scene_list
            elif 'Monsters' in file_path:
                # name = file_data['IDname']
                scene_list = {}
                loss_scene_list = []
                victory_scene_list = []
                for scenes in file_data['lossScenes']:
                    loss_scene_list.append(scenes['NameOfScene'])
                for scenes in file_data['victoryScenes']:
                    victory_scene_list.append(scenes['NameOfScene'])
                scene_list['lossScenes'] = loss_scene_list
                scene_list['victoryScenes'] = victory_scene_list
                scene_list['generic'] = file_data['generic']
                scene_list['skillList'] = file_data['skillList']
                # temp_file_list.append({name: scene_list})
                """new organization. file data in main_game_data. later change main_game_item_data to only have path display"""
                girl_data = {'lossScenes': loss_scene_list, 'victoryScenes': victory_scene_list,
                             'generic': file_data['generic'], 'skillList': file_data['skillList']}
                # GlobalVariables.main_game_data['Girls'][files] = girl_data
                Glob_Var.main_game_data['Girls'][file_data['IDname']] = girl_data

            elif 'Fetish' in file_path:
                continue
            elif 'Skills' in file_path:
                # GlobalVariables.main_game_items['Skills']['data'][files] = {'skillTags': file_data['skillTags'],
                #                                                         'fetishTags': file_data['fetishTags']}
                Glob_Var.main_game_items['Skills'][files] = {'skillTags': file_data['skillTags'],
                                                             'fetishTags': file_data['fetishTags']}
                # GlobalVariables.main_game_items['Skills_Data'][name] = {'skillTags': file_data['skillTags'],
                #                                                         'fetishTags': file_data['fetishTags']}
                # temp_file_list.append(name)

            # else:
            #     temp_file_list.append(name)
    # except UnicodeDecodeError as json_load_error:
    #     print(json_load_error.object)
    # print('something  wrong with ' + files)

    return

def remove_files(files_dict, mod_path, mod_name):
    for file in files_dict:
        """instead of removing, move files to temp data to mod folder"""
        file_path = files_dict[file]
        if not access('files/modsTempData/' + mod_name, F_OK):
            mkdir('files/modsTempData/' + mod_name)
        rename(mod_path + '/' + file_path + file + '.json', 'files/modsTempData/' + mod_name + '/' + file
               + '_copy.json')
