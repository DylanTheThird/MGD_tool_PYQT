from PyQt5 import QtGui, QtWidgets
from PyQt5.Qt import QStandardItem
from PyQt5.QtCore import Qt
from GlobalVariables import Glob_Var
from otherFunctions import show_message
from ImageViewer_MGD import QImageViewer
import copy
import SimpleFields
import MarkUpDialog
# class ExpandDictionaryField:
#     def __init__(self, master=None, field_name=None, tooltip_text=None,
#                  fields_data=None, templateName='', mode=1):
#         self.master_layout = master
#         self.custom_layout = QtWidgets.QHBoxLayout()
#         if field_name:
#             self.label = SimpleFields.CustomLabel(self.custom_layout)
#             self.custom_layout.addWidget(self.label)
#         else:
#             self.label = None
#         if self.label:
#             self.label.setToolTip(tooltip_text)
#         self.title = field_name
#         self.modifyFlag = False
#         self.name_field = 'Name'
#         self.fieldsNames = fields_data['fields'].keys()
#         # print(str(fields_data['options']))
#         # print(str(self.fieldsNames))
#         self.addition = False
#         self.ExpandFlag = False
#         self.repeat_vals = False
#         if 'options' in fields_data:
#             if 'expand' in fields_data['options']:
#                 self.ExpandFlag = True
#             if 'multi_val' in fields_data['options']:
#                 self.repeat_vals = True
#             if 'limit' in fields_data['options']:
#                 self.limit = fields_data['limit']
#             else:
#                 self.limit = 0
#             if 'addition' in fields_data['options']:
#                 self.addition = True
#         # else:
#         #     print('expand dictionary in customer fields - missing options tags in field ' + field_name)
#         # print(self.fieldsNames)
#         self.fields_list = []
#         self.current_expanded_data = []
#         self.template_name = templateName
#         if templateName:
#             field_address = templateName + '-' + self.title
#         else:
#             field_address = ''
#         if not self.ExpandFlag or mode:
#             for fields in fields_data['fields']:
#                 field = createField(frame_expand_dictionary, fields, fields_data['fields'][fields], template_name=field_address, mode=mode)
#                 field.pack()
#                 self.fields_list.append(field)
#                 self.row_size += field.row_size
#                 # rowposition += 3
#         # print('expand dictionary row size - ' + str(self.row_size))
#         if self.ExpandFlag:
#         # print(str(fields_data))
#             self.tree_final_data = SimpleFields.ElementsList(self, 3, 0, field_name, colspan=2)
#             self.tree_final_data.treeview.configure(selectmode='extended')
#             for data in fields_data['fields']:
#                 self.name_field = data
#                 break
#             if mode:
#                 self.butCommand = partial(self.add_data_to_treeview, self.fields_list, fields_data.keys(),
#                                           self.tree_final_data)
#                 self.buttonADD_controlTreeview = tk.Button(self, text='Add', wraplength=50,
#                                                            command=self.add_data_to_treeview)
#                 self.buttonADD_controlTreeview.grid(row=2, column=0, sticky='W', columnspan=2)
#                 self.buttonMOD_controlTreeview = tk.Button(self, text='Modify', wraplength=50,
#                                                            command=self.mod_data_to_treeview)
#                 self.buttonMOD_controlTreeview.grid(row=2, column=0, columnspan=2)
#                 self.buttonDEL_controlTreeview = tk.Button(self, text='Delete', wraplength=50,
#                                                            command=self.del_data_to_treeview)
#                 self.buttonDEL_controlTreeview.grid(row=2, column=0, sticky='E', columnspan=2)
#                 # self.treeview_optionstochoose.treeview.bind("<Double-1>", self.OnDoubleClick)
#                 # self.get, self.set = self.var.get, self.var.set
#
#                     # if 'Name' in data or 'name' in data:
#                     #         self.name_field = data
#                     #         break
#             else:
#                 self.tree_final_data.treeview.heading("#0", text='Double Click to Edit')
#                 self.tree_final_data.treeview.bind("<Double-Button-1>", self.on_double_click_edit_field)
#                 self.tree_final_data.treeview.unbind("<Delete>")
#                 self.tree_final_data.treeview.unbind("<Control_L>")
#         if fields_data['type'] == 'listDict':
#             self.flag_listdict = True
#         else:
#             self.flag_listdict = False
#     def set_val(self, values):
#         if self.ExpandFlag:
#             """just add data to treeview second function should be enough, since it requires already prepared data"""
#             for fields in values:
#                 for data in fields:
#                     if fields[data] == '':
#                         return
#                     else:
#                         break
#                 break
#             self.add_data_to_treeview_2(values)
#         else:
#             # its working for now, lets leave it
#             if isinstance(values, list):
#                 for fields, input_values in zip(self.fields_list, values):
#                     temp = list(input_values.items())
#                     # print(str(temp[0][1]))
#                     fields.set_val(temp[0][1])
#             else:
#                 for fields, input_values in zip(self.fields_list, values.items()):
#                     fields.set_val(input_values[1])
#
#     def get_val(self, temp_dict_container=None):
#         if self.ExpandFlag:
#             # tempfinalList = self.current_expanded_data
#             # for Parent in self.treeview_optionstochoose.treeview.get_children():
#             #     tempdictinlist = {}
#             #     templist = []
#             #     for child in self.treeview_optionstochoose.treeview.get_children(Parent):
#             #         tempdict = {}
#             #         data = self.treeview_optionstochoose.treeview.item(child)["text"].split(':')
#             #         tempdict[data[0]] = data[1]
#             #         templist.append(tempdict)
#             #     for item in self.fields_list:
#             #         # print(item.title)
#             #         # print(item.type)
#             #         # item_occur = [k[item] for k in templist if k.get(item)]
#             #         # print(len(item_occur))
#             #         # if len(item_occur) > 1:
#             #         if 'multilist' in item.type:
#             #             templist2 = []
#             #             for data in templist:
#             #                 # print(list(data.keys())[0])
#             #                 if list(data.keys())[0] == item.title:
#             #                     templist2.append(list(data.values())[0])
#             #             tempdictinlist[item.title] = templist2
#             #         else:
#             #             item_value = ''
#             #             for data in templist:
#             #                 if list(data.keys())[0] == item.title:
#             #                     item_value = (list(data.values())[0])
#             #                     break
#             #             tempdictinlist[item.title] = item_value
#             #     tempfinalList.append(tempdictinlist)
#             # print(str(tempfinalList))
#             # print('test')
#             #     # if there is a child, it probably need to be a list, not create list, put in dictionary and put in list
#             #     for child in self.treeview_optionstochoose.treeview.get_children(Parent):
#             #             data = self.treeview_optionstochoose.treeview.item(child)["text"]
#             #             templist.append(data)
#             #     if templist:
#             #         tempdictinlist[self.treeview_optionstochoose.treeview.heading('#0')['text']] = templist
#             #         tempfinalList.append(tempdictinlist)
#             #     # if templist is empty, then all data is in parent, separated with _ so turn it into a dictionary
#             #     if not templist:
#             #         tempdictinlist = {}
#             #         data = self.treeview_optionstochoose.treeview.item(Parent)["text"]
#             #         # print(data)
#             #         listed_values = data.split('_')
#             #         print(listed_values)
#             #         for name, values in zip(self.fieldsNames, listed_values):
#             #             tempdictinlist[name] = values
#             #         tempfinalList.append(tempdictinlist)
#             # # return a list of dictionaries of data from treevieww elements
#             # # print("jest expand")
#             tempfinalList = []
#             for roots in self.tree_final_data.treeview.get_children(''):
#                 tempfinalList.append(self.gather_data(roots))
#         elif self.flag_listdict:
#             tempfinalList = []
#             for fields in self.fields_list:
#                 val1 = fields.title
#                 val2 = fields.get_val()
#                 tempdic = {val1: val2}
#                 tempfinalList.append(tempdic)
#         else:
#             """return a dictionary of values from self list. This is in case it is expected only 1 dictionary"""
#             tempfinalList = {}
#             for name, values in zip(self.fieldsNames, self.fields_list):
#                 tempfinalList[name] = values.get_val()
#         if not tempfinalList:
#             temp_dict = {}
#             for fields in self.fields_list:
#                 temp_dict[fields.title] = fields.get_val()
#             tempfinalList = [temp_dict]
#         if temp_dict_container is not None:
#             """it displays nested dictionaries as dict in dict, but for writing to file it should be dict in list.
#             So lets iterate over all data again, and if value is a dictionary, replace it with a copy of list of
#              contained dictionaries"""
#             for root_vals in tempfinalList:
#                 if isinstance(root_vals, dict):
#                     for vals in root_vals:
#                         if isinstance(root_vals[vals], dict):
#                             templist = []
#                             """this replace should be a dictionaries to put in a list"""
#                             for replace in root_vals[vals]:
#                                 # for i in root_vals[vals][replace]:
#                                 templist.append(root_vals[vals][replace])
#                             root_vals[vals] = templist
#             temp_dict_container[self.title] = tempfinalList
#         else:
#             return tempfinalList
#
#     def clear_val(self):
#         for item in self.fields_list:
#             item.clear_val()
#         if self.ExpandFlag:
#             if self.modifyFlag:
#                 print('cool')
#             else:
#                 for Parent in self.tree_final_data.treeview.get_children():
#                     self.tree_final_data.treeview.delete(Parent)
#                 for data in self.current_expanded_data:
#                     self.current_expanded_data.remove(data)
#
#     def mod_data_to_treeview(self):
#         """change add and delete button. here set modify flag, unset on other buttons"""
#         # for field in self.fields_list:
#         #     field.clear_val()
#         self.modifyFlag = True
#         self.buttonADD_controlTreeview['text'] = 'Save'
#         self.buttonDEL_controlTreeview['text'] = 'Cancel'
#         for fields in self.fields_list:
#             fields.clear_val()
#
#         data_to_modify = self.tree_final_data.selected_item(value='code')
#         target_data = self.tree_final_data.find_root_parent(data_to_modify)
#         data_to_load = self.gather_data(target_data)
#         # it seems to be working for its fields
#         for fields, values in zip(self.fields_list, data_to_load.values()):
#             fields.set_val(values)
#         # for fields in self.current_expanded_data:
#         #     if fields[self.name_field] == target_data:
#         #         self.set_val(fields)
#         #         break
#
#     def add_data_to_treeview(self):
#         """since speaker field got limit of 12 items, first check if limit reached or not"""
#         if self.limit > 0:
#             if len(self.tree_final_data.treeview.get_children()) >= self.limit:
#                 messagebox.showerror('Limit reached', 'Only ' + str(self.limit) + ' allowed', parent=self)
#                 return
#         """lets split it into 2 functions. one takes all data and pass to the other, recursive that puts it in treev"""
#         for fields in self.fields_list:
#             if fields.get_val():
#                 final_data = []
#                 data_var = {}
#                 for fields_name, input_values in zip(self.fieldsNames, self.fields_list):
#                     data_var[fields_name] = input_values.get_val()
#                 """cant just append dictionaries to list, as in theory, each dictionary should be unique"""
#
#                 if self.modifyFlag:
#                     self.buttonADD_controlTreeview['text'] = 'Add'
#                     self.buttonDEL_controlTreeview['text'] = 'Delete'
#                     self.modifyFlag = False
#                     root_item = self.tree_final_data.find_root_parent(self.tree_final_data.selected_item(value='code'))
#                     previous_data_index = self.tree_final_data.treeview.index(root_item)
#                     self.tree_final_data.treeview.delete(root_item)
#                 else:
#                     previous_data_index = 'end'
#                     # previous_data_index = self.treeview_optionstochoose.treeview.index()
#                 # if self.current_expanded_data:
#                 # for fields in self.current_expanded_data:
#                 #     if fields[self.name_field] == data_var[self.name_field]:
#                 #         previous_data_index = self.current_expanded_data.index(fields)
#                 #         self.current_expanded_data.remove(fields)
#                             # self.current_expanded_data.insert(previous_data_index, final_data)
#
#                 # self.current_expanded_data.insert(previous_data_index, data_var)
#                 final_data.append(data_var)
#                 self.add_data_to_treeview_2(final_data, position_no=previous_data_index)
#                 for field in self.fields_list:
#                     field.clear_val()
#             else:
#                 messagebox.showwarning("missing name", 'Missing name', parent=self)
#             break
#
#     def add_data_to_treeview_2(self, final_data_list, branch='', position_no='end'):
#         """this should work recursive. if branch is empty, then its main list, so add branch with empty leaves.
#         if branch is provided, then we are adding another dictionary no deeper level, so just name leave
#         it will works as branch."""
#         """its not always NAME"""
#         if isinstance(final_data_list, dict):
#             data_list = []
#             for data in final_data_list:
#                 data_list.append(final_data_list[data])
#             final_data_list = data_list
#         for final_data in final_data_list:
#             branch_title = final_data[self.name_field]
#             if isinstance(branch_title, list):
#                 branch_title = branch_title[0]
#             try:
#                 if branch:
#                     new_branch = self.tree_final_data.add_leaves(branch, [final_data[self.name_field]], update_flag=False)
#                 else:
#                     new_branch = self.tree_final_data.add_branch(branch_title, [], position=position_no,
#                                                         update_flag=self.repeat_vals)
#             except:
#                 otherFunctions.error_log('problem with adding data to treeview - GuiFieldClasses in line 1174')
#                 otherFunctions.error_log('branch is ' + branch)
#                 otherFunctions.error_log('adding  ' + str(final_data))
#             for data in final_data:
#                 """if data is in list, it might be just list of values, or list of dictionaries
#                 Either way, add that leaf. Everything will be added to it"""
#                 if isinstance(final_data[data], list):
#                     next_level_branch = self.tree_final_data.add_leaves(final_data[self.name_field],
#                                                                             [data], update_flag=False)
#                     templist = []
#                     for values in final_data[data]:
#                         if isinstance(values, dict):
#                             """start this function again, but on already created leaf which will work as root branch"""
#                             self.add_data_to_treeview_2([values], branch=next_level_branch)
#                         else:
#                             templist.append(values)
#                     if templist:
#                         self.tree_final_data.add_leaves(next_level_branch, templist,
#                                                             update_flag=False)
#                 else:
#                     temp = data + ':' + final_data[data]
#                     self.tree_final_data.add_leaves_simple(new_branch, [temp])
#                     # self.tree_final_data.add_leaves(new_branch, [temp], update_flag=False)
#         # # if modify data, check index of selection, delete it and put new branch in its place
#         # if self.modifyFlag:
#         #     # current_item = self.treeview_optionstochoose.treeview.selection()[0]
#         #     # current_index = self.treeview_optionstochoose.treeview.index(current_item)
#         #     # self.treeview_optionstochoose.treeview.delete(current_item)
#         #     self.buttonADD_controlTreeview['text'] = 'Add'
#         # # self.treeview_optionstochoose.add_branch(branch_name, fields_list, update_flag=self.modifyFlag,
#         # #                                          position=current_index)
#         # # self.modifyFlag = False
#         # # # self.treeview_optionstochoose.add_branch(fieldvals[:-1],fields_list)
#
#     def del_data_to_treeview(self):
#         if self.modifyFlag:
#             self.modifyFlag = False
#             self.buttonADD_controlTreeview['text'] = 'Add'
#             self.buttonDEL_controlTreeview['text'] = 'Delete'
#             for fields in self.fields_list:
#                 fields.clear_val()
#         else:
#             try:
#                 item = self.tree_final_data.treeview.selection()[0]
#                 item_to_del = self.tree_final_data.treeview.item(item)['text']
#                 self.tree_final_data.treeview.delete(item)
#                 for data in self.current_expanded_data:
#                     if data[self.name_field] == item_to_del:
#                         self.current_expanded_data.remove(data)
#             except:
#                 print("nothing to delete")
#     def OnDoubleClick(self, event):
#         # item = self.treeview_optionstochoose.treeview.identify("item", event.x, event.y)
#         # item = self.treeview_optionstochoose.treeview.selection()[0]
#         # print("you clicked on", self.treeview_optionstochoose.treeview.item(item)["text"])
#         item = self.tree_final_data.treeview.selection()[0]
#         # print(str(self.treeview_optionstochoose.treeview.index(item)))
#         leaf_flag = self.tree_final_data.treeview.parent(item)
#         # # print("you clicked on", self.treeview_optionstochoose.treeview.item(item, "text"))
#         tempdic = {}
#         index = 0
#         if not leaf_flag:
#             # print("clicked on parent")
#             # oh man, first, prepare all items in leaf into a dictionary in a list object
#             leaf_data = []
#             leafs = self.tree_final_data.treeview.get_children(item)
#             for leaf in leafs:
#                 tempdic = {}
#                 temp = self.tree_final_data.treeview.item(leaf)['text'].split(':')
#                 tempdic[temp[0]] = temp[1]
#                 leaf_data.append(tempdic)
#             # print(str(leaf_data))
#             # no check in field, if type is multilist, then values should be in list.
#             # for now, other types usually uses strings
#             for item in self.fields_list:
#                 # print(item.title)
#                 # print(item.type)
#                 # print(len(item_occur))
#                 if 'multilist' in item.type:
#                     templist = []
#                     for data in leaf_data:
#                         # print(list(data.keys())[0])
#                         if list(data.keys())[0] == item.title:
#                             templist.append(list(data.values())[0])
#                     item.set_val(templist)
#                     # print("create list from values with same key")
#                 else:
#                     # print('just return value, since only once it appears so it probably a text')
#                     for data in leaf_data:
#                         # print(list(data.keys())[0])
#                         if list(data.keys())[0] == item.title:
#                             item.set_val(list(data.values())[0])
#         self.modifyFlag = True
#         self.buttonADD_controlTreeview['text'] = 'Modify'
#         #     # for leaf in leafs:
#         #     #     print(self.treeview_optionstochoose.treeview.item(leaf)['text'])
#         #     #     leaf_data = self.treeview_optionstochoose.treeview.item(leaf)['text'].split(':')
#         #     #     if leaf_data[0] == leaf_name:
#         #     #         leaf_list.append(leaf_data[1])
#         #     #         leaf_name = leaf_data[0]
#         #     #         continue
#         #     #     else:
#         #     #         leaf_val = leaf_data[1]
#         #     #     leaf_name = leaf_data[0]
#         #
#         #     print("clicked on parent")
#         #     # values = item.split('_')
#         #     # for fields in self.fields_list:
#         #     #     fields.set_val(values[index])
#         #     #     index += 1
#         # else:
#         #     # data = self.treeview_optionstochoose.treeview.item(item)["text"]
#         #     # print("leaf")
#         #     # print(str(data))
#         #     # for fields in self.fields_list:
#         #     #     fields.set_val(data)
#         #     return
#     def gather_data(self, item):
#         temp_dict = {}
#         temp_list = []
#         for leaves in self.tree_final_data.treeview.get_children(item):
#             value = self.tree_final_data.treeview.item(leaves)['text']
#             value = value.split(':')
#             if len(value) == 2:
#                 temp_dict[value[0]] = value[1]
#             elif len(value) == 1:
#                 if self.tree_final_data.treeview.get_children(leaves):
#                     """this is used only in pictures field, where to display, dictionary is put in another dictionary,
#                      but it causes problem to load data from treeview. So, since it is used in one place only,
#                       I added line to dive in treeview twice, to avoid first dictionary and prepare list from
#                        remaining dicts."""
#                     temp_list_2 = []
#                     for image_leaf in self.tree_final_data.treeview.get_children(leaves):
#                         temp_list_2.append(self.gather_data(image_leaf))
#                         # temp_dict[value[0]] = self.gather_data(image_leaf)
#                     temp_dict[value[0]] = temp_list_2
#                 else:
#                     temp_list.append(value[0])
#         if temp_list:
#             return temp_list
#         else:
#             return temp_dict
#     def on_double_click_edit_field(self, event):
#         if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
#             if self.addition:
#                 flag = True
#             else:
#                 flag = False
#         else:
#             flag = True
#         if flag:
#             region = self.tree_final_data.treeview.identify("region", event.x, event.y)
#             if region == "heading":
#                 Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
#                                                structure_data=self.get_val(), structure_link=self)
#
#     def bind_control(self, binding):
#         if binding:
#             self.tree_final_data.bind('<Double-Button-1>', self.on_double_click_edit_field)
#         else:
#
#             self.tree_final_data.unbind('<Double-Button-1>')
#
#     # def hide_field(self):
#     #     self.pack_forget()
#     #
#     # def show_field(self):
#     #     self.field_frame.pack()

# TODO fix, add multilist display for monster and events cards which will connect to main data tree, instead of connecting it all
class DeckField:
    def __init__(self, master=None, field_data=None):
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.title = 'Deck'
        self.type = 'multilist'
        self.selection_type = ''
        self.option_flag = False #for adding monster list. later, is set to 1 if adding monsters, when done, add end tag
        self.option_list = ["Event", "Monster", "RandomEvent", "RandomMonsters", "RandomTreasure", "CommonTreasure",
                            "UncommonTreasure", "RareTreasure", "BreakSpot", "Unrepeatable"]
        self.row_size = 6

        self.options_selection = SimpleFields.SingleList(master, 'Deck', edit=False)
        self.options_selection.set_val(self.option_list)
        self.options_selection.currentTextChanged.connect(self.options_prepare)
        self.label_custom = self.options_selection.label_custom
        self.add_button = SimpleFields.CustomButton(master, '', class_connector=self)
        self.add_button.clicked.connect(self.add_data)
        self.add_button.setMaximumWidth(30)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/file-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon)

        self.field_for_events_and_monsters = SimpleFields.MultiListDisplay(None, '', main_data_treeview=Glob_Var.main_game_field,
                                                                           field_data={'choices': [""], 'options': ["single_item"]})
        # self.field_for_events_and_monsters.final_data.setAlignment(Qt.AlignCenter)
        self.field_for_events_and_monsters.hide()
        self.deck_tree = SimpleFields.ElementsList(master, class_connector=self)
        self.options_selection.set_up_widget(self.custom_layout)
        self.field_for_events_and_monsters.set_up_widget(self.custom_layout)
        self.options_selection.custom_layout.addWidget(self.add_button)
        self.custom_layout.addWidget(self.deck_tree)
        self.addition = True

    def set_val(self, values=None):
        # if loading data, values is a list, need to load it all just. but updating also uses set_val, and update
        #  requires more coding, so lets separate these 2 processes
        if isinstance(values, str):
            try:
                self.add_data(values)
            except:
                print('deck field - might as well remove that line above')
        else:
            try:
                temp_list = []
                i = 0
                """since i need to skip and gather some card, i need to use while. For loop has separate index"""
                while i < len(values):
                    if values[i] == 'Monster':
                        monster_spot = i
                        i += 1
                        while values[i] != 'EndLoop':
                            temp_list.append(values[i])
                            values.pop(i)
                        values.pop(i)
                        temp_dict = {'Monster': temp_list}
                        temp_list = []
                        values[monster_spot] = temp_dict
                        continue
                    elif values[i] == 'Event':
                        i += 1
                        temp_dict = {'Event': values[i]}
                        values[i - 1] = temp_dict
                        values.pop(i)
                        continue
                    i += 1
            except:
                print("error adding new branch to treeview in deckfield - setval")
            self.deck_tree.add_data(data=values)
            self.deck_tree.expandAll()

    def get_val(self, temp_dict_container=None):
        final_list = []
        deck_list = self.deck_tree.get_data()
        for cards in deck_list:
            if isinstance(cards, dict):
                card_call = list(cards.keys())[0]
                final_list.append(card_call)
                for card in cards:
                    # card will be a list, need to iterate over it again
                    for a in cards[card]:
                        final_list.append(a)
                if card_call == 'Monster':
                    final_list.append('EndLoop')
            else:
                final_list.append(cards)
        if temp_dict_container is not None:
            temp_dict_container['Deck'] = final_list
        else:
            return final_list

    def clear_val(self):
        self.deck_tree.clear_tree()

    def add_data(self):
        selected_option = self.options_selection.get_val()
        new_insert = QStandardItem(selected_option)
        # adding to monster or event group
        """if selected option is monster or event take value from designed field
         then check in data tree if it should be added to correct branch or create new branch"""
        if selected_option == 'Monster' or selected_option == 'Event':
            tree_selection = self.deck_tree.selected_element()
            new_insert.setText(self.field_for_events_and_monsters.get_val())
            if tree_selection:
                """if selected item is group, append to that group"""
                if tree_selection.text() == selected_option:
                    tree_selection.appendRow(new_insert)
                    return
                elif tree_selection.parent():
                    """if selected item is in group, just insert above it"""
                    if tree_selection.parent().text() == selected_option:
                        tree_selection.parent().insertRow(tree_selection.row(), new_insert)
                        return
            """if selected group which is not same as selected option. for example, still selected event,
                while adding monsters, need to add to the end of deck tree, but first check
                if there is proper group there"""
            last_item = self.deck_tree.tree_model.item(self.deck_tree.tree_model.rowCount()-1)
            if last_item.text() == selected_option:
                last_item.appendRow(new_insert)
                return
            new_group = QStandardItem(selected_option)
            new_group.appendRow(new_insert)
            self.deck_tree.tree_model.appendRow(new_group)
        else:
            tree_selection = self.deck_tree.selected_element()
            if tree_selection:
                if tree_selection.parent():
                    tree_selection = tree_selection.parent()
                self.deck_tree.tree_model.insertRow(tree_selection.row(), new_insert)
            else:
                self.deck_tree.tree_model.appendRow(new_insert)
        Glob_Var.edited_field()

    def options_prepare(self, selected_value=None):
        if selected_value in 'Monsters Events':
            self.field_for_events_and_monsters.show()
            self.field_for_events_and_monsters.clear_val()
            self.field_for_events_and_monsters.selection_type = selected_value + 's'
            Glob_Var.main_game_field.disconnect_multilist()
        else:
            self.field_for_events_and_monsters.hide()

    def set_up_widget(self, outside_layer):
        outside_layer.addLayout(self.custom_layout)

# TODO check if expanddictionaryfield is even used
class ExpandDictionaryField(QtWidgets.QWidget):
    # this is attempt at adding working shortcuts. Class is derivered from Qwidget
    # changes: added self.setLayout(customlayout) and in setUpWidget is adding self as widget instead of custom layout
    def __init__(self, master=None, field_name=None, fields_data=None, templateName='', mode=0):
        super().__init__()
        self.addition = False
        self.current_expanded_data = []
        self.ExpandFlag = False
        self.fields_list = []
        self.modifyFlag = False
        self.name_field = 'Name'
        self.selection_type = []
        self.repeat_vals = False
        self.row_size = 1
        self.title = field_name
        self.type = 'dictionary'
        self.template_name = templateName

        self.custom_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.custom_layout)
        self.label_custom = SimpleFields.CustomLabel(master, field_name)
        self.label_custom.change_position('C')
        self.custom_layout.addWidget(self.label_custom)

        self.fieldsNames = fields_data['fields'].keys()
        # print(str(fields_data['options']))
        # print(str(self.fieldsNames))
        if fields_data:
            if 'options' in fields_data:
                if 'expand' in fields_data['options']:
                    self.ExpandFlag = True
                if 'multi_val' in fields_data['options']:
                    self.repeat_vals = True
                if 'limit' in fields_data['options']:
                    self.limit = fields_data['limit']
                else:
                    self.limit = 0
                if 'addition' in fields_data['options']:
                    self.addition = True
                if 'tooltip' in fields_data:
                    self.label_custom.setToolTip(fields_data['tooltip'])
        # else:
        #     print('expand dictionary in customer fields - missing options tags in field ' + field_name)
        # print(self.fieldsNames)
        # if templateName:
        #     field_address = templateName + '-' + self.title
        # else:
        #     field_address = ''
        # if not self.ExpandFlag or mode:
        for field_name in fields_data['fields']:
            field = createField(master, field_name, fields_data['fields'][field_name])
            self.fields_list.append(field)
            field.set_up_widget(self.custom_layout)
            self.row_size += field.row_size
            # rowposition += 3
        # print('expand dictionary row size - ' + str(self.row_size))
        if self.ExpandFlag:
            temp_button = SimpleFields.CustomButton(master, 'V V', self)
            self.custom_layout.addWidget(temp_button)
            temp_button.clicked.connect(self.add_data_to_treeview)
            # self.shortcut_add = QtWidgets.QShortcut(QtGui.QKeySequence('s'), self.fields_list[1])
            # self.shortcut_add = self.fields_list[1].set_up_shortcut('Ctrl+a')
            # self.shortcut_add.activated.connect(self.add_data_to_treeview)
            # self.fields_list[1].set_up_shortcut('Ctrl+w', self.add_data_to_treeview)
            self.tree_final_data = SimpleFields.ElementsList(master, all_edit=False, folders=False, class_connector=self)
            self.tree_final_data.set_up_widget(self.custom_layout)
            for data in fields_data['fields']:
                self.name_field = data
                break
            # self.tree_final_data.treeview.heading("#0", text='Double Click to Edit')
            # self.tree_final_data.doubleClicked.connect(self.on_double_click_edit_field)
        if fields_data['type'] == 'listDict':
            self.flag_listdict = True
        else:
            self.flag_listdict = False

    def set_val(self, values):
        if self.ExpandFlag:
            """just add data to treeview second function should be enough, since it requires already prepared data"""
            for fields in values:
                for data in fields:
                    if fields[data] == '':
                        return
                    else:
                        break
                break
            """need to transform. now its dictionaries in list. 
            need to make a big dictionary where key is name of item and value is data of item"""
            transformed_data = {}
            for fields in values:
                title = list(fields.values())[0]
                transformed_data[title] = fields
            self.tree_final_data.add_data(data=transformed_data)
            # self.add_data_to_treeview_2(values)
        else:
            # its working for now, lets leave it
            if isinstance(values, list):
                for fields, input_values in zip(self.fields_list, values):
                    temp = list(input_values.items())
                    # print(str(temp[0][1]))
                    fields.set_val(temp[0][1])
            else:
                for fields, input_values in zip(self.fields_list, values.items()):
                    fields.set_val(input_values[1])

    def get_val(self, temp_dict_container=None):
        if self.ExpandFlag:
            final_data = self.tree_final_data.get_data()
            transformed_data = []
            """need to get rid of row titles, they are just for display"""
            for data_dictionary in final_data:
                for key in data_dictionary:
                    temp_dict = {}
                    """data_dictionary[key] is a list of final dictionary variables"""
                    for correct_records in data_dictionary[key]:
                        if isinstance(correct_records, dict):
                            """here is correct data. also, all values are lists, but in case it's len is 1, change to string"""
                            for correct_key in correct_records:
                                if len(correct_records[correct_key]) == 1:
                                    correct_records[correct_key] = correct_records[correct_key][0]
                                temp_dict[correct_key] = correct_records[correct_key]
                        else:
                            temp_dict[correct_records] = ""
                transformed_data.append(temp_dict)
            final_data = transformed_data
        else:
            final_data = {}
            for name, values in zip(self.fieldsNames, self.fields_list):
                final_data[name] = values.get_val()
        if temp_dict_container is not None:
            temp_dict_container[self.title] = final_data
        else:
            return final_data

    def get_val_old(self, temp_dict_container=None):
        if self.ExpandFlag:
            # tempfinalList = self.current_expanded_data
            # for Parent in self.treeview_optionstochoose.treeview.get_children():
            #     tempdictinlist = {}
            #     templist = []
            #     for child in self.treeview_optionstochoose.treeview.get_children(Parent):
            #         tempdict = {}
            #         data = self.treeview_optionstochoose.treeview.item(child)["text"].split(':')
            #         tempdict[data[0]] = data[1]
            #         templist.append(tempdict)
            #     for item in self.fields_list:
            #         # print(item.title)
            #         # print(item.type)
            #         # item_occur = [k[item] for k in templist if k.get(item)]
            #         # print(len(item_occur))
            #         # if len(item_occur) > 1:
            #         if 'multilist' in item.type:
            #             templist2 = []
            #             for data in templist:
            #                 # print(list(data.keys())[0])
            #                 if list(data.keys())[0] == item.title:
            #                     templist2.append(list(data.values())[0])
            #             tempdictinlist[item.title] = templist2
            #         else:
            #             item_value = ''
            #             for data in templist:
            #                 if list(data.keys())[0] == item.title:
            #                     item_value = (list(data.values())[0])
            #                     break
            #             tempdictinlist[item.title] = item_value
            #     tempfinalList.append(tempdictinlist)
            # print(str(tempfinalList))
            # print('test')
            #     # if there is a child, it probably need to be a list, not create list, put in dictionary and put in list
            #     for child in self.treeview_optionstochoose.treeview.get_children(Parent):
            #             data = self.treeview_optionstochoose.treeview.item(child)["text"]
            #             templist.append(data)
            #     if templist:
            #         tempdictinlist[self.treeview_optionstochoose.treeview.heading('#0')['text']] = templist
            #         tempfinalList.append(tempdictinlist)
            #     # if templist is empty, then all data is in parent, separated with _ so turn it into a dictionary
            #     if not templist:
            #         tempdictinlist = {}
            #         data = self.treeview_optionstochoose.treeview.item(Parent)["text"]
            #         # print(data)
            #         listed_values = data.split('_')
            #         print(listed_values)
            #         for name, values in zip(self.fieldsNames, listed_values):
            #             tempdictinlist[name] = values
            #         tempfinalList.append(tempdictinlist)
            # # return a list of dictionaries of data from treevieww elements
            # # print("jest expand")
            tempfinalList = self.tree_final_data.get_data()
            # for roots in self.tree_final_data.treeview.get_children(''):
            #     tempfinalList.append(self.gather_data(roots))
        elif self.flag_listdict:
            tempfinalList = []
            for fields in self.fields_list:
                val1 = fields.title
                val2 = fields.get_val()
                tempdic = {val1: val2}
                tempfinalList.append(tempdic)
        else:
            """return a dictionary of values from self list. This is in case it is expected only 1 dictionary"""
            tempfinalList = {}
            for name, values in zip(self.fieldsNames, self.fields_list):
                tempfinalList[name] = values.get_val()
        if not tempfinalList:
            temp_dict = {}
            for fields in self.fields_list:
                temp_dict[fields.title] = fields.get_val()
            tempfinalList = [temp_dict]
        if temp_dict_container is not None:
            """it displays nested dictionaries as dict in dict, but for writing to file it should be dict in list.
            So lets iterate over all data again, and if value is a dictionary, replace it with a copy of list of
             contained dictionaries"""
            for root_vals in tempfinalList:
                if isinstance(root_vals, dict):
                    for vals in root_vals:
                        if isinstance(root_vals[vals], dict):
                            templist = []
                            """this replace should be a dictionaries to put in a list"""
                            for replace in root_vals[vals]:
                                # for i in root_vals[vals][replace]:
                                templist.append(root_vals[vals][replace])
                            root_vals[vals] = templist
            temp_dict_container[self.title] = tempfinalList
        else:
            return tempfinalList

    def clear_val(self):
        for item in self.fields_list:
            item.clear_val()
        if self.ExpandFlag:
            if self.modifyFlag:
                print('cool')
            else:
                self.tree_final_data.clear_tree()
                # for Parent in self.tree_final_data.treeview.get_children():
                #     self.tree_final_data.treeview.delete(Parent)
                # for data in self.current_expanded_data:
                #     self.current_expanded_data.remove(data)

    def destroy(self):
        self.to_delete_outside_layout.removeWidget(self)
        self.deleteLater()

    def set_up_widget(self, outside_layout, insert_for_options=False):
        self.to_delete_outside_layout = outside_layout
        if insert_for_options:
            outside_layout.insertWidget(outside_layout.count() - 1, self)
        else:
            outside_layout.addWidget(self)

    def add_data_to_treeview(self, insert=False):
        """since speaker field got limit of 12 items, first check if limit reached or not"""
        if self.limit > 0:
            if self.tree_final_data.tree_model.rowCount() >= self.limit:
                # messagebox.showerror('Limit reached', 'Only ' + str(self.limit) + ' allowed', parent=self)
                return
        """lets split it into 2 functions. one takes all data and pass to the other, recursive that puts it in treev"""
        if self.fields_list[0].get_val():
            data_var = {}
            values = []
            for fields in self.fields_list:
                """before, if 1 text was, it would combine key:value, but in some cases it would be 1 value in a list
                so lets keep all in a list, but expand leaf always"""
                value_from_field = fields.get_val()
                # if isinstance(value_from_field, list):
                values.append({fields.title: value_from_field})
                # else:
                #     values.append(fields.title + ':' + value_from_field)
                #     old code
                # for fields_name, input_values in zip(self.fieldsNames, self.fields_list):
                #     if isinstance(input_values, list):
                #         data_var[fields_name] = input_values.get_val()
                #     else:
                #         data_var[fields_name] = [input_values.get_val()]
                # """cant just append dictionaries to list, as in theory, each dictionary should be unique"""

                # if self.modifyFlag:
                #     self.modifyFlag = False
                #     root_item = self.tree_final_data.find_root_parent(self.tree_final_data.selected_item(value='code'))
                #     previous_data_index = self.tree_final_data.treeview.index(root_item)
                #     self.tree_final_data.treeview.delete(root_item)
                # else:
                #     previous_data_index = 'end'
                    # previous_data_index = self.treeview_optionstochoose.treeview.index()
                # if self.current_expanded_data:
                # for fields in self.current_expanded_data:
                #     if fields[self.name_field] == data_var[self.name_field]:
                #         previous_data_index = self.current_expanded_data.index(fields)
                #         self.current_expanded_data.remove(fields)
                            # self.current_expanded_data.insert(previous_data_index, final_data)

                # self.current_expanded_data.insert(previous_data_index, data_var)
                # final_data.append(data_var)
                # self.add_data_to_treeview_2([data_var], position_no=previous_data_index)
            # first field might return list. but i think it should always be 1 text
            data_var[self.fields_list[0].get_val()] = values
            self.tree_final_data.add_data(data=[data_var], insert_row=insert)
                # self.add_data_to_treeview_2([data_var], position_no=previous_data_index)
            for field in self.fields_list:
                field.clear_val()
        else:
            # messagebox.showwarning("missing name", 'Missing name', parent=self)
            return
        """here we expand child elements of added item. Item itself will not be expanded
        but for that I need index of added element, which is created after adding"""
        current_row_count = self.tree_final_data.tree_model.rowCount()
        last_item = self.tree_final_data.tree_model.item(current_row_count-1)
        if last_item.hasChildren():
            for idx in range(last_item.rowCount()):
                self.tree_final_data.expand(self.tree_final_data.tree_model.indexFromItem(last_item.child(idx)))
    # below should be obsolete VV
    def add_data_to_treeview_2(self, final_data_list, branch='', position_no='end'):
        """this should work recursive. if branch is empty, then its main list, so add branch with empty leaves.
        if branch is provided, then we are adding another dictionary no deeper level, so just name leave
        it will works as branch."""
        """its not always NAME"""
        if isinstance(final_data_list, dict):
            data_list = []
            for data in final_data_list:
                data_list.append(final_data_list[data])
            final_data_list = data_list
        for final_data in final_data_list:
            branch_title = final_data[self.name_field]
            if isinstance(branch_title, list):
                branch_title = branch_title[0]
            try:
                self.tree_final_data.add_data(data=final_data_list)
                # if branch:
                #     new_branch = self.tree_final_data.add_leaves(branch, [final_data[self.name_field]], update_flag=False)
                # else:
                #     new_branch = self.tree_final_data.add_branch(branch_title, [], position=position_no,
                #                                         update_flag=self.repeat_vals)
            except:
                print('error add data treeview 2')
                # otherFunctions.error_log('problem with adding data to treeview - GuiFieldClasses in line 1174')
                # otherFunctions.error_log('branch is ' + branch)
                # otherFunctions.error_log('adding  ' + str(final_data))
            for data in final_data:
                """if data is in list, it might be just list of values, or list of dictionaries
                Either way, add that leaf. Everything will be added to it"""
                if isinstance(final_data[data], list):
                    next_level_branch = self.tree_final_data.add_leaves(final_data[self.name_field],
                                                                            [data], update_flag=False)
                    templist = []
                    for values in final_data[data]:
                        if isinstance(values, dict):
                            """start this function again, but on already created leaf which will work as root branch"""
                            self.add_data_to_treeview_2([values], branch=next_level_branch)
                        else:
                            templist.append(values)
                    if templist:
                        self.tree_final_data.add_leaves(next_level_branch, templist,
                                                            update_flag=False)
                else:
                    temp = data + ':' + final_data[data]
                    self.tree_final_data.add_leaves_simple(new_branch, [temp])
                    # self.tree_final_data.add_leaves(new_branch, [temp], update_flag=False)
        # # if modify data, check index of selection, delete it and put new branch in its place
        # if self.modifyFlag:
        #     # current_item = self.treeview_optionstochoose.treeview.selection()[0]
        #     # current_index = self.treeview_optionstochoose.treeview.index(current_item)
        #     # self.treeview_optionstochoose.treeview.delete(current_item)
        #     self.buttonADD_controlTreeview['text'] = 'Add'
        # # self.treeview_optionstochoose.add_branch(branch_name, fields_list, update_flag=self.modifyFlag,
        # #                                          position=current_index)
        # # self.modifyFlag = False
        # # # self.treeview_optionstochoose.add_branch(fieldvals[:-1],fields_list)
    #
    # def del_data_to_treeview(self):
    #     if self.modifyFlag:
    #         self.modifyFlag = False
    #         self.buttonADD_controlTreeview['text'] = 'Add'
    #         self.buttonDEL_controlTreeview['text'] = 'Delete'
    #         for fields in self.fields_list:
    #             fields.clear_val()
    #     else:
    #         try:
    #             item = self.tree_final_data.treeview.selection()[0]
    #             item_to_del = self.tree_final_data.treeview.item(item)['text']
    #             self.tree_final_data.treeview.delete(item)
    #             for data in self.current_expanded_data:
    #                 if data[self.name_field] == item_to_del:
    #                     self.current_expanded_data.remove(data)
    #         except:
    #             print("nothing to delete")
    # def OnDoubleClick(self, event):
    #     # item = self.treeview_optionstochoose.treeview.identify("item", event.x, event.y)
    #     # item = self.treeview_optionstochoose.treeview.selection()[0]
    #     # print("you clicked on", self.treeview_optionstochoose.treeview.item(item)["text"])
    #     item = self.tree_final_data.treeview.selection()[0]
    #     # print(str(self.treeview_optionstochoose.treeview.index(item)))
    #     leaf_flag = self.tree_final_data.treeview.parent(item)
    #     # # print("you clicked on", self.treeview_optionstochoose.treeview.item(item, "text"))
    #     tempdic = {}
    #     index = 0
    #     if not leaf_flag:
    #         # print("clicked on parent")
    #         # oh man, first, prepare all items in leaf into a dictionary in a list object
    #         leaf_data = []
    #         leafs = self.tree_final_data.treeview.get_children(item)
    #         for leaf in leafs:
    #             tempdic = {}
    #             temp = self.tree_final_data.treeview.item(leaf)['text'].split(':')
    #             tempdic[temp[0]] = temp[1]
    #             leaf_data.append(tempdic)
    #         # print(str(leaf_data))
    #         # no check in field, if type is multilist, then values should be in list.
    #         # for now, other types usually uses strings
    #         for item in self.fields_list:
    #             # print(item.title)
    #             # print(item.type)
    #             # print(len(item_occur))
    #             if 'multilist' in item.type:
    #                 templist = []
    #                 for data in leaf_data:
    #                     # print(list(data.keys())[0])
    #                     if list(data.keys())[0] == item.title:
    #                         templist.append(list(data.values())[0])
    #                 item.set_val(templist)
    #                 # print("create list from values with same key")
    #             else:
    #                 # print('just return value, since only once it appears so it probably a text')
    #                 for data in leaf_data:
    #                     # print(list(data.keys())[0])
    #                     if list(data.keys())[0] == item.title:
    #                         item.set_val(list(data.values())[0])
    #     self.modifyFlag = True
    #     self.buttonADD_controlTreeview['text'] = 'Modify'
    #     #     # for leaf in leafs:
    #     #     #     print(self.treeview_optionstochoose.treeview.item(leaf)['text'])
    #     #     #     leaf_data = self.treeview_optionstochoose.treeview.item(leaf)['text'].split(':')
    #     #     #     if leaf_data[0] == leaf_name:
    #     #     #         leaf_list.append(leaf_data[1])
    #     #     #         leaf_name = leaf_data[0]
    #     #     #         continue
    #     #     #     else:
    #     #     #         leaf_val = leaf_data[1]
    #     #     #     leaf_name = leaf_data[0]
    #     #
    #     #     print("clicked on parent")
    #     #     # values = item.split('_')
    #     #     # for fields in self.fields_list:
    #     #     #     fields.set_val(values[index])
    #     #     #     index += 1
    #     # else:
    #     #     # data = self.treeview_optionstochoose.treeview.item(item)["text"]
    #     #     # print("leaf")
    #     #     # print(str(data))
    #     #     # for fields in self.fields_list:
    #     #     #     fields.set_val(data)
    #     #     return
    # def gather_data(self, item):
    #     temp_dict = {}
    #     temp_list = []
    #     for leaves in self.tree_final_data.treeview.get_children(item):
    #         value = self.tree_final_data.treeview.item(leaves)['text']
    #         value = value.split(':')
    #         if len(value) == 2:
    #             temp_dict[value[0]] = value[1]
    #         elif len(value) == 1:
    #             if self.tree_final_data.treeview.get_children(leaves):
    #                 """this is used only in pictures field, where to display, dictionary is put in another dictionary,
    #                  but it causes problem to load data from treeview. So, since it is used in one place only,
    #                   I added line to dive in treeview twice, to avoid first dictionary and prepare list from
    #                    remaining dicts."""
    #                 temp_list_2 = []
    #                 for image_leaf in self.tree_final_data.treeview.get_children(leaves):
    #                     temp_list_2.append(self.gather_data(image_leaf))
    #                     # temp_dict[value[0]] = self.gather_data(image_leaf)
    #                 temp_dict[value[0]] = temp_list_2
    #             else:
    #                 temp_list.append(value[0])
    #     if temp_list:
    #         return temp_list
    #     else:
    #         return temp_dict
    # def on_double_click_edit_field(self, event):
    #     if GlobalVariables.flag_addition or GlobalVariables.flag_modify_addition:
    #         if self.addition:
    #             flag = True
    #         else:
    #             flag = False
    #     else:
    #         flag = True
    #     if flag:
    #         region = self.tree_final_data.treeview.identify("region", event.x, event.y)
    #         if region == "heading":
    #             Edit_Data_Window.ElementEditWindow(structure_path=self.template_name + '-' + self.title,
    #                                            structure_data=self.get_val(), structure_link=self)
    #
    # def bind_control(self, binding):
    #     if binding:
    #         self.tree_final_data.bind('<Double-Button-1>', self.on_double_click_edit_field)
    #     else:
    #
    #         self.tree_final_data.unbind('<Double-Button-1>')

    # def hide_field(self):
    #     self.pack_forget()
    #
    # def show_field(self):
    #     self.field_frame.pack()


class EDF_forcombatDialogue(ExpandDictionaryField):
    """updated from basic expanddictionaryfield. There are additional stuff, like setMusitTo or something else that
    need custom code"""
    def __init__(self, master=None, field_name=None, fields_data=None):
        super().__init__(master, field_name, fields_data)
        # connect first field - line triggers - to custom trigger here
        self.label_custom.change_position('center')
        self.fields_list[0].final_data.textChanged.connect(self.trigger_custom)
        self.tree_final_data.doubleClicked.connect(self.edit_data)
        self.edit_flag = False
    """probably, double click on anything, check root, take all data from root parent and put in proper fields"""
    # custom get_val, as origin getval will add titles to files
    def get_val(self, temp_dict_container=None):
        final_data = self.tree_final_data.get_data()
        transformed_data = []
        """need to get rid of row titles, they are just for display"""
        for data_dictionary in final_data:
            for key in data_dictionary:
                temp_dict = {}
                """data_dictionary[key] is a list of final dictionary variables"""
                for correct_records in data_dictionary[key]:
                    """here is correct data. also, all values are lists, but in case it's len is 1, change to string"""
                    for correct_key in correct_records:
                        if len(correct_records[correct_key]) == 1 and correct_key != 'theText':
                            correct_records[correct_key] = correct_records[correct_key][0]
                        temp_dict[correct_key] = correct_records[correct_key]
            transformed_data.append(temp_dict)
        if temp_dict_container is not None:
            temp_dict_container[self.title] = transformed_data

    def add_data_to_treeview(self):
        """check trigger and its options. in some cases there are limits"""
        trigger = self.fields_list[0].get_val()
        options = Glob_Var.lineTriggers[trigger]['move']
        if 'empty' in options:
            """it means field MOVE should be left empty"""
            self.fields_list[1].clear_val()
        if 'limit' in options:
            """if limit-10, specific trigger should appear withing first 10 rows.
            first check if rows is selected - check which rows it is to insert.
            if nothing is selected, check amount of current rows in list"""
            limitNO = Glob_Var.lineTriggers[trigger]['limit']
            selected_row = self.tree_final_data.selected_element()
            if selected_row:
                if selected_row.row() > int(limitNO):
                    show_message('Start entry', 'this trigger must be place \n within first 10 records','Starter Trigger')
                    return
            else:
                if self.tree_final_data.tree_model.rowCount() > int(limitNO):
                    show_message('Start entry', 'this trigger must be place \n within first 10 records','Starter Trigger')
                    return
        if 'mandatory' in options:
            if not self.fields_list[1].get_val():
                self.fields_list[1].label_custom.change_background_color()
                return
        self.fields_list[1].label_custom.clear_color()
        if self.edit_flag:
            self.edit_flag = False
            super().add_data_to_treeview(insert=self.edit_insert_row)
            return
        super().add_data_to_treeview()

    def edit_data(self):
        selected_value = self.tree_final_data.selected_element()
        if not selected_value.child(0, 0):
            self.edit_insert_row = self.tree_final_data.find_root_parent(selected_value).row()
            self.edit_flag = True
            # problem here, if setting first value, should probably give list for second values
            # TODO getData
            temp = []
            data_to_edit = self.tree_final_data.get_data(self.tree_final_data.find_root_parent(selected_value), temp)
            # this make temp like this [dict[key-root:[{linetrigger:[value]},{move:[value]},]]
            # so need to remake this list of dictionaries of lists into proper structure
            temp_list_2 = []
            restructirized = ['lineTrigger-singlevalue','move-list','Text-list']
            for root_dict in temp:
                for root_name in root_dict:
                    for field_val_pair_dict in root_dict[root_name]:
                        for value_in_field in field_val_pair_dict:
                            temp_list_2.append(field_val_pair_dict[value_in_field])
            restructirized[0] = temp_list_2[0][0]
            restructirized[1] = temp_list_2[1]
            restructirized[2] = temp_list_2[2]
            # not put restructurized value in fieldlist
            for idx in range(len(self.fields_list)):
                self.fields_list[idx].clear_val()
                self.fields_list[idx].set_val(restructirized[idx])

    def trigger_custom(self):
        trigger = self.fields_list[0].get_val()
        # options = Glob_Var.lineTriggers[trigger]['move']
        if trigger == 'SetMusicTo':
            # self.trigger_file()
            self.fields_list[2].flag_file = True
        else:
            self.fields_list[2].flag_file = False

    def trigger_file(self):
        self.fields_list[1].flag_file = True
        # TODO finish combat field - when selected music, second field should load file
        """change second field in field list - move - to instead load file"""

    def set_val(self, values):
        """this should be list of dictionaries,
        [{
            "lineTrigger": "StanceStruggleFree",
            "move": "Making Out",
            "theText": [
                "And manage to push the insistent Nereid away!",
                "And free your mouth from the Nereid's wet smooches!"
            ]
        }]
        so make 'linetrigger + move' as key of this dictionary"""
        final_data_to_insert = []
        for fields in values:
            new_key = fields['lineTrigger']
            if new_key == 'SetMusicTo':
                for files in fields['move']:
                    temp = files.split('/')
                    filename = temp[-1]
                    self.fields_list[2].files_container[filename] = files
                    files = filename
            if isinstance(fields['move'], str):
                new_key += '-' + fields['move']
            temp_value = {new_key: fields}
            final_data_to_insert.append(temp_value)
        self.tree_final_data.add_data(data=final_data_to_insert)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.edit_flag = False
            for fields in self.fields_list:
                fields.clear_val()
        super().keyPressEvent(event)

class FunctionField(SimpleFields.ElementsList):
    def __init__(self, flag_for_list_of_functions=False, master=None, view_title="Scenes"):
        super().__init__(masterWun=master, listTitle=view_title, search_field=True, folders=False)
        """this is just container for scenes. Most of stuff will be done by MarkUpWindow.
        Basicly, its just element list. Double click on root - eventText, to open Markup with no data.
        Doubleclick on bottom element - load scene to edit"""
        self.entry_search.hide()
        self.title = view_title
        self.type = 'functionfield'
        self.row_size = 12
        # print(str(fields_data))
        """each type of scene will have its own frame. in case there is a scene with different setup. 
            Then I just hide or show specific frame instead of all fields"""
        self.field_frame = {}
        self.markup_win = None
        self.label_custom = SimpleFields.CustomLabel(None, 'Scenes')
        self.layout.insertWidget(0, self.label_custom, alignment=Qt.AlignCenter)
        self.treeview_scenes = self
        self.treeview_scenes.doubleClicked.connect(self.modify_scene)
        # TODO scene lookup in main window
        # self.area_lookup = SimpleFields.AreaEntry(self, width_i=40)
        # self.area_lookup.field.configure(state='disabled')
        # self.area_lookup.grid(row=rowposition+6, column=colpos, columnspan=1)
        # self.list_scenes.treeview.bind("<<TreeviewSelect>>", lambda e: self.display_scene_text(self.list_scenes))
        """fields setup - eventtext:{keys:values,fields:{keys:values}}"""
        self.field_setup = {}
        self.scene_data_container = {}
        self.edition_flag = False
        self.dict_fields_with_setvals_for_scene_edition = {}

        self.flag_prepare_event_logic_data = False

    def set_val(self, values, event_type=False):
        """event type is needed, since if there are more then 1 function types, instead of making more fields taking
         more space, i made dummy objects with reference to first function fields. Only first operates data,
          dummy only sets and gets values. Each field has a title which is field name and main branch in display
          values should be list of dictionaries with nameofthescene:name, scene"scenetext"""
        if not event_type:
            event_type = self.title
        templist = []
        for scenes in values:
            if scenes['NameOfScene'] == '':
                return
            self.scene_data_container[event_type][scenes['NameOfScene']] = scenes
            # templist.append(scenes['NameOfScene'])
        for scene_name in self.scene_data_container[event_type]:
            templist.append(scene_name)
        self.treeview_scenes.add_data(templist, event_type, update_flag=False)
        self.treeview_scenes.open_tree()

    def get_val(self, event_type=False, temp_dict_container=None):
        if not event_type:
            event_type = self.title
        templist = []
        for scenes in self.scene_data_container[event_type]:
            templist.append(self.scene_data_container[event_type][scenes])
        if not templist:
            """fields setup - eventtext:{keys:values,fields:{keys:values}}"""
            tempdict = {}
            for field in self.field_setup[event_type]:
                tempdict[field] = ''
            templist.append(tempdict)
        if temp_dict_container is not None:
            temp_dict_container[self.title] = templist
        else:
            return templist

    def clear_val(self):
        temp_list = []
        for roots_no in range(self.tree_model.rowCount()):
            temp_list.append(self.tree_model.item(roots_no).text())
        self.tree_model.clear()
        self.add_data(temp_list)
        for event_type in self.scene_data_container:
            self.scene_data_container[event_type] = {}

    def modify_scene(self, quick_load=None):
        """cant remember what was that for"""
        if not self.flag_prepare_event_logic_data:
            self.flag_prepare_event_logic_data = True
        """changes approach. this just displayes data. so user double clicks on any row, it opens markup and passes
        model from this tree. in Markup user create and also modified scene list"""
        # scene_name = ''
        # scene_fields_setup = {}
        # selected_item = self.treeview_scenes.selected_element()
        # """first check if proper item is selected. for adding - only root works. for edit - only leaf, include root"""
        # if not selected_item.child(0, 0):
        #     """if no child, it should be parent item so user is adding new scene"""
        #     root_scene_setup_name = selected_item.parent().text()
        #
        # else:
        #     # self.edition_flag = True
        #     if not selected_item.parent():
        #         show_message('wrong selection', 'Please select event scene', '')
        #         return
        #     scene_name = selected_item.text()
        #     root_scene_setup_name = selected_item.parent().text()
        #     scene_text = self.scene_data_container[root_scene_setup_name][scene_name]
            # scenedata_to_load = self.scene_data_container[root_scene_setup_name][scene_name]
        # root_scene_setup_name = self.list_scenes.treeview.parent(selected_item_code)
            # root_scene_setup_name = self.list_scenes.treeview.parent(root_scene_setup_name)
            # if self.list_scenes.treeview.parent(root_scene_setup_name):
            #     root_scene_setup_name = self.list_scenes.treeview.parent(root_scene_setup_name)
        # scene_fields_setup[root_scene_setup_name] = self.field_setup[root_scene_setup_name]
        # self.button_AddData['text'] = 'Save Scene'
        # self.button_AddData.bind('<Button-1>', self.save_scene)
        # self.button_ModifyData['text'] = 'Cancel'
        # self.button_ModifyData.bind('<Button-1>', self.cancel_scene)
        """go over all frames, hide them, then show the one that is selected"""
        # for event_type in self.field_frame:
        #     self.field_frame[event_type]['frame'].grid_forget()
        # self.field_frame[root_scene_setup_name]['frame'].grid(row=1, column=0, columnspan=1)
        """if there is a scene selected, then it probably to edit, to put data in fields too"""
        # if scene_name:
        #     for field, values in zip(self.field_frame[root_scene_setup_name]['fields'],
        #                              self.scene_data_container[root_scene_setup_name][scene_name]):
        #         self.field_frame[root_scene_setup_name]['fields'][field].set_val(self.scene_data_container[root_scene_setup_name][scene_name][values])
        # SceneWindow(scene_fields_setup, self.list_scenes, self.scene_data_container,
        #             flag_list_of_functions=functionFlag, scene_data_to_load=scenedata_to_load)
        # FunctionalWindow.SceneWindow(scene_fields_setup, self.dict_fields_with_setvals_for_scene_edition[root_scene_setup_name],
        #             flag_list_of_functions=functionFlag, scene_data_to_load=scenedata_to_load)

        # SimpleFields.mod_temp_data.current_editing_event = Glob_Var.access_templates['Events'].input_filename.get_val()
        # Window_txt_markup.SceneWindow(source_field=self, scene_data_to_load=scene_text, event_type=root_scene_setup_name,
        #                               master=self, fields_data=self.field_setup[root_scene_setup_name])
        # if not self.markup_win:
        markup_win = MarkUpDialog.MarkUp_Window(target_field=self.treeview_scenes, scenes_flag=True, current_scene_list=self.scene_data_container,
                                                scene_data=self.field_setup, quick_load_scene=quick_load)
        markup_win.show()
    # if i figure out how to use this then ill uncomment it
    # def delete_scene(self):
    #     branchdeleteflag = messagebox.askokcancel("DELETING WHOLE SCENE",
    #                                               "You are about to delete this scene\n Are you sure?", parent=self)
    #     if branchdeleteflag:
    #         parent = self.treeview_scenes.treeview.parent(self.treeview_scenes.treeview.focus())
    #         if parent:
    #             self.treeview_scenes.delete_leaf(self.treeview_scenes.treeview.focus())
    #             if self.treeview_scenes.treeview.parent(parent):
    #                 self.treeview_scenes.delete_leaf(parent)
    #         else:
    #             messagebox.showwarning("STOP RIGHT THERE", 'Whoa, cannot delete root, it is important', parent=self)

    def display_scene_text(self, treevieID):
        # TODO maybe add
        # for now not used but working
        # treevieID is just variable for elementlist, so access treeview in it, get selected item idx or parent idx,
        """expected display - root parent which is event type(event,loss,victory scene) with scenes names as leaves
            if user selected root - do nothing. So user selected leaf. Check branch for even type and display theScene
            from scene data container. Keys should be same as scene name"""
        curItem = treevieID.treeview.focus()
        scene_type = treevieID.treeview.parent(curItem)
        curItem = treevieID.selected_item()
        explanation_text = ''
        if scene_type:
            for texts in self.scene_data_container[scene_type][curItem]['theScene']:
                # if isinstance(texts,dict):
                #     texts = list(texts.keys())[0]
                explanation_text += texts + '\n'
        else:
            return
        self.area_lookup.field.configure(state='normal')
        self.area_lookup.field.delete(1.0, tk.END)
        self.area_lookup.field.insert(1.0, explanation_text)
        self.area_lookup.field.configure(state='disabled')

    def add_new_field(self, fields_data, main_field_name, label_to_hide=None, dummy_field=None):
        self.treeview_scenes.add_data(main_field_name)
        self.field_setup[main_field_name] = fields_data
        # container example :
        #  {eventtext:{name1:{nameofscene:name1, text:sometest},name2:{keyname:valname, keytext:valtext}}}
        #  this way should be easy to add and modify at same spot. index within root children is always the same.
        self.scene_data_container[main_field_name] = {}
        """only 1 function field exists. others are dummies that send and get data from main field"""
        self.dict_fields_with_setvals_for_scene_edition[main_field_name] = dummy_field

    # def save_scene(self):
    #     """previously main display had basic scene data, scene text was kept in scene container. So user had to click
    #     'save' to save entire scene data. Now the markup field might as well save scene data"""
    #     """this is save scene with eventtext attributes and all scenes included"""
    #     temp_dict = {}
    #     selected_item_code = self.treeview_scenes.selected_item(value='code')
    #     event_type = self.treeview_scenes.treeview.parent(selected_item_code)
    #     if event_type:
    #         event_type = self.treeview_scenes.treeview.item(event_type)['text']
    #     else:
    #         event_type = self.treeview_scenes.treeview.item(selected_item_code)['text']
    #     if self.field_frame[event_type]['fields']['NameOfScene'].get_val():
    #         for fields in self.field_frame[event_type]['fields']:
    #             if fields == 'theScene':
    #                 value = self.field_frame[event_type]['fields'][fields].list
    #                 """since functions are made to be first funt name then list of attributes, and later i need scene
    #                  data container to contains only strings, here i need to transform any list in list into strings.
    #                 and function window should transform it back on its own, based on function title"""
    #                 templist = []
    #                 for val in value:
    #                     if isinstance(val,list):
    #                         for v in val:
    #                             templist.append(v)
    #                     else:
    #                         templist.append(val)
    #                 value = templist
    #             else:
    #                 value = self.field_frame[event_type]['fields'][fields].get_val()
    #
    #             temp_dict[fields] = value
    #             self.field_frame[event_type]['fields'][fields].clear_val()
    #         self.scene_data_container[event_type][temp_dict['NameOfScene']] = temp_dict
    #         self.treeview_scenes.add_leaves(event_type, [temp_dict['NameOfScene']], update_flag=False)
    #         self.button_AddData['text'] = 'Add Scene'
    #         self.button_AddData.bind('<Button-1>', lambda e:  self.modify_scene(False, add_flag=True))
    #         self.button_ModifyData['text'] = 'Edit Scene'
    #         self.button_ModifyData.bind('<Button-1>', lambda e: self.modify_scene(False))
    #         for event_type in self.field_frame:
    #             self.field_frame[event_type]['frame'].grid_forget()
    #     else:
    #         messagebox.showwarning('Missing name', 'Please input scene name', parent=self)
    #
    # def cancel_scene(self, *args):
    #     selected_item_code = self.treeview_scenes.selected_item(value='code')
    #     event_type = self.treeview_scenes.treeview.parent(selected_item_code)
    #     if event_type:
    #         event_type = self.treeview_scenes.treeview.item(event_type)['text']
    #     else:
    #         event_type = self.treeview_scenes.treeview.item(selected_item_code)['text']
    #     # for fields in self.field_frame[event_type]['fields']:
    #     #     self.field_frame[event_type]['fields'][fields].clear_val()
    #     self.button_AddData['text'] = 'Add Scene'
    #     self.button_AddData.bind('<Button-1>', lambda e:  self.modify_scene(False, add_flag=True))
    #     self.button_ModifyData['text'] = 'Edit Scene'
    #     self.button_ModifyData.bind('<Button-1>', lambda e: self.modify_scene(False))
    #     for event_type in self.field_frame:
    #         self.field_frame[event_type]['frame'].grid_forget()
    #
    # def add_scene_button_obsolete(self, *args):
    #     # self.list_scenes
    #     # load_data = self.field_frame[main_field_name]['fields']['theScene'].list
    #     selected_item_code = self.treeview_scenes.selected_item(value='code')
    #     event_type = self.treeview_scenes.treeview.parent(selected_item_code)
    #     event_type = self.treeview_scenes.treeview.item(event_type)['text']
    #     if self.edition_flag:
    #         # selected_item_code = self.list_scenes.selected_item(value='code')
    #         # event_type = self.list_scenes.treeview.parent(selected_item_code)
    #         # event_type = self.list_scenes.treeview.item(event_type['text'])
    #         selected_item = self.treeview_scenes.selected_item()
    #         data_to_load = self.scene_data_container[event_type][selected_item]
    #     else:
    #         data_to_load = ''
    #     Window_txt_markup.SceneWindow(source_field=self, scene_data_to_load=data_to_load, event_type=event_type)


class Functional_Dummy:
    def __init__(self, main_functional_field, view_title=''):
        self.main_field = main_functional_field
        self.title = view_title
        self.row_size = 6

    def set_val(self, values):
        self.main_field.set_val(values, event_type=self.title)

    def get_val(self, temp_dict_container=None):
        if temp_dict_container is not None:
            temp_dict_container[self.title] = self.main_field.get_val(event_type=self.title)
        else:
            return self.main_field.get_val(event_type=self.title)

    def clear_val(self):
        return


class CombatTrigger(SimpleFields.ElementsList):
    """this should write data as a list into the current mod
    display element list. add new row with text 'doubleclick to edit'
    check user if clicked 'enter' then check if last row is as above. if now, add new row
     double click to edit and write text.
     change get, set val to include new rows"""
    # def __init__(self, master=None,  field_name=None, tooltip_text=None, label_position='U', fields=None):
    #     super().__init__(master=master, label='', tooltip=None, label_pos=None)
    def __init__(self, master=None, field_name='', fields_data=None):
        super().__init__(master, field_name)
        self.title = field_name
        self.files_container = {}
        self.data = []
        self.row_size = 6
        self.flag_child_editable = True
        self.flag_folders = False
        self.add_leaf(['doubleclick to edit'], row_height=40)
        self.doubleClicked.connect(self.on_double_click)
        self.activated.connect(self.edit_selected)
        self.max_text_length = 20
        self.setWordWrap(True)
        self.setMaximumHeight(40)
        # self.display_flag = False
        # self.index = 0
        # self.modify_flag = False
        """in case trigger is music list"""
        self.flag_file = False

    def edit_selected(self):
        if self.flag_file:
            return
        current_index = self.selectedIndexes()[0]
        self.edit(current_index)
        self.on_double_click(current_index)

    def on_double_click(self, index):
        """this flag is specific for monaster>combat dialogue>line trigger. set music to refers to files. so then
        when clicked on THETEXT, it should open file dialog where user select multiple files. then, add then to list"""
        if self.flag_file:
            file = QtWidgets.QFileDialog.getOpenFileNames(self, "Select files")
            file_list = []
            if file[0]:
                self.delete_leaf('doubleclick to edit')
                for files in file[0]:
                    file_path_start = files.find('game/')
                    temp = files.split('/')
                    filename = temp[-1]
                    file_path = './' + files[file_path_start:]
                    self.files_container[filename] = file_path
                    file_list.append(filename)
                self.set_val(file_list)
        else:
            self.setCurrentIndex(index)
            self.edit(index)
            self.tree_model.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        self.tree_model.itemChanged.disconnect()
        if len(item.text()) > self.max_text_length:
            self.change_row_color(item, 'bad')
            current_text = item.text()
            last_chara = current_text[self.max_text_length]
            temp = current_text.split(last_chara)
            current_text = temp[0] + '/' + last_chara + temp[1]
            item.setText(current_text)
        else:
            self.change_row_color(item, 'good')
        if item.row() == self.tree_model.rowCount() - 1:
            if item.text() != "doubleclick to edit":
                self.add_leaf(["doubleclick to edit"], row_height=40)
    def set_val(self, values):
        # TODO how to deal with values here
        self.clear_tree()
        self.add_data(data=values)
        self.change_row_height(40)
        self.add_leaf(["doubleclick to edit"], row_height=40)

    def get_val(self, temp_dict_container=None):
        if self.flag_file:
            final_data = list(self.files_container.values())
            self.files_container.clear()
        else:
            final_data = self.get_data()
            final_data.pop(-1)
        if temp_dict_container is not None:
            temp_dict_container[self.title] = final_data
        else:
            return final_data

    def clear_val(self):
        self.clear_tree()
        self.add_leaf(["doubleclick to edit"], row_height=40)
   #
    # def load_line_triggers(self):
    #     tempdic = {}
    #     tempdic['test1'] = {}
    #     tempdic['test1']['trigger1'] = {'test1':'val1'}
    #     return tempdic
    #
    # def logics(self):
    #     options = self.line_triggers_dict[self.var.get()]
    #     if 'disable move' in options:
    #         self.fields_list[1].clear_val()
    #         self.fields_list[1].configure(state='disabled')
    #     else:
    #         self.fields_list[1].configure(state='enabled')
        # if 'first 10' in options:


    # def set_val(self, values):
    #     if self.ExpandFlag:
    #         # branch_name = ''
    #         for input_dictionary_list_element in values:
    #             branch_name = ''
    #             input_value = ''
    #             for fields_names, fields_values in input_dictionary_list_element.items():
    #                 if branch_name == '':
    #                     branch_name = fields_values
    #                 input_value += fields_values + '_'
    #             try:
    #                 self.treeview_combat_text.add_branch(branch_name, [input_value])
    #             except:
    #                 print("Failed to set values to list dictionary fields")
    #         # self.treeview_optionstochoose.add_branch(branch_name, [fieldList])
    #     else:
    #         #     print(str(values))
    #         for fields, input_values in zip(self.fields_list, values):
    #             # print('values - '+ str(input_values))
    #             fields.set_val(list(input_values.values())[0])
    #
    # def get_val(self, temp_dict_container=None):
    #     if self.ExpandFlag:
    #         tempdict = []
    #         for Parent in self.treeview_optionstochoose.treeview.get_children():
    #             # print(self.treeview_optionstochoose.treeview.item(Parent)["text"])
    #             for child in self.treeview_optionstochoose.treeview.get_children(Parent):
    #                 tempdictinlist = {}
    #                 data = self.treeview_optionstochoose.treeview.item(child)["text"]
    #                 # print(data)
    #                 listed_values = data[:-1].split('_')
    #                 # print(listed_values)
    #                 for name, values in zip(self.fieldsNames, listed_values):
    #                     tempdictinlist[name] = values
    #                 tempdict.append(tempdictinlist)
    #         # return a list of dictionaries of data from treevieww elements
    #         # print("jest expand")
    #     else:
    #         # return a dictionary of values from self list
    #         tempdict = []
    #         for name, values in zip(self.fieldsNames, self.fields_list):
    #             templistD = {}
    #             templistD[name] = values.get_val()
    #             tempdict.append(templistD)
    #     if temp_dict_container is not None:
    #         temp_dict_container[self.title] = tempdict
    #     else:
    #         return tempdict
    #
    # def clear_val(self):
    #     for item in self.fields_list:
    #         item.clear_val()
    #     if self.ExpandFlag:
    #         for Parent in self.treeview_combat_text.treeview.get_children():
    #             self.treeview_combat_text.treeview.delete(Parent)
    #
    # def add_data_to_treeview(self):
    #     index = 0
    #     fieldList = ''
    #     branch_name = ''
    #     if self.modify:
    #         position = self.treeview_combat_text.treeview.index(self.treeview_combat_text.selected_item(value='code'))
    #         self.del_data_to_treeview()
    #         self.modify = False
    #     else:
    #         position = 'end'
    #     branch_name = self.fields_list[2].get_val()
    #     self.fields_list[2].clear_val()
    #     if branch_name:
    #         self.treeview_combat_text.add_branch(otherFunctions.wrap(branch_name, 30), [], position = position,
    #                                              update_flag=False)
    #
    # def del_data_to_treeview(self):
    #     self.treeview_combat_text.treeview.delete(self.treeview_combat_text.selected_item(value='code'))
    #
    # def OnDoubleClick(self, event):
    #     """this load selected item into the fields, to modify them"""
    #     self.modify = True
    #     self.fields_list[2].clear_val()
    #     self.fields_list[2].set_val(self.treeview_combat_text.selected_item())
    #     # item = self.treeview_optionstochoose.treeview.selection()[0]
    #     # leaf_flag = self.treeview_optionstochoose.treeview.parent(item)
    #     # print("you clicked on", self.treeview_optionstochoose.treeview.item(item, "text"))
    #     # index = 0
    #     # if leaf_flag:
    #     #     # print("clicked on leaf")
    #     #     values = item.split('_')
    #     #     for fields in self.fields_list:
    #     #         fields.set_val(values[index])
    #     #         index += 1
    #     # else:
    #         # print("not leaf")
    #         # return

class FetishApply:
    def __init__(self, master=None, field_name=None, fields_data=None):
        self.title = field_name
        self.fields_set = fields_data['fields']
        self.final_data_tree = SimpleFields.ElementsList(master, "Fetishes", class_connector=self)
        self.final_data_tree.setHeaderHidden(False)
        header_labels = []
        for field in self.fields_set:
            header_labels.append(field['name'])
            # self.final_data_tree.tree_model.setHorizontalHeaderItem(self.fields_set.index(field), QStandardItem(field['name']))
        self.final_data_tree.tree_model.setHorizontalHeaderLabels(header_labels)
        self.final_data_tree.setColumnWidth(1, 3)
        self.final_data_tree.setMaximumHeight(110)
        self.selection_type = 'Fetishes Addictions'
        self.row_size = 4

    def set_val(self, values):
        # self.fields_display_row = 1
        if isinstance(values, str):
            values = [values]
        for value in values:
            if value == '':
                continue
            if '|/|' in value:
                value_to_enter = value.split('|/|')
            else:
                value_to_enter = [value, '0']
            self.final_data_tree.add_leaf(value_to_enter, editable=True)
    #         this editable refers to both items and I need 0 to be editable

    def get_val(self, temp_dict_container=None):
        list_data = self.final_data_tree.get_data()
        """this should return [[name, value],name]"""
        """nonetype is when its empty value, so just name should be"""
        final_data = []
        for values in list_data:
            if isinstance(values, list):
                if values[1] == 0:
                    final_data.append(values[0])
                else:
                    final_data.append(values[0] + '|/|' + values[1])
            else:
                final_data.append(values)

        if not final_data:
            final_data = ['']
        if temp_dict_container is not None:
            temp_dict_container[self.title] = final_data
        else:
            return final_data

    def clear_val(self):
        self.final_data_tree.clear_tree()

    def set_up_widget(self, outside_layout=QtWidgets.QLayout):
        outside_layout.addWidget(self.final_data_tree)


class MonsterGroups:
    def __init__(self, master=None, view_title=''):
        """add multilist display with single element and button to add.
        when nothing selected, adds new group
        when selected root group, add to that group
        when selected row in group, insert above"""
        self.addition = True
        self.add_button = SimpleFields.CustomButton(master, 'Add Monster or Group', self)
        self.label_custom = self.add_button
        self.add_button.clicked.connect(self.create_new_group)
        self.add_button.setToolTip('Button to add new group.\n'
                                   'Select group then double click on monster in main view to add')
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.fields_list = []
        self.title = view_title
        self.type = 'multilist'
        self.template_name = 'Adventures'
        self.treeview_MonsterFinalList = SimpleFields.ElementsList(master, 'Double click to Edit', class_connector=self)
        self.treeview_MonsterFinalList.setFixedWidth(160)
        self.treeview_MonsterFinalList.setFixedHeight(70)
        self.fields_list.append(self.treeview_MonsterFinalList)
        self.selection_type = 'Monsters'
        self.row_size = 3
        self.custom_layout.addWidget(self.add_button)
        self.treeview_MonsterFinalList.set_up_widget(self.custom_layout)

    def set_val(self, values):
        # if loading data, it should be cleared first, so nothing is selected.
        # so if nothing selected, and no data available(new group), just add everything
        # if there is a groups, then its adding new rows to that last group
        current_selection = self.treeview_MonsterFinalList.selected_element()
        if not current_selection:
            groups_in_tree = self.treeview_MonsterFinalList.tree_model.rowCount()
            if groups_in_tree:
                last_group = self.treeview_MonsterFinalList.tree_model.item(groups_in_tree-1)
                new_item = QStandardItem(values)
                last_group.appendRow(new_item)
            else:
                if isinstance(values, str):
                    return
                else:
                    # previously, it would change group name to reflect what it consist of, that needs more coding here
                    self.treeview_MonsterFinalList.add_data(data=values)
        else:
            # if something is selected, then
            # if selected group, add to the group, if item from group, add before it
            new_item = QStandardItem(values)
            if current_selection.parent():
                current_selection.parent().insertRow(current_selection.row(), new_item)
            else:
                current_selection.appendRow(new_item)
            return

    def get_val(self, temp_dict_container=None):
        temp_final_list = self.treeview_MonsterFinalList.get_data()
        if temp_dict_container is not None:
            temp_dict_container[self.title] = temp_final_list
        else:
            return temp_final_list

    def clear_val(self):
        self.treeview_MonsterFinalList.clear_tree()

    def create_new_group(self):
        """just add new group"""
        self.treeview_MonsterFinalList.add_data(data=['Group'])

    def set_up_widget(self, outside_layout):
        outside_layout.addLayout(self.custom_layout)


class OptionalFields(SimpleFields.ElementsList):
    def __init__(self, master=None, fields_data=None, main_layout=None):
        super().__init__(master, folders=False)
        """idea is, there will be 1 object for all templates, and when getting, it will get data from this, and when
         setting, if field is not mandatory(not found in template list) it is passed to this object.
         This object will take care of all optional fields, retrieve and set data in them, hide and show.
        1 treeview, working similar to perkTypes. Double click lowest item to add it SELECTED VALUES and create field.
         """
        self.title = 'optional'
        self.change_title('Optional fields')
        self.label_custom = SimpleFields.CustomLabel(None, '')
        self.row_size = 6
        self.main_widget = master
        """just in case, lets put it all in seperate frame. Main frame is horizontal, and fields will be put vertivally
        , similar to create fields in templates.
        This optional object along with other optional fields should be but in new layout in main layout so its easy to 
        distinguish them"""
        self.template_main_laout = main_layout
        self.optional_field_frame = QtWidgets.QVBoxLayout()
        self.optional_field_frame.setAlignment(Qt.AlignCenter)
        """this will be dictionary of created fields, for which will set and get vals"""
        self.optional_fields_dict = {}

        self.selected_values_display_row = QStandardItem('SELECTED VALUES')
        self.selected_values_display_row.setEditable(False)
        self.tree_model.appendRow(self.selected_values_display_row)
        self.doubleClicked.connect(self.adds_selected)
        self.selected_values = {}
        self.loaded_data = False
        self.optional_options = fields_data
        self.load_main_data()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.restore_selected()
        # super().keyPressEvent(event)

    def set_up_widget(self, outside_layout, insert=None):
        self.template_main_laout.addLayout(self.optional_field_frame)
        self.optional_field_frame.addWidget(self)
        self.optional_field_frame.addStretch(1)
        # how to insert widgets before stretch
        # temp = SimpleFields.SimpleEntry(None, 'test')
        # self.optional_field_frame.insertWidget(self.optional_field_frame.count()-1, temp)
        #TODO

    def get_val(self, temp_dict_container):
        for field in self.optional_fields_dict:
            temp_dict_container[field] = self.optional_fields_dict[field].get_val()

    def set_val(self, field, value):
        """field - name of field to activate
        value - value provided for field"""
        if field in self.all_fields_to_compare:
            self.select_element(field)
            self.adds_selected()
            self.optional_fields_dict[field].set_val(value)
        return

    def clear_val(self):
        current_row_count = self.selected_values_display_row.rowCount()
        for selected_idx in range(current_row_count):
            selected = self.selected_values_display_row.child(0)
            selected = self.tree_model.indexFromItem(selected)
            self.select_element(selected)
            self.restore_selected()

    def load_main_data(self):
        self.all_fields_to_compare = []
        data_to_load = copy.copy(Glob_Var.optional_fields)
        for group_title in data_to_load:
            display_list = list(data_to_load[group_title].keys())
            self.all_fields_to_compare += display_list
            data_to_load[group_title] = display_list
        self.add_data(data=data_to_load)

    def adds_selected(self):
        """just adds selected value from available to SELECTED VALUES then remove selected value"""
        selected_value = self.selected_element()
        if selected_value:
            # if selected multiple elements. just in case, select only 1. In case of optional, should always be one
            if isinstance(selected_value, list):
                selected_value = selected_value[0]
            # here can only works with lowest level items.
            if selected_value.parent():
                # is if not "selected values" then it one of the others, add them to selected values
                # delete original but remember its data to restore later
                if selected_value.parent().text() != 'SELECTED VALUES':
                    delete_element_data = {'index': selected_value.row(), 'parent': selected_value.parent()}
                    self.selected_values[selected_value.text()] = delete_element_data
                    new_selected = QStandardItem(selected_value.text())
                    new_selected.setEditable(False)
                    new_selected2 = QStandardItem('')
                    self.selected_values_display_row.appendRow([new_selected, new_selected2])
                    self.create_field(selected_value)
                    self.delete_leaf()

    def restore_selected(self):
        selected_value = self.selected_element()
        if selected_value:
            if isinstance(selected_value, list):
                selected_value = selected_value[0]
            if selected_value.parent():
                if selected_value.parent().text() == 'SELECTED VALUES':
                    # self.optional_fields_dict.pop(selected_value.text)
                    self.optional_fields_dict[selected_value.text()].destroy()
                    val_to_restore = selected_value.text()
                    self.delete_leaf()
                    restore = QStandardItem(val_to_restore)
                    self.selected_values[val_to_restore]['parent'].insertRow(
                        self.selected_values[val_to_restore]['index'], restore)
                    del self.optional_fields_dict[val_to_restore]

    def create_field(self, selected_item):
        """normally fields are created one after the other. optional fields can be created after everything is done
        so align widgets, i added strecher at the end of last field, which cannot be removed. so to add new fields
        it needs to insert them. But create field does not have insert, so instead i created new method here for that"""
        parent = selected_item.parent()
        field = createField(self.main_widget, selected_item.text(), Glob_Var.optional_fields[parent.text()][selected_item.text()])
        self.optional_fields_dict[selected_item.text()] = field
        field.set_up_widget(self.optional_field_frame, True)


class PerkDoubleList(SimpleFields.ElementsList):
    def __init__(self, master=None, fields_data=None):
        super().__init__(master, '', folders=True)
        """this is very similar to fetishapply, but does not use main game items. it could,
         but I want to keep it separated.
         problem is, fetishApply is only 1 field, while this comes in 2 separate fields. first is names, second is vals.
         set_val will have to first add column with names, then add column with values
         
         Too many values for perktypes to put in single list. Well make complex treeview.
         Add first row - "SELECTED VALUES", and after that all perktypes.
         double click on perktype - its hidden and added to selectd values.
         edit colmn with value in selected values.

         getval - get val from SELECTED VALUES
         setval - set vals in SELECTED VALUES
         only problem - perkIcon - its a file. so double click in tree - add to selected values. double click in
         selected values - open load file.

        also, block edit and delete for other places besides selected values
        """
        self.files_container = []
        self.flag_folders = False
        self.load_type = ''
        self.title = 'PerksDoubleField'
        self.fields_set = fields_data['fields']
        self.path_cut = '../../'
        self.setHeaderHidden(False)
        header_labels = []
        for field in self.fields_set:
            header_labels.append(field['name'])
            # print(str(self.fields_set.index(field)))
            # self.final_data_tree.tree_model.setHorizontalHeaderItem(self.fields_set.index(field), QStandardItem(field['name']))
        self.tree_model.setHorizontalHeaderLabels(header_labels)
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 3)
        self.setMaximumHeight(100)
        # self.area_explanation = AreaEntry(master)
        # self.area_explanation.label.grid_forget()
        # self.area_explanation.grid(row=5, column=0, columnspan=3)
        # self.options_tree.treeview.bind("<<TreeviewSelect>>", self.display_info)
        # self.custom_layout.addWidget(self.final_data_tree)
        self.row_size = 6

        if 'Perk' in self.fields_set[0]['name']:
            self.load_type = 'PerkType'
            self.load_data = 'EffectPower'
        elif 'Stat' in self.fields_set[0]['name']:
            self.load_type = 'StatReq'
            self.load_data = 'StatReqAmount'
        else:
            print('Unknown data to load. - Adding new row in perk double list class')
            return
        """"""
        if self.load_type == 'PerkType':
            self.area_explanation = SimpleFields.AreaEntry(self, edit=False)
            self.area_explanation.change_size(200, 100)
            self.area_explanation.set_up_widget(self.layout)
            self.clicked.connect(self.display_explanations)
        self.selected_values_display_row = QStandardItem('SELECTED VALUES')
        self.selected_values_display_row.setEditable(False)
        self.tree_model.appendRow(self.selected_values_display_row)
        self.doubleClicked.connect(self.select_data)
        self.selected_values = {}
        self.loaded_data = False
        self.load_main_data()

    def display_explanations(self):
        """clicking on any element in treeview, if its lowest level, check if there is explanation, is yes, display"""
        selected_element = self.selected_element()
        if not isinstance(selected_element, list):
            if not selected_element.hasChildren():
                parent = selected_element.parent().text()
                explanation = Glob_Var.perks_and_stats[self.load_type][parent][selected_element.text()]['tooltip']
                self.area_explanation.set_val(explanation)
        return

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.restore_selected()

    def set_val(self, names, values):
        """this is used when loading new element. Problem is that it is 2 fields in file. So when it load data
         it takes data from both fields and passes here. For that reason, there is separate loading for skill template
         which takes data from 2 fields and loads here"""
        for name, val in zip(names, values):
            if name == 'StatusIcon':
                temp = val.split('/')
                self.files_container = [temp[-1], val]
                self.add_leaf([name, temp[-1]], parent=self.selected_values_display_row)
            elif name == '':
                continue
            else:
                self.add_leaf([name, val], parent=self.selected_values_display_row)

    def get_val(self, temp_dict_container=None):
        """it needs to get data from treeview and return it in 2 separate fields"""
        final_data = self.get_data()
        final_data = final_data[0]
        load_type = []
        load_data = []
        if isinstance(final_data, dict):
            for selected_values in final_data:
                for rows in final_data[selected_values]:
                    load_type.append(rows[0])
                    if rows[0] == 'StatusIcon':
                        load_data.append(self.files_container[1])
                    else:
                        load_data.append(rows[1])
        if temp_dict_container is not None:
            temp_dict_container[self.load_type] = load_type
            temp_dict_container[self.load_data] = load_data
        else:
            return load_type, load_data

    def clear_val(self):
        current_row_count = self.selected_values_display_row.rowCount()
        self.selected_values_display_row.removeRows(0, current_row_count)

    def load_main_data(self):
        data_to_load = copy.copy(Glob_Var.perks_and_stats[self.load_type])
        for group_title in data_to_load:
            display_list = list(data_to_load[group_title].keys())
            data_to_load[group_title] = display_list
        self.add_data(data=data_to_load)

    def select_data(self):
        """just adds selected value from perk types to SELECTED VALUES then remove selected value and nothing else"""
        selected_value = self.selected_element()
        if selected_value:
            # if selected multiple elements. just in case, select only 1
            if isinstance(selected_value, list):
                selected_value = selected_value[0]
            # here can only works with lowest level items.
            if selected_value.parent():
                # is if not "selected values" then it one of the others, add them to selected values
                # delete original but remember its data to restore later
                if selected_value.parent().text() != 'SELECTED VALUES':
                    delete_element_data = {'index': selected_value.row(), 'parent': selected_value.parent()}
                    self.selected_values[selected_value.text()] = delete_element_data
                    new_selected = QStandardItem(selected_value.text())
                    new_selected.setEditable(False)
                    new_selected2 = QStandardItem('')
                    self.delete_leaf()
                    self.selected_values_display_row.appendRow([new_selected,new_selected2])
                else:
                    """if clicked on element in SELECTED VALUES then if its icon it should open file load"""
                    if 'Icon' in selected_value.text():
                        icon = QtWidgets.QFileDialog.getOpenFileName(caption="Select file", filter="Images (*.png *.xpm *.jpg)")
                        if icon:
                            """selected value is actually first element in row, so need
                             to get its sibling in next column"""
                            icon_row = self.tree_model.indexFromItem(selected_value)
                            icon_place = self.tree_model.itemFromIndex(icon_row.siblingAtColumn(1))

                            temp = icon[0].split('/')
                            filename = temp[-1]
                            file_path_start = icon[0].find('Mods/')
                            file_path = self.path_cut + icon[0][file_path_start:]
                            self.files_container = [filename, file_path]
                            icon_place.setText(filename)

    def restore_selected(self):
        selected_value = self.selected_element()
        if selected_value:
            if isinstance(selected_value, list):
                selected_value = selected_value[0]
            if selected_value.parent():
                if selected_value.parent().text() == 'SELECTED VALUES':
                    val_to_restore = selected_value.text()
                    self.delete_leaf()
                    restore = QStandardItem(val_to_restore)
                    self.selected_values[val_to_restore]['parent'].insertRow(self.selected_values[val_to_restore]['index'], restore)

    # # todo
    # def add_other_fields(self, field):
    #     self.other_fields.append(field)

    # def set_up_widget(self, outside_layout):
    #     outside_layout.addWidget(self)


class Pictures:
    def __init__(self, field_name, field_data):
        """first a button to open picture viewer"""
        self.custom_layout = QtWidgets.QVBoxLayout()
        button_open_viewer = SimpleFields.CustomButton(None, 'Pictures')
        self.label_custom = button_open_viewer
        self.label_custom.clicked.connect(self.show_viewer)
        self.custom_layout.addWidget(self.label_custom)
        """and element tree to display pictures for quick look"""
        self.final_data = SimpleFields.ElementsList(None)
        self.final_data.set_up_widget(self.custom_layout)

        self.row_size = 5

    def set_up_widget(self, outside_layout):
        outside_layout.addLayout(self.custom_layout)

    def set_val(self, data=[], node=None, insert_row=False, data_info=''):
        """experimental - for values in dictionaries it should add in 2 columns instead of one.
        will also need to change how to get values then"""
        # top level,  gather data into list. this way, if need to insert, just provide row number
        final_items_to_add = []
        if not node:
            node = self.final_data.tree_model
        else:
            if isinstance(node, str):
                node = self.final_data.find_node(node)
                node = self.final_data.tree_model.itemFromIndex(node)
        if isinstance(data, list):
            for values in data:
                if isinstance(values, dict):
                    for key in values:
                        parent_row = QStandardItem()
                        final_items_to_add.append(parent_row)
                        parent_row.setText(key)
                        self.set_val(parent_row, values[key])
                else:
                    bottom_row = QStandardItem()
                    bottom_row.setText(values)
                    final_items_to_add.append(bottom_row)
                    # if not self.flag_child_editable:
                    #     bottom_row.setEditable(False)
        elif isinstance(data, dict):
            for key in data:
                parent_row = QStandardItem()
                parent_row.setText(key)
                final_items_to_add.append(parent_row)
                parent_row.setEditable(False)
                self.set_val(parent_row, data[key])
        else:
            """if data is just string"""
            bottom_row = QStandardItem()
            bottom_row.setText(data)
            if data_info:
                bottom_row.setWhatsThis(data_info)
            # if not self.flag_child_editable:
            bottom_row.setEditable(False)
            final_items_to_add.append(bottom_row)

        for items in (final_items_to_add):
            node.appendRow(items)
        # current_row_count = self.final_data.tree_model.rowCount()
        # for idx in range(current_row_count):
        #     item = self.final_data.tree_model.item(idx)
        #     if item.hasChildren():
        #         for idx in range(item.rowCount()):
        #             self.final_data.expand(self.final_data.tree_model.indexFromItem(item.child(idx)))
        return
    def get_val(self):
        return
    def clear_val(self):
        self.final_data.clear_val()

    def show_viewer(self):
        self.image_viewer = QImageViewer()
        self.image_viewer.show()


def createField(parent_widget, fieldname, fieldData, template_name=None):
    #   master_layout - layout where it should go,
    # fieldname - what should be displayd in label and also in field title, for inside recognition
    # fielddata - data from file about field attributed
    tempfield = ''
    if fieldData["type"] in "text int singlelist filePath":
        if fieldData["type"] == "text":
            tempfield = SimpleFields.SimpleEntry(master_widget=parent_widget, field_name=fieldname,
                                                 field_data=fieldData, main_data_treeview=Glob_Var.main_game_field)
        elif fieldData["type"] == "int":
            tempfield = SimpleFields.NumericEntry(master=parent_widget, wid=4, field_name=fieldname,
                                                  field_data=fieldData)
        elif fieldData["type"] == "singlelist":
            tempfield = SimpleFields.SingleList(parent_widget, fieldname, fieldData)
        elif fieldData["type"] == "filePath":
            tempfield = SimpleFields.FileField(parent_widget, fieldname, field_data=fieldData)
    elif fieldData["type"] in 'multilist area requirement combattext':
        if fieldData["type"] == 'area':
            # TODO
            # if 'options' in fieldData:
            #     if 'function' in fieldData["options"]:
            #         temp = Text_With_Function(masterName, fieldname, tooltip, 'U', 'F')
            #         field_area = temp.area_text
            #         field_area.bind("<Tab>", otherFunctions.focus_next_window)
            #     else:
            #         field_area = SimpleFields.AreaEntry(masterName, fieldname, tooltip, 'U')
            #         field_area.bind("<Tab>", otherFunctions.focus_next_window)
            # else:
            tempfield = SimpleFields.AreaEntry(parent_widget, fieldname)
            # field_area.bind("<Tab>", otherFunctions.focus_next_window)
        elif fieldData["type"] == 'multilist':
            tempfield = SimpleFields.MultiListDisplay(parent_widget, fieldname, fieldData, main_data_treeview=Glob_Var.main_game_field)
        elif fieldData["type"] in 'combattext':
            tempfield = CombatTrigger(parent_widget, fieldname, fieldData['fields'])
    else:
        if fieldData["type"] == 'dictionary':
            tempfield = ExpandDictionaryField(parent_widget, fieldname, fields_data=fieldData)
        elif fieldData["type"] == 'combatDialogue':
            tempfield = EDF_forcombatDialogue(parent_widget, fieldname, fields_data=fieldData)
        elif fieldData["type"] in 'listDict':
            # tempfield = ListDict(masterName, fieldname, fields_data=fieldData)
            tempfield = ExpandDictionaryField(parent_widget, fieldname, fields_data=fieldData)
        elif fieldData["type"] in 'deck':
            tempfield = DeckField(parent_widget, fieldData)
        elif fieldData["type"] in 'monstergroups':
            tempfield = MonsterGroups(parent_widget, fieldname)
        # elif fieldData["type"] in 'speaker':
        #     tempfield = Speaker(parent_widget, fieldData)
        elif fieldData["type"] in 'FetishApply':
            tempfield = FetishApply(parent_widget, fieldname, fieldData)
        elif fieldData["type"] in 'Pictures':
            tempfield = Pictures(fieldname, fieldData)
        elif fieldData["type"] in 'PairFields':
            tempfield = PerkDoubleList(parent_widget, fieldData)
        elif fieldData['type'] in 'functionfield':
            tempfield = Functional_Dummy(None, fieldname)
    return tempfield

def createField_workingBackup(parent_widget, fieldname, fieldData, mode=1, template_name=None):
    #   master_layout - layout where it should go,
    # fieldname - what should be displayd in label and also in field title, for inside recognition
    # fielddata - data from file about field attributed
    field_ready = None
    tempfield = ''
    if mode:
        # if fieldData["type"] in "text singlelist scenesinglelist  filePath":
        if fieldData["type"] in "text int singlelist filePath":
            if fieldData["type"] == "text":
                tempfield = SimpleFields.SimpleEntry(master_widget=parent_widget, field_name=fieldname,
                                                     field_data=fieldData, main_data_treeview=Glob_Var.main_game_field)
                # tempfield.grid(row=rowposition, column=colposition + 1)
                # field_ready = tempfield
            elif fieldData["type"] == "int":
                tempfield = SimpleFields.NumericEntry(master=parent_widget, wid=4, field_name=fieldname,
                                                      field_data=fieldData)
                # tempfield.bind("<Tab>", otherFunctions.focus_next_window)
                # field_ready = tempfield
                # tempfield.grid(row=rowposition, column=colposition+1)
            elif fieldData["type"] == "singlelist":
                tempfield = SimpleFields.SingleList(parent_widget, fieldname, fieldData)
            elif fieldData["type"] == "filePath":
                tempfield = SimpleFields.FileField(parent_widget, fieldname, field_data=fieldData)
            elif fieldData['type'] == 'scenesinglelist':
                field_optionbox = SceneSingleList(masterName, fieldname, tooltip, 'L', fieldData['choices'])
                field_optionbox.configure(takefocus=1)
                tempfield = field_optionbox
            # tempfield.pack(fill='both')
        elif fieldData["type"] in 'multilist area requirement combattext':
            if fieldData["type"] == 'area':
                # if 'options' in fieldData:
                #     if 'function' in fieldData["options"]:
                #         temp = Text_With_Function(masterName, fieldname, tooltip, 'U', 'F')
                #         field_area = temp.area_text
                #         field_area.bind("<Tab>", otherFunctions.focus_next_window)
                #     else:
                #         field_area = SimpleFields.AreaEntry(masterName, fieldname, tooltip, 'U')
                #         field_area.bind("<Tab>", otherFunctions.focus_next_window)
                # else:
                tempfield = SimpleFields.AreaEntry(parent_widget, fieldname)
                # field_area.bind("<Tab>", otherFunctions.focus_next_window)
            elif fieldData["type"] == 'multilist':
                tempfield = SimpleFields.MultiListDisplay(parent_widget, fieldname, fieldData, main_data_treeview=Glob_Var.main_game_field)
            # elif fieldData["type"] == 'requirement':
            #     tempfield = Requires(masterName, fieldname)
            elif fieldData["type"] in 'combattext':
                tempfield = CombatTrigger(parent_widget, fieldname, fieldData['fields'])
            # tempfield.pack()
        else:
            # frame_advancedFields = tk.Frame(master=masterName, bg='blue')
            # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
            if fieldData["type"] == 'dictionary':
                tempfield = ExpandDictionaryField(parent_widget, fieldname, fields_data=fieldData)
            elif fieldData["type"] == 'combatDialogue':
                tempfield = EDF_forcombatDialogue(parent_widget, fieldname, fields_data=fieldData)
        #     # elif fieldData["type"] in 'functionfield':
        #     #     # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
        #     #     # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
        #     #     # self.frame_fields['Items'][field] = {}
        #     #     # label_field = tk.Label(master=frame_advancedFields, text=field)
        #     #     # label_field.grid(row=rowsC, column=0, columnspan=2)
        #     #     # rowsC += 1
        #     #     functionflag = ''
            elif fieldData["type"] in 'listDict':
                # tempfield = ListDict(masterName, fieldname, fields_data=fieldData)
                tempfield = ExpandDictionaryField(parent_widget, fieldname, fields_data=fieldData)
            elif fieldData["type"] in 'deck':
                tempfield = DeckField(parent_widget, fieldData)
            elif fieldData["type"] in 'monstergroups':
                tempfield = MonsterGroups(parent_widget, fieldname)
            # elif fieldData["type"] in 'speaker':
            #     tempfield = Speaker(parent_widget, fieldData)
            elif fieldData["type"] in 'FetishApply':
                tempfield = FetishApply(parent_widget, fieldname, fieldData)
            elif fieldData["type"] in 'Pictures':
                tempfield = Pictures(fieldname, fieldData)
            elif fieldData["type"] in 'PairFields':
                advance_field = PerkDoubleList(parent_widget, fieldData)
                tempfield = advance_field
                # for field in fieldData['fields'][1:]:
                #     connected_field = RestOfPerks(field)
                #     # field_ready['name'] = connected_field
                #     advance_field.add_other_fields(connected_field)
                # return [advance_field, connected_field]

            elif fieldData['type'] in 'functionfield':
                tempfield = Functional_Dummy(None, fieldname)
    # else:
    #     """here create fields only for display."""
    #     if fieldData["type"] in "text singlelist scenesinglelist int filePath":
    #         # controlVar = tk.StringVar()
    #         if fieldData["type"] == "text":
    #             tempfield = SimpleFields.SimpleEntryDisplay(master=masterName, field_name=fieldname, label_position='L'
    #                                                  , tooltip_text=tooltip, field_data=fieldData, template_name=template_name)
    #         elif fieldData["type"] == "int":
    #             tempfield = SimpleFields.NumericEntryDisplay(master=masterName, wid=4, field_name=fieldname, label_position='L'
    #                                                   , tooltip_text=tooltip, template_name=template_name)
    #             tempfield.bind("<Tab>", otherFunctions.focus_next_window)
    #         elif fieldData["type"] == "singlelist":
    #             field_optionbox = SimpleFields.SingleListDisplay(masterName, fieldname, tooltip, 'L', fieldData,
    #                                                              template_name)
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #         elif fieldData["type"] == "filePath":
    #             tempfield = SimpleFields.FileField(masterName, fieldname, tooltip, 'L', None, 0, template_name)
    #         elif fieldData['type'] == 'scenesinglelist':
    #             field_optionbox = SceneSingleList(masterName, fieldname, tooltip, 'L', fieldData['choices'])
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #     elif fieldData["type"] in 'multilist area requirement combattext':
    #         if fieldData["type"] == 'area':
    #             field_area = SimpleFields.AreaEntryDisplay(masterName, fieldname, tooltip, 'U', fieldData, template_name=template_name)
    #             field_area.bind("<Tab>", otherFunctions.focus_next_window)
    #             tempfield = field_area
    #         elif fieldData["type"] == 'multilist':
    #             multilist_field = SimpleFields.MultiListDisplay(masterName, fieldname, tooltip, 'U',
    #                                                             field_options=fieldData['options'], template_name=template_name)
    #             tempfield = multilist_field
    #         elif fieldData["type"] in 'combattext':
    #             tempfield = CombatTrigger(masterName, fieldname, fieldData['fields'])
    #         # tempfield.pack()
    #     else:
    #         if fieldData["type"] == 'dictionary':
    #             tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #         elif fieldData["type"] == 'combatDialogue':
    #             tempfield = ExpandDictionaryField_withcombat(masterName, fieldname, fields_data=fieldData, mode=0)
    #         elif fieldData["type"] in 'listDict':
    #             tempfield = ListDict(masterName, fieldname, fieldData, mode=0)
    #             # tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #         elif fieldData["type"] in 'deck':
    #             tempfield = DeckFieldDisplay(masterName, fieldData['tooltip'])
    #         elif fieldData["type"] in 'monstergroups':
    #             tempfield = MonsterGroupsDisplay(masterName, view_title=fieldname)
    #         elif fieldData["type"] in 'speaker':
    #             tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #             # tempfield = Speaker(masterName, fieldData)
    #         elif fieldData["type"] in 'FetishApply':
    #             tempfield = FetishApplyDisplay(masterName)
    #         elif fieldData["type"] in 'PairFields':
    #             # print(fieldname)
    #             tempfield = PerkDoubleListDisplay(fieldData, masterName, fieldname)
    #             # advance_field = PerkDoubleList(fieldData, masterName)
    #             # for field in fieldData['fields'][1:]:
    #             #     connected_field = RestOfPerks(field)
    #             #     advance_field.add_other_fields(connected_field)
    #             # return [advance_field, connected_field]
    #         elif fieldData['type'] in 'functionfield':
    #             tempfield = Functional_Dummy(None, fieldname)

    return tempfield

    #   master_layout - layout where it should go,
    # fieldname - what should be displayd in label and also in field title, for inside recognition
    # fielddata - data from file about field attributed
    # field_ready = None
    # if 'tooltip' in fieldData:
    #     tooltip = fieldData['tooltip']
    # else:
    #     tooltip = ''
    # tempfield = ''
    # if mode:
    #     if fieldData["type"] in "text singlelist scenesinglelist int filePath":
    #         # controlVar = tk.StringVar()
    #         if fieldData["type"] == "text":
    #             tempfield = SimpleFields.SimpleEntry(master=masterName, field_name=fieldname, label_position='L'
    #                                                  , tooltip_text=tooltip, field_data=fieldData)
    #             # tempfield.grid(row=rowposition, column=colposition + 1)
    #             # field_ready = tempfield
    #         elif fieldData["type"] == "int":
    #             tempfield = SimpleFields.NumericEntry(master=masterName, wid=4, field_name=fieldname, label_position='L'
    #                                                   , tooltip_text=tooltip, field_data=fieldData)
    #             tempfield.bind("<Tab>", otherFunctions.focus_next_window)
    #             # field_ready = tempfield
    #             # tempfield.grid(row=rowposition, column=colposition+1)
    #         elif fieldData["type"] == "singlelist":
    #             field_optionbox = SimpleFields.SingleList(masterName, fieldname, tooltip, 'L', fieldData['choices'])
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #         elif fieldData["type"] == "filePath":
    #             tempfield = SimpleFields.FileField(masterName, fieldname, tooltip, 'L', field_data=fieldData)
    #         elif fieldData['type'] == 'scenesinglelist':
    #             field_optionbox = SceneSingleList(masterName, fieldname, tooltip, 'L', fieldData['choices'])
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #         # tempfield.pack(fill='both')
    #     elif fieldData["type"] in 'multilist area requirement combattext':
    #         if fieldData["type"] == 'area':
    #             if 'options' in fieldData:
    #                 if 'function' in fieldData["options"]:
    #                     temp = Text_With_Function(masterName, fieldname, tooltip, 'U', 'F')
    #                     field_area = temp.area_text
    #                     field_area.bind("<Tab>", otherFunctions.focus_next_window)
    #                 else:
    #                     field_area = SimpleFields.AreaEntry(masterName, fieldname, tooltip, 'U')
    #                     field_area.bind("<Tab>", otherFunctions.focus_next_window)
    #             else:
    #                 field_area = SimpleFields.AreaEntry(masterName, fieldname, tooltip, 'U')
    #                 field_area.bind("<Tab>", otherFunctions.focus_next_window)
    #         #     field_area.grid(row=rowposition+1, columnspan=2, column=colposition)
    #         #     # field_area.configure(width=20, heigh=4)
    #             tempfield = field_area
    #         elif fieldData["type"] == 'multilist':
    #             multilist_field = SimpleFields.MultiList(masterName, fieldname, tooltip, 'U', fieldData['choices'],
    #                                                      field_options=fieldData['options'])
    #             tempfield = multilist_field
    #         # elif fieldData["type"] == 'requirement':
    #         #     tempfield = Requires(masterName, fieldname)
    #         elif fieldData["type"] in 'combattext':
    #             tempfield = CombatTrigger(masterName, fieldname, fieldData['fields'])
    #         # tempfield.pack()
    #     else:
    #         # frame_advancedFields = tk.Frame(master=masterName, bg='blue')
    #         # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #         if fieldData["type"] == 'dictionary':
    #             tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData)
    #         elif fieldData["type"] == 'combatDialogue':
    #             tempfield = ExpandDictionaryField_withcombat(masterName, fieldname, fields_data=fieldData)
    #     #     # elif fieldData["type"] in 'functionfield':
    #     #     #     # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
    #     #     #     # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #     #     #     # self.frame_fields['Items'][field] = {}
    #     #     #     # label_field = tk.Label(master=frame_advancedFields, text=field)
    #     #     #     # label_field.grid(row=rowsC, column=0, columnspan=2)
    #     #     #     # rowsC += 1
    #     #     #     functionflag = ''
    #         elif fieldData["type"] in 'listDict':
    #             tempfield = ListDict(masterName, fieldname, fields_data=fieldData)
    #             # tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData)
    #         elif fieldData["type"] in 'deck':
    #             tempfield = DeckField(masterName, fields_data=fieldData)
    #         elif fieldData["type"] in 'monstergroups':
    #             tempfield = MonsterGroups(masterName, fieldData['choices'], view_title=fieldname)
    #         elif fieldData["type"] in 'speaker':
    #             tempfield = Speaker(masterName, fieldData)
    #         elif fieldData["type"] in 'FetishApply':
    #             tempfield = FetishApply(masterName, fieldname, fieldData)
    #         elif fieldData["type"] in 'PairFields':
    #             advance_field = PerkDoubleList(fieldData, masterName)
    #             tempfield = advance_field
    #             # for field in fieldData['fields'][1:]:
    #             #     connected_field = RestOfPerks(field)
    #             #     # field_ready['name'] = connected_field
    #             #     advance_field.add_other_fields(connected_field)
    #             # return [advance_field, connected_field]
    #         elif fieldData['type'] in 'functionfield':
    #             tempfield = Functional_Dummy(None, fieldname)
    # else:
    #     """here create fields only for display."""
    #     if fieldData["type"] in "text singlelist scenesinglelist int filePath":
    #         # controlVar = tk.StringVar()
    #         if fieldData["type"] == "text":
    #             tempfield = SimpleFields.SimpleEntryDisplay(master=masterName, field_name=fieldname, label_position='L'
    #                                                  , tooltip_text=tooltip, field_data=fieldData, template_name=template_name)
    #         elif fieldData["type"] == "int":
    #             tempfield = SimpleFields.NumericEntryDisplay(master=masterName, wid=4, field_name=fieldname, label_position='L'
    #                                                   , tooltip_text=tooltip, template_name=template_name)
    #             tempfield.bind("<Tab>", otherFunctions.focus_next_window)
    #         elif fieldData["type"] == "singlelist":
    #             field_optionbox = SimpleFields.SingleListDisplay(masterName, fieldname, tooltip, 'L', fieldData,
    #                                                              template_name)
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #         elif fieldData["type"] == "filePath":
    #             tempfield = SimpleFields.FileField(masterName, fieldname, tooltip, 'L', None, 0, template_name)
    #         elif fieldData['type'] == 'scenesinglelist':
    #             field_optionbox = SceneSingleList(masterName, fieldname, tooltip, 'L', fieldData['choices'])
    #             field_optionbox.configure(takefocus=1)
    #             tempfield = field_optionbox
    #     elif fieldData["type"] in 'multilist area requirement combattext':
    #         if fieldData["type"] == 'area':
    #             field_area = SimpleFields.AreaEntryDisplay(masterName, fieldname, tooltip, 'U', fieldData, template_name=template_name)
    #             field_area.bind("<Tab>", otherFunctions.focus_next_window)
    #             tempfield = field_area
    #         elif fieldData["type"] == 'multilist':
    #             multilist_field = SimpleFields.MultiListDisplay(masterName, fieldname, tooltip, 'U',
    #                                                             field_options=fieldData['options'], template_name=template_name)
    #             tempfield = multilist_field
    #         elif fieldData["type"] in 'combattext':
    #             tempfield = CombatTrigger(masterName, fieldname, fieldData['fields'])
    #         # tempfield.pack()
    #     else:
    #         if fieldData["type"] == 'dictionary':
    #             tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #         elif fieldData["type"] == 'combatDialogue':
    #             tempfield = ExpandDictionaryField_withcombat(masterName, fieldname, fields_data=fieldData, mode=0)
    #         elif fieldData["type"] in 'listDict':
    #             tempfield = ListDict(masterName, fieldname, fieldData, mode=0)
    #             # tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #         elif fieldData["type"] in 'deck':
    #             tempfield = DeckFieldDisplay(masterName, fieldData['tooltip'])
    #         elif fieldData["type"] in 'monstergroups':
    #             tempfield = MonsterGroupsDisplay(masterName, view_title=fieldname)
    #         elif fieldData["type"] in 'speaker':
    #             tempfield = ExpandDictionaryField(masterName, fieldname, fields_data=fieldData, templateName=template_name, mode=0)
    #             # tempfield = Speaker(masterName, fieldData)
    #         elif fieldData["type"] in 'FetishApply':
    #             tempfield = FetishApplyDisplay(masterName)
    #         elif fieldData["type"] in 'PairFields':
    #             # print(fieldname)
    #             tempfield = PerkDoubleListDisplay(fieldData, masterName, fieldname)
    #             # advance_field = PerkDoubleList(fieldData, masterName)
    #             # for field in fieldData['fields'][1:]:
    #             #     connected_field = RestOfPerks(field)
    #             #     advance_field.add_other_fields(connected_field)
    #             # return [advance_field, connected_field]
    #         elif fieldData['type'] in 'functionfield':
    #             tempfield = Functional_Dummy(None, fieldname)
    #
    #     # try:
    #     #     if tempfield:
    #     #         tempfield.pack(side=tk.LEFT, fill=tk.BOTH)
    #     # except:
    #     #     print('something wrong with ' + fieldname)
    # field_ready = tempfield
    # return field_ready
