from collections import OrderedDict
import textwrap
import json
import re
from time import time, ctime
from os.path import join, isfile, isdir, getmtime
from os import access, F_OK, mkdir, makedirs, listdir
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from GlobalVariables import Glob_Var, Mod_Var


def load_json_data(file_path):
    with open(file_path) as fileData:
        # try:
            temp = json.load(fileData, object_hook=OrderedDict)
        # except:
        #     print("failed to load json file")
        #     return "error"
    return temp


def change_position(widget, position):
    if position == 'center':
        widget.setAlignment(Qt.AlignCenter)
    elif position == 'left':
        widget.setAlignment(Qt.AlignLeft)
    elif position == 'right':
        widget.setAlignment(Qt.AlignRight)


def check_if_folder_exists(path='files/modsTempData', create=True):
    if not access(path, F_OK):
        if create:
            mkdir(path)
            return True
        return False
    else:
        return True


def check_if_file_exists(file_path):
    return isfile(file_path)


def write_json_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as fileData:
        json.dump(data, fileData)


def update_config_data(config_keys, config_vals):
    config_data = load_json_data('config.ini')
    for update_keys, update_vals in zip(config_keys, config_vals):
        config_data[update_keys] = update_vals
    write_json_data('config.ini', config_data)


def clean_text(original_text):
    cleaned_text = re.sub('[^A-Za-z0-9]+', '', original_text)
    return cleaned_text


def getListOptions(field_data, list_type):
    # get list of options for field with dropdown
    # its OPTIONS field in file, if it starts  with dir - list all files in directory, if start with file, read file
    # if currentmod - add from where in current mod to take data, if currentfield - add field name
    # try:
        templist = {}
        list_values = field_data
        # print(field_data)
        listTemp = []
        for values in list_values:
            if 'dir' in values or 'file' in values:
                name_pos = 0
                while name_pos < len(values) and values.find('/', name_pos+1) > 0:
                    if values.find('/', name_pos+1) > 0:
                        name_pos = values.find('/', name_pos+1)
                name_of_elements = values[name_pos + 1:]
                if 'file' in values:
                    dot_place = name_of_elements.find('.')
                    name_of_elements = name_of_elements[:dot_place]
                    templist[name_of_elements] = []
                    file_start_position = values.find('-')
                    filename = values[file_start_position + 1:]
                    if access(filename, F_OK):
                        with open(filename) as listData:
                            for line in listData:
                                templist[name_of_elements].append(line.rstrip())
                if 'dir' in values:
                    templist[name_of_elements] = []
                    dir_start_position = values.find('-')
                    directory = values[dir_start_position + 1:]
                    if access(directory, F_OK):
                        files = [f for f in listdir(directory) if isfile(join(directory, f))]
                        for file in files:
                            if file[0] == '_':
                                continue
                            templist[name_of_elements].append(file[:-5])
            elif 'current' in values:
                if values.find('/') < 0:
                    end_val_index = len(values)
                else:
                    end_val_index = values.find('/')
                # templist[values[7:end_val_index]] = []
                branch_name = values[7:end_val_index]
                templist[branch_name] = []
                item_name = values[11:end_val_index]
                for element_list in GlobalVariables.list_elementlists:
                    if element_list.treeview.heading('#0')['text'] == item_name:
                        templist[branch_name] = element_list.gather_data()
                        break

                # if 'Scene' in values:
                #     for index in range(len(GlobalVariables.list_elementlists)):
                #         if GlobalVariables.list_elementlists[index].treeview.winfo_ismapped():
                #             list_name = GlobalVariables.list_elementlists[index].treeview.heading('#0')['text']
                #
                #     duplicate_treeview()
                #     """"""
                # I forgot this is initated on startup, when all lists are empty.
                # this should be: currentmod-item, monster/generic, event/scene/choice or currentelement-monster
                # if values.find('_') > 0:
                #     value_filter = values[values.find('_')+1:]
                # else:
                #     value_filter = 'ALL'
                # if values.find('/')>0:
                #     elements = values[values.find('-')+1:values.find('/')]
                # else:
                #     elements = values[values.find('-') + 1:]
                # elements_attribute = values[values.find('/')+1:values.find('_')]
                # templist['Mod_' + elements_attribute] = []
                # for element in GlobalVariables.current_mod[elements]:
                #     #this should be - items/itemname/itemtype - for example, only key items
                #     # this if should probably be elsewhere
                #     if elements_attribute in GlobalVariables.current_mod[elements][element]:
                #         if value_filter == 'ALL':
                #             templist['Mod_' + elements_attribute].append(element)
                #         elif GlobalVariables.current_mod[elements][element][elements_attribute] == value_filter:
                #             templist['Mod_' + elements_attribute].append(element)
            elif 'main' in values:
                """text should be main/filepath/finaldirectory. folders should be keys in mainvar
                check up to first / after it its path in main var where to search for data.
                split everything before first /, it will be additional options - inc, generic
                 if -inc- means inclusive, so also need to scan folders inside the one mentioned
                 data should be returned as {folderpath1:[items list], folderpath2:[items list]"""
                # search_options = values[:values.find('/')]
                items_source = values.split('/')
                if len(items_source) > 2:
                    print('need to filter search results')
                else:
                    for items in GlobalVariables.main_game_items[items_source[1]]['path']:
                        listTemp.append(items)
                    # templist[items_source[1]] = GlobalVariables.main_game_items[items_source[1]]['path']
                # if '-inc-' in search_options:
                #     search_deep = True
                # else:
                #     search_deep = False
                """here add how to search for specific element in files, if possible"""
                #
                # items_source = items_source.split('/')
                # if search_deep:
                #     items_names = get_main_game_items_name_recursive_includeFolders(items_source.split('/'), GlobalVariables.main_game_items)
                # else:
                #     items_names = {}
                #     temp = get_main_game_items_name_recursive_one_folder(items_source.split('/'), GlobalVariables.main_game_items)
                #     items_names[items_source] = temp
                # # print(items_source)
                # # print(items_names)
                # if '/Events' in values or '/Monsters' in values:
                #     for items_path in items_names:
                #         eventtemplist = []
                #         for event_name in items_names[items_path]:
                #             temp = ''
                #             """final check. here should be possible to search additioal options,
                #              since event contains all data from about element. This was tough"""
                #             """decision is if to break adding. check if generic in event - true means its monster data
                #             then  if data is  not same  as in file, skip - decitions true."""
                #             for key in event_name.keys():
                #                 decision = False
                #                 if 'generic' in event_name[key]:
                #                     if ('generic' in search_options and event_name[key]['generic'] == 'False') or ('generic' not in search_options and event_name[key]['generic'] == 'True'):
                #                         decision = True
                #                 if decision:
                #                     break
                #                 temp = key
                #             if temp:
                #                 eventtemplist.append(temp)
                #         templist[items_path] = eventtemplist
                # else:
                #     for items_path in items_names:
                #         templist[items_path] = items_names[items_path]
            # elif 'nain' in values:
            #     temp = values.split('-')
            #     templist['main-'+temp[1]] = []
            elif values == 'Stances':
                for stance_type in Glob_Var.stances:
                    templist[stance_type] = Glob_Var.stances[stance_type]
            elif values == 'Fetishes':
                templist['Fetishes'] = Glob_Var.main_game_items["Fetishes"]["Fetish"]
                templist['Addictions'] = Glob_Var.main_game_items["Fetishes"]["Addiction"]
                custom_fetishes = Mod_Var.mod_data['Fetishes']
                if custom_fetishes:
                    templist['Mod'] = list(custom_fetishes.keys())
            elif "game" in values:
                temp = values[5:]
                temp = temp.split('-')
                for val in Glob_Var.game_hard_data[temp[0]][temp[1]]:
                    listTemp.append(val)
            elif '_' in values:
                """get data from global var from dropdown options"""
                listTemp = Glob_Var.drop_down_options[values[1:]]
            else:
                listTemp.append(values)
        if listTemp:
            templist['Main'] = listTemp
        #                    if len(line)>fieldWidth:
        #                        fieldWidth = len(line)
        # print(templist)
        if list_type == 'single':
            final_list = []
            for keys in templist:
                # final_list.append(keys)
                for items in templist[keys]:
                    final_list.append(items)
                    # print(len(final_list))
        else:
            final_list = templist
        return final_list
    # except:
    #     print('problem with function getListOptions with data - ' + str(fieldData))


# TODO probably obsolete
# def get_main_game_items_name_recursive_includeFolders(keys_list, main_items_place=Glob_Var.main_game_items, keypath = ''):
#     """keylist is list made form starting filepath to reach - that is first IF. keypath is to display in treeview"""
#     """then is FOR - check stuff inside, if there is something besides dictionary with files, enter and repeat"""
#     tempdict = {}
#     if len(keys_list) > 0:
#         items_names = get_main_game_items_name_recursive_includeFolders(keys_list[1:], main_items_place[keys_list[0]], keypath+'/'+keys_list[0])
#         tempdict.update(items_names)
#         return items_names
#     if 'files' not in main_items_place:
#         main_items_place['files'] = []
#     for files_and_directories in main_items_place:
#         if files_and_directories != 'files':
#             items_names = get_main_game_items_name_recursive_includeFolders([],
#                                                                             main_items_place[files_and_directories],
#                                                                             keypath + '/' + files_and_directories)
#             tempdict.update(items_names)
#         #         in main game in folder perks/levelperks for some reason 'files' are not created
#         if 'files' in main_items_place:
#             if main_items_place['files']:
#                 tempdict[keypath] = main_items_place['files']
#             """problem in different place - loadmod - load main game items. level perks are groups in directories, and
#              its coded for only depts 1 directories. if it goes deepers, it does not add empty list of files for
#               directoried in between. In short, i expected it to be game/dir/dir max, and level perks are
#                game/dir/dir/dir and for middle dir, it does not add empty files list. So just add here if list is
#                 missing, add it before FOR"""
#     return tempdict
#
#     # tempdict[keypath] = main_items_place['files']
#     # return tempdict

# def get_main_game_items_name_recursive_one_folder(keys_list, main_items_place=Glob_Var.main_game_items):
#     """same as above, but only check folder in keylist and return files from there."""
#     # temp = main_items_place[keys_list[0]]
#     # print(str(temp))
#     if len(keys_list) > 0:
#         if keys_list[0] in main_items_place:
#             items_names = get_main_game_items_name_recursive_one_folder(keys_list[1:], main_items_place[keys_list[0]])
#             return items_names
#         else:
#             return ['Not found']
#     return main_items_place['files']


# def save_item(item_file_name, item_data, elementPath):
#     # print('test should next be item name')
#     # print(item_data['name'])
#     item_Type = item_data['itemType']
#     # elementPath = mod_name + '/Items/'
#     # elementPath = mod_name
#     # if item_Type == 'Consumable':
#     #     item_destination = 'Consumables/Healing/'
#     # elif item_Type == 'CombatConsumable' or item_Type == 'CombatConsumable' or item_Type == 'DissonantConsumable':
#     #     item_destination = 'Consumables/'
#     # elif item_Type == 'Accessory':
#     #     item_destination = 'Equipment/'
#     # elif item_Type == 'Rune':
#     #     item_destination = 'Equipment/Rune/'
#     # elif item_Type == 'Key':
#     #     item_destination = 'KeyItems/'
#     # elif item_Type == 'Loot':
#     #     item_destination = 'Loot/'
#     # else:
#     #     item_destination = 'i dont know where it goes'
#     # elementPath += item_destination
#     if not access(elementPath, F_OK):
#         makedirs(elementPath)
#         # print(elementPath)
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(elementPath + file_name + '.json', 'w') as objectF:
#             objectF.write(json.dumps(item_data, indent='\t'))


# def save_adventure(item_file_name, item_data, mod_name):
#     # print('test should next be item name')
#     # print(item_data['name'])
#     # elementPath = mod_name
#     if not access(mod_name, F_OK):
#         makedirs(mod_name)
#         # print(elementPath)
#     # file_name = item_file_name
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(mod_name + file_name + '.json', 'w') as objectF:
#             objectF.write(json.dumps(item_data, indent='\t'))


# def save_location(item_file_name, item_data, elementPath):
#     # print('test should next be item name')
#     # print(item_data['name'])
#     # elementPath = mod_name
#     if not access(elementPath, F_OK):
#         makedirs(elementPath)
#         # print(elementPath)
#     # file_name = item_data['name']
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(elementPath + file_name + '.json', 'w') as objectF:
#             objectF.write(json.dumps(item_data, indent='\t'))


# def save_event(item_file_name, item_data, element_path):
#     # print('test should next be item name')
#     # print(item_data['name'])
#     # element_path = mod_name
#     if not access(element_path, F_OK):
#         makedirs(element_path)
#         # print(elementPath)
#     # file_name = item_data['name']
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(element_path + file_name + '.json', 'w') as objectF:
#             objectF.write(json.dumps(item_data, indent='\t'))


# def save_fetish(item_data, mod_name):
#     """fetish list is a one item dictionary of  list of dictionaries of fetishes
#         create a template for fetish and saving in list, but as mod saving all to one file
#         item data is dictionary of ordered dictionaries, so"""
#     # print('test')
#     # print(item_data)
#     if item_data:
#         temp_dictionary1 = {'FetishList': []}
#         temp_dictionary2 = {'FetishList': []}
#         elementPath = mod_name + '/'
#         if not access(elementPath, F_OK):
#             makedirs(elementPath)
#             # print(elementPath)
#         for fetish in item_data:
#             if item_data[fetish]['Type'] == 'Fetish':
#                 temp_dictionary1["FetishList"].append(item_data[fetish])
#             if item_data[fetish]['Type'] == 'Addiction':
#                 temp_dictionary2["FetishList"].append(item_data[fetish])
#         if temp_dictionary1['FetishList']:
#             with open(elementPath + '0fetishList.json', 'w') as Fetishes_file:
#                     Fetishes_file.write(json.dumps(temp_dictionary1, indent='\t'))
#         if temp_dictionary2['FetishList']:
#             with open(elementPath + 'addictionList.json', 'w') as Fetishes_file:
#                     Fetishes_file.write(json.dumps(temp_dictionary2, indent='\t'))


# def save_monster(item_file_name, item_data, elementPath):
#     # elementPath = mod_name
#     if not access(elementPath, F_OK):
#         makedirs(elementPath)
#         # print(elementPath)
#     # file_name = item_file_name
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(elementPath + file_name + '.json', 'w') as objectF:
#         objectF.write(json.dumps(item_data, indent='\t'))


# def save_standard(item_file_name, item_data, mod_name):
#     # print('test should next be item name ' + mod_name)
#     # print(item_data['name'])
#     elementPath = mod_name + '/'
#     if not access(elementPath, F_OK):
#         makedirs(elementPath)
#         # print(elementPath)
#     # file_name = item_file_name
#     file_name = re.sub('[^A-Za-z0-9]+', '', item_file_name)
#     with open(elementPath + file_name + '.json', 'w') as objectF:
#             objectF.write(json.dumps(item_data, indent='\t'))


# def save_Mod(mod_name):
#     """should be obsolete as I made one with folders included"""
#     whole_mod = GlobalVariables.current_mod
#     # print('test')
#     # print(mod_name.get())
#     # modname = mod_name.get()
#     mod_path = GlobalVariables.startPath + GlobalVariables.mod_main_switch
#     for elements in whole_mod:
#         if elements == 'Adventures':
#             for adventure in whole_mod[elements]:
#                 save_adventure(whole_mod[elements][adventure], mod_path + mod_name.get())
#         elif elements == "Items":
#             # print("test save item")
#             for item in whole_mod[elements]:
#                 # print(item)
#                 # print(whole_mod[elements][item])
#                 save_item(whole_mod[elements][item], mod_path + mod_name.get())
#         elif elements == 'Fetishes':
#             # print(whole_mod[elements])
#             # for fetish in whole_mod[elements]:
#             #     print('fetish? - ' + fetish)
#             save_fetish(whole_mod[elements], mod_name.get())
#         elif elements == 'Locations' and whole_mod[elements]:
#             for location in whole_mod[elements]:
#                 save_location(whole_mod[elements][location], mod_path + mod_name.get())
#         elif elements == 'Monsters' and whole_mod[elements]:
#             for monster in whole_mod[elements]:
#                 save_monster(whole_mod[elements][monster], mod_path + mod_name.get())
#         elif elements == 'Events' and whole_mod[elements]:
#             for monster in whole_mod[elements]:
#                 save_event(whole_mod[elements][monster], mod_path + mod_name.get())
#         else:
#             for element in whole_mod[elements]:
#                 save_standard(whole_mod[elements][element], mod_path + mod_name.get(), elements)


# def save_Mod_withfolders(mod_name):
#     """should be obsolete as I changed it into function of main window, which then sends data of files to templates
#     and templates save data into files"""
#     mod_path = Glob_Var.start_path + Glob_Var.mod_main_switch + mod_name
#     """elements name will be "adventures", "items", element_items should be {"folders":{"folder":...},"files":[]}"""
#     for elements_name in Mod_Var.mod_display:
#         element_items = Mod_Var.mod_display[elements_name]
#         save_Mod_withfolders2(elements_name, mod_path + '/' + elements_name + '/', element_items)


# def save_Mod_withfolders2(el_name, el_path_start, el_items):
#     """obsolete"""
#     for item in el_items:
#         # if item != 'files':
#         if isinstance(item, dict):
#             for folder in item:
#                 el_path = el_path_start + folder + '/'
#                 save_Mod_withfolders2(el_name, el_path, item[folder])
#             # save_Mod_withfolders2(el_name, el_path, el_items[item])
#         else:
#             # for file in el_items[item]:
#             save_element(el_name, item, el_path_start)
#         # TODO safe to delete
#         # if 'folder' in el_list.treeview.item(item)['tags']:
#         #     el_path = el_path_start + el_list.treeview.item(item)['text'] + '/'
#         #     el_items = el_list.treeview.get_children(item)
#         #     save_Mod_withfolders2(el_name, el_path, el_items, el_list)
#         # else:
#         #     item = el_list.treeview.item(item)['text']
#         #     save_element(el_name, item, el_path_start)


# def save_element(elements, item, mod_path):
#     """obsolete - should be inside each template with customization for separate items"""
#     whole_mod = Mod_Var.mod_data
#     if elements == 'Adventures':
#             save_adventure(item, whole_mod[elements][item], mod_path)
#     elif elements == "Items":
#         # print("test save item")
#             save_item(item, whole_mod[elements][item], mod_path)
#     elif elements == 'Fetishes':
#         # print(whole_mod[elements])
#         # for fetish in whole_mod[elements]:
#         #     print('fetish? - ' + fetish)
#         save_fetish(whole_mod[elements], mod_path)
#     # elif elements == 'Locations' and whole_mod[elements]:
#     #         save_location(whole_mod[elements][item], mod_path)
#     # elif elements == 'Monsters' and whole_mod[elements]:
#     #         save_monster(whole_mod[elements][item], mod_path)
#     # elif elements == 'Events' and whole_mod[elements]:
#     #         save_event(whole_mod[elements][item], mod_path)
#     else:
#             save_standard(item, whole_mod[elements][item], mod_path)

#     nice funtion, goes over directories and file in it and create huge dictionary of all files and their content
# def LoadMod(mod_name, mod_path='.', localdict={}):
#     # global current_mod
#     #   mypath = './game/Mods/'
#     my_path = mod_path + '/' + mod_name
#     #print(mypath)
#     fileanddirs = listdir(my_path)
#     app.setEntry('ModName', mod_name)
#     #print(fileanddirs)
#     modfiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
#     moddirectories = [f for f in listdir(my_path) if isdir(join(my_path, f))]
#     #print(moddirectories)
#     #print(modfiles)
# #   first need to go dig in dir, once no more to dig, take all files, load them. Element - first nothing then item or
# #   adventure etc
#     for element in moddirectories:
#         localdict[element] = {}
# # after we get whole path, create nested dictionary according to path and load all files withing to that dictionary
#     for files in modfiles:
#         if files[0] == '_':
#             continue
#         filepath = my_path[2:] + '/' + files
#         #print('file path is = ' + filepath)
#         with open(filepath) as fileData:
#             try:
#                 LoadData = json.load(fileData, object_hook=OrderedDict)
#             except Exception as a:
#                 print('file problem in - ' +filepath)
#                 print(a)
#                 exit(0)
#
#         localdict[files] = LoadData
# now we go over all elements in localdict, if its in modirec - its a direcotry and we load data from it
#     for elements in localdict:
#         if elements in moddirectories:
#             LoadMod(elements, my_path, localdict[elements])
#     return localdict
#


# def browse_files(button_to_display_filename, variable_for_file_path, media_path):
# def browse_files(file_type, return_list):
#     if file_type:
#         file_type = (("Image files", "*.png*"), ("all files", "*.*"))
#     else:
#         file_type = (("Music files", "*.opus*"), ("Music files", "*.ogg*"), ("Music files", "*.mp3*"),
#                      ("Music files", "*.wav*"), ("all files", "*.*"))
#     if return_list:
#         filename = filedialog.askopenfilenames(initialdir=GlobalVariables.startPath + "/game/mods/",
#                                                title="Select a Files",
#                                                filetypes=file_type)
#     else:
#         filename = filedialog.askopenfilename(initialdir=GlobalVariables.startPath + "/game/mods/",
#                                               title="Select a File",
#                                               filetypes=file_type)
#     # filename = filedialog.askopenfilename(initialdir=GlobalVariables.startPath + "/game/mods/",
#     #                                       title="Select a File",
#     #                                       filetypes=(("Image files", "*.png*"),
#     #                                                  ("all files", "*.*")))
#     if filename:
#         if not isinstance(filename, tuple):
#             return [filename]
#         return filename
#     else:
#         return False
#         # temp = filename.find('Mods/')
#         # local_path = media_path + filename[temp:]
#         # variable_for_file_path.set(local_path)
#         #
#         # filename =filename.split('/')
#         # button_to_display_filename['text'] = filename[-1]


def wrap(string, length=20, row_len=39):
    return '\n'.join(textwrap.wrap(string, length))


def error_log(log_data):
    if Glob_Var.file_log:
        with open('error_logs.txt', 'a', encoding='utf-8-sig') as error_file:
            error_file.write('time of error - ' + str(ctime(time())))
            error_file.write(str(log_data) + '\n')
    else:
        print(log_data)


def duplicate_treeview(source, destination, source_leaf='', destination_leaf=''):
    for child in source.get_children(source_leaf):
        new_leaf = destination.insert(destination_leaf, "end", text=source.item(child)['text'])
        if source.get_children(child):
            duplicate_treeview(source, destination, child, new_leaf)


def find_current_displayed_characters(event_type=None, current_scene_field=None):
    """it needs to check current edited scene from last item in list backwards for tag  'DisplayCharacters'
     if not found, get scene name and check ...what next? scenes are just data in a treeview.
      I would need to make a web connection of scenes to be able to traverse it safely and find
       current displayed characters. DAMN"""
    """well, first check current scene. if not, then worry"""
    display_characters_list = []
    # current_scene_field should be elementlist
    leaves = current_scene_field.treeview.get_children()
    if current_scene_field.treeview.selection():
        row_start_number = current_scene_field.treeview.index(current_scene_field.treeview.selection()[0])
    else:
        row_start_number = len(leaves)-1
    for index in range(row_start_number, -1, -1):
        row_text = current_scene_field.treeview.item(leaves[index])['text']
        if row_text == 'DisplayCharacters':
            temp = current_scene_field.treeview.get_children(leaves[index])
            for element in temp[:-1]:
                display_characters_list.append(current_scene_field.treeview.item(element)['text'])
            break
    return display_characters_list


def find_monster_skills(girl_id):
    """returns girls skill list"""
    if girl_id in Mod_Var.mod_data['Monsters']:
        skill_list = Mod_Var.mod_data['Monsters'][girl_id]['skillList']
    else:
        skill_list = Glob_Var.main_game_data['Girls'][girl_id]['skillList']
    return_list = []
    for skill in skill_list:
        if skill not in return_list:
            return_list.append(skill)
    return return_list






    # if event_type == 'EventText':
    #     temp = 'Events'
    # else:
    #     temp = 'Monsters'
    # current_scene = GlobalVariables.templates[temp].frame_fields[event_type].field_frame['NameOfScene'].get_val()
    # for scenes in scene_list:
    #     if scene_list['NameOfScene'] ==


def findSkillTags(skill_name):
    return
# ask around if this is even needed.


# def load_main_game_item_2(main_path='./../json', element_type='', main_var=None):
#     """ this should load main game data into global variable, to use later in other fields where you choose items """
#     mod_directories = [f for f in listdir(main_path) if isdir(join(main_path, f))]
#     # print(mod_files)
#     # print(mod_directories)
#     # recursive go into folders until no more folder available
#     for element in mod_directories:
#         temp_dict = {element: []}
#         main_var.append(temp_dict)
#         load_main_game_item_2(main_path + '/' + element, element_type, main_var[-1][element])
#     mod_files = [f for f in listdir(main_path) if isfile(join(main_path, f))]
#     for file in mod_files:
#         if file[0] != '_':
#             main_var.append(file[:-5])
#     load_main_game_files_data(main_path)
#
# def load_main_game_files_data(file_path=''):
#     mod_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
#
#     """open each file. usually only need name from file, but in some cases also need scene text or maybe something else.
#     so final list usually is list of file names or dictionaries with file name and more stuff inside  to choose from """
#     for file_data in mod_files:
#         if file_data[0] == '_':
#             continue
#         # print(str(main_item_dict))
#         # try:
#         with open(file_path + '/' + file_data, encoding='utf-8') as file:
#             files = file_data[:-5]
#             file_data = json.load(file, object_hook=OrderedDict)
#             if 'Fetishes' in file_path:
#                 continue
#             # name = file_data['name']
#             # if name != ' ':
#             if 'Events' in file_path:
#                 temp_scene_list = []
#                 for scenes in file_data['EventText']:
#                     # TODO might need to add to search to choices too
#                     temp_scene_list.append(scenes['NameOfScene'])
#                 GlobalVariables.main_game_items['Events']['data'][files] = temp_scene_list
#             elif 'Monsters' in file_path:
#                 # name = file_data['IDname']
#                 scene_list = {}
#                 loss_scene_list = []
#                 victory_scene_list = []
#                 for scenes in file_data['lossScenes']:
#                     loss_scene_list.append(scenes['NameOfScene'])
#                 for scenes in file_data['victoryScenes']:
#                     victory_scene_list.append(scenes['NameOfScene'])
#                 scene_list['lossScenes'] = loss_scene_list
#                 scene_list['victoryScenes'] = victory_scene_list
#                 scene_list['generic'] = file_data['generic']
#                 scene_list['skillList'] = file_data['skillList']
#                 # temp_file_list.append({name: scene_list})
#                 """new organization. file data in main_game_data. later change main_game_item_data to only have path display"""
#                 girl_data = {'lossScenes': loss_scene_list, 'victoryScenes': victory_scene_list,
#                              'generic': file_data['generic'], 'skillList': file_data['skillList']}
#                 # GlobalVariables.main_game_data['Girls'][files] = girl_data
#                 GlobalVariables.main_game_data['Girls'][file_data['IDname']] = girl_data
#
#             elif 'Fetish' in file_path:
#                 continue
#             elif 'Skills' in file_path:
#                 GlobalVariables.main_game_items['Skills']['data'][files] = {'skillTags': file_data['skillTags'],
#                                                                         'fetishTags': file_data['fetishTags']}
#                 # GlobalVariables.main_game_items['Skills_Data'][name] = {'skillTags': file_data['skillTags'],
#                 #                                                         'fetishTags': file_data['fetishTags']}
#                 # temp_file_list.append(name)
#
#             # else:
#             #     temp_file_list.append(name)
#     # except UnicodeDecodeError as json_load_error:
#     #     print(json_load_error.object)
#     # print('something  wrong with ' + files)
#
#     return


def load_recent_mods():
    file_data = {}
    if access('recent_mods.json', F_OK):
        with open('recent_mods.json', encoding='utf-8') as file:
            file_data = json.load(file, object_hook=OrderedDict)
    else:
        file_data['recentmods'] = []
    return file_data['recentmods']


# def unlock_field(field):
#     if field.type in ['text', 'area']:
#         field.setReadOnly(False)
#         field.setFocus()
#     else:
#         field.setEnabled(True)
#     return
#
#
# def lock_field(field):
#     if field.type in ['text', 'area', 'multilist']:
#         field.setReadOnly(True)
#     else:
#         field.setEnabled(False)
#     return


def show_message(title, information, win_title):
    msg = QMessageBox()
    msg.setText(title)
    msg.setInformativeText(information)
    msg.setWindowTitle(win_title)
    msg.exec_()


def confirmation_message():
    msg = QMessageBox()
    msg.setInformativeText("Do you want to save your changes?")
    msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Save)
    selection = msg.exec_()
    if selection == QMessageBox.Save:
        return 'save'
    elif selection == QMessageBox.Discard:
        return 'continue'
    elif selection == QMessageBox.Cancel:
        return 'cancel'


def message_yes_no():
    msg = QMessageBox()
    msg.setInformativeText("Do you want to continue?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.Yes)
    selection = msg.exec_()
    if selection == QMessageBox.Yes:
        return 1
    elif selection == QMessageBox.No:
        return 0


def get_file_time_modification(file):
    return getmtime(file)
