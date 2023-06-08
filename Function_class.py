import tkinter as tk
from datetime import datetime
# from tkinter import colorchooser
# from tkinter.ttk import *
# from Elements_list import Elements_List
# from functools import partial
# import GUIFieldClasses
import otherFunctions
# from tkinter import messagebox
# from tkinter.ttk import Treeview
import GlobalVariables
import SimpleFields
import copy
# class ExpandedList(GUIFieldClasses.Elements_List):
#
# def JustName(master, function_name, field_data=''):
#     """this add field with function name only"""
#     rowp=0
#     colp=0
#     templist = []
#     entry_name = SceneSimpleEntry(master, function_name)
#     entry_name.set_val(function_name)
#     entry_name.grid(row=rowp, column=colp)
#     colp += 1
#     templist.append(entry_name)
#     return templist
#
#     # return 'done'
# def AddInput(master, function_name, field_data):
#     """function and text field"""
#     rowp=0
#     colp=0
#     templist = []
#     entry_name = SceneSimpleEntry(master, function_name)
#     entry_name.set_val(function_name)
#     entry_name.grid(row=rowp, column=colp)
#     colp += 1
#     templist.append(entry_name)
#     value_field = SceneSimpleEntry(master, field_data['name'])
#     value_field.grid(row=rowp, column=colp)
#     templist.append(value_field)
#     return templist
#
#     # return 'done'
#
# def ChangeMainStat(master, function_name, field_data):
#     """function and number"""
#     rowp=0
#     colp=0
#     templist = []
#     entry_name = SceneSimpleEntry(master, field_data['name'], state='disabled')
#     entry_name.set_val(field_data['name'])
#     entry_name.grid(row=rowp, column=colp)
#     colp += 1
#     templist.append(entry_name)
#     value_field = SceneNumericEntry(master, field_data['name'])
#     value_field.grid(row=rowp, column=colp)
#     templist.append(value_field)
#     return templist
#
#     # return 'done'
#
# def ChangeMainOption(master, function_name, field_data):
#     """function, list with basic attributes and number to change it"""
#     rowp=0
#     colp=0
#     templist = []
#     entry_name = SceneSimpleEntry(master, field_data['name'], state='disabled')
#     entry_name.set_val(field_data['name'])
#     entry_name.grid(row=rowp, column=colp, ipadx=len(field_data['name']))
#     colp += 1
#     templist.append(entry_name)
#     options = SceneSingleList(master, field_data['options'])
#     options.grid(row=rowp, column=colp)
#     colp += 1
#     templist.append(options)
#     value_field = SceneNumericEntry(master)
#     value_field.grid(row=rowp, column=colp)
#     colp += 1
#     templist.append(value_field)
#     return templist
#     # return 'test2'
#TODO function swap line if - fetish with int and choices
from PyQt5 import QtCore, QtGui, QtWidgets

# class SceneNewWindow(tk.Toplevel):
#     def __init__(self, master=None):
#         super().__init__(master=master)
#
# """should be obsolete"""
# class SceneSceneNewWindow(tk.Toplevel):
#     def __init__(self, master=None):
#         super().__init__(master=master)
#
# """seems not used"""
# class SceneNumericEntry(SimpleFields.NumericEntry):
#     def __init__(self, master=None, width=0):
#         super().__init__(master=master, wid=width, field_name='temp', label_position='U', tooltip_text=None,
#                          field_data=None)
#         # self.hidden_flag = True
#
#     def hide_field(self):
#         self.pack_forget()
#         # self.hidden_flag = True
#
#     def show_field(self):
#         self.pack(side=tk.LEFT)
#         # self.hidden_flag = False
# # class SceneNumericEntry(tk.Entry):
# #     def __init__(self, master=None, field_name='', tooltip_text='', wid=0, **kwargs):
# #         self.title = field_name
# #         self.field_frame = master
# #         self.var = tk.StringVar()
# #         self.type = 'text'
# #         self.hidden_flag = True
# #         self.var.trace('w', self.limit_size_day)
# #         if wid==0:
# #             wid=3
# #
# #         tk.Entry.__init__(self, master, textvariable=self.var, width=wid, **kwargs)
# #         self.old_value = '0'
# #         # self.var.trace('w', self.check)
# #         self.bind('<Key>', self.check_for_digit)
# #         self.grid(row=1, column=0)
# #         self.label = tk.Label(master=master, text=field_name)
# #         self.label.grid(row=0, column=0)
# #         if tooltip_text:
# #             SceneCreateToolTip(self.label, tooltip_text)
# #         # self.label.grid(row=0, column=0, sticky='W')
# #         # self.grid(row=0, column=1, sticky='E')
# #         self.get, self.set = self.var.get, self.var.set
# #
# #     def check(self, *args):
# #         if self.get().isdigit():
# #             # the current value is only digits; allow this
# #             self.old_value = self.get()
# #         else:
# #             # there's non-digit characters in the input; reject this
# #             self.set(self.old_value)
# #
# #     def limit_size_day(self, *args):
# #         value = self.var.get()
# #         if len(value) > 3:
# #             self.var.set(value[:3])
# #
# #     def get_val(self):
# #         if self.var.get() == '':
# #             return 0
# #         else:
# #             return self.var.get()
# #
# #     def set_val(self, value):
# #         self.var.set(value)
# #
# #     def clear_val(self):
# #         self.set(0)
# #
# #     def check_for_digit(self, event):
# #         v = event.char
# #         try:
# #             v = int(v)
# #         except ValueError:
# #             if v != "\x08" and v != "":
# #                 return "break"
# #
# #     def hide_field(self):
# #         self.field_frame.pack_forget()
# #         self.hidden_flag = True
# #
# #     def show_field(self):
# #         self.field_frame.pack(side=tk.LEFT)
# #         self.hidden_flag = False
# #
# #     def update_label(self, new_text):
# #         self.label['text'] = new_text
#
# # TODO change this treeview. need to change  way id is created, so later I can recognize if its function or not.
# class SceneElementsList:
#     def __init__(self, masterWun, rowPos, colPos, listTitle, colspan=1, search_field=False, treeview_height=5, delete_flag=True):
#         self.row_placement = rowPos + 2
#         self.col_placement = colPos
#         self.col_span = colspan
#         if listTitle:
#             self.title = listTitle
#         self.search_frame = tk.Frame(masterWun)
#         if search_field:
#             self.label_search = tk.Label(self.search_frame, text="Search")
#             self.search_var = tk.StringVar()
#             self.search_var.trace_add("write", self.searchval)
#             self.entry_search = tk.Entry(self.search_frame, textvariable=self.search_var)
#             self.label_search.grid(row=0, column=0)
#             self.entry_search.grid(row=1, column=0)
#         self.row_placement = rowPos
#         self.col_placement = colPos
#         self.search_frame.grid(row=self.row_placement, column=self.col_placement)
#         self.treeview = Treeview(masterWun)  # tworzenie kontrolki Treeview
#         self.treeview.bind("<<TreeviewSelect>>",
#                            self.on_tv_select)  # podpinam zdarzenie, wywoływane, gdy kliknięto jakiś element drzewa
#
#         # reszta to nudne i przyziemne podpinanie kontrolki scrollbar oraz pozycjonowanie scrollbara i kontrolki treeview
#         self.sb_treeview = tk.Scrollbar(masterWun)
#         self.sb_treeview.grid(row=self.row_placement+1, column=self.col_placement + colspan, sticky=tk.NS + tk.E)
#         self.treeview.config(yscrollcommand=self.sb_treeview.set, height=treeview_height)
#         self.treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NSEW, columnspan=colspan)
#         self.treeview.bind('<Escape>', lambda event: self.deselect_row())
#         if delete_flag:
#             # self.treeview.bind("<Delete>", lambda event: self.delete_leaf())
#             self.treeview.bind("<Delete>", lambda event: self.delete_with_backup())
#             self.treeview.bind("<Control_L>" + "<z>", lambda event: self.restore_deleted())
#         self.treeview.bind('<Prior>', self.move_up)
#         self.treeview.bind('<Next>', self.move_down)
#         self.sb_treeview.config(command=self.treeview.yview)
#         self.treeview.heading("#0", text=listTitle)
#         self.hidden_leafs = []
#         self.back_up_deleted = []
#
#         # self.sb_treeview.grid(in_=self.treeview, row=1, column=1)
#         # self.terminal_scrollbar = tk.Scrollbar(self)
#         # self.terminal_scrollbar.grid(row=2, column=5, sticky=tk.NS)
#         # self.sb_treeview.place(in_=self.treeview, relx=1., y=0, relheight=1.)
#         # self.treeview.place(x=0, y=0, relwidth=1., relheight=1., width=-18)
#         # self.treeview.pack(expand=True, fill='y')
#         # rowspan = self.row_spaning
#
# #     self.treeview_optionstochoose.treeview.item(selection)['tags']:
# #     self.treeview_optionstochoose.treeview.item(selection, tags=())
# # self.treeview_optionstochoose.treeview.item(selection, tags='selected')
#
#     def add_branch(self, name, values=[], update_flag=True, position='end', tagging=''):
#         current_selected_element_id = self.selected_item(value='code')
#         next_item_in_deck = None
#         # print(current_selected_element)
#         # if current_selected_element_id:
#         #     position = self.treeview.index(current_selected_element_id) + 1
#         #     # next_item_in_deck = self.treeview.next(current_selected_element_id)
#         # else:
#         #     position = 'end'
#             # temp = self.treeview.get_children('')
#             # if len(temp) > 0:
#             #     next_item_in_deck = temp[-1]
#             # else:
#             #     next_item_in_deck = ''
#         # print(next_item_in_deck)
#         # self.add_branch(name, position=tree_insert, update_flag=False)
#         """temporary solution. for scenes, text is often too longs and later are problems with finding, probably
#          findIID def, so instead make ids of time date and no"""
#         # now = datetime.now()
#         if update_flag:
#             if self.treeview.exists(name):
#                 self.add_leaves(name, values, update_flag)
#             else:
#                 value = self.treeview.insert("", position, name, text=name)  # dodanie nowego drzewa (korzenia głównego)
#                 index = 0
#                 for i in values:
#                     try:
#                         self.treeview.insert(value, 'end', i + '_' + value + '_' + str(index),
#                                              text=i)  # dodawanie kolejnych gałęzi drzewa
#                     except:
#                         print('value - ' + str(value))
#                         print('index - ' + str(index))
#                         print('I - ' + str(i))
#                     index += 1
#         else:
#             roots_no = self.treeview.get_children()
#             value = self.treeview.insert("", position, name + '_' + str(len(roots_no)),
#                                          text=name)  # dodanie nowego drzewa (korzenia głównego)
#             """tagging values to distinquish function from normal tests"""
#             if tagging:
#                 self.treeview.item(value, tags=tagging)
#             index = 0
#             for i in values:
#                 leaf = self.treeview.insert(value, 'end', i + '_' + value + '_' + str(index),
#                                             text=i)  # dodawanie kolejnych gałęzi drzewa
#                 if tagging == 'function':
#                     self.treeview.item(i + '_' + value + '_' + str(index), tags='attribute')
#                 index += 1
#
#     def add_leaves(self, iid, values, update_flag=True):  # dodawanie podgałęzi do istniejącej gałęzi drzewa
#         """ need to find proper parent iid as root branches are normal,
#             but leaves are generated with index and parent name,
#             might cause problems when some leaves are similar"""
#         iid = self.find_iid(iid)
#         currentleaves = self.treeview.get_children(iid)
#         if update_flag:
#             for i in currentleaves:  # first clean all leaves
#                 self.treeview.delete(i)
#             for i in values:
#                 # if i not in currentleaves:
#                 #     self.treeview.insert(iid, 'end', i, text=i)  # dodawanie podgałęzi drzewa
#                 # else:   #update branch
#                 self.treeview.insert(iid, 'end', i, text=i)  # dodawanie podgałęzi drzewa
#         else:
#             index = len(currentleaves) + 1
#             # final_iid = self.find_iid(iid)
#             for i in values:
#                 if i not in currentleaves:
#                     self.treeview.insert(iid, 'end', i + '_' + iid + '_' + str(index),
#                                          text=i)  # dodawanie podgałęzi drzewa
#                     index += 1
#
#     def on_tv_select(self, event):  # metoda podpięta pod zdarzenie wywoływane po kliknięciu jakiegoś elementu na liście
#         curItem = self.treeview.focus()  # element, który otrzymał fokus
#         curItem = self.treeview.item(curItem)["text"]
#
#     def hide_tree(self):
#         self.treeview.grid_forget()
#         self.sb_treeview.grid_forget()
#         self.search_frame.grid_forget()
#
#     def show_tree(self):
#         self.treeview.grid(row=self.row_placement+1, column=self.col_placement, sticky=tk.NSEW, columnspan=self.col_span)
#         self.sb_treeview.grid(row=self.row_placement+1, column=self.col_placement + self.col_span, sticky=tk.NS + tk.E)
#         self.search_frame.grid(row=self.row_placement, column=self.col_placement)
#
#     def delete_leaf(self, branch=''):
#         try:
#             if branch == '':
#                 # selected_item = self.treeview.selection()[0]  ## get selected item
#                 selected_item = self.treeview.selection()  ## get selected item
#                 for items in selected_item:
#                     self.treeview.delete(items)
#             else:
#                 self.treeview.delete(branch)
#         except:
#             print("nothing left to delete")
#
#     def change_title(self, new_title):
#         self.treeview.heading("#0", text=new_title)
#
#     def filter_leafs(self, item, branch):
#         # it might works, returning from reversed hidden leafs. this way we put them back in order they were taken away
#         # if not work, will have to change to one list as main, filter it and copy to display
#         # for hiddenleafs in reversed(self.hidden_leafs):
#         #     checkid = hiddenleafs['itemID']
#         #     if item.lower() in checkid[:checkid.find('_')].lower():
#         #         self.treeview.reattach(checkid, hiddenleafs['itemParent'], hiddenleafs['itemNumber'])
#         # branches = self.treeview.get_children()
#         # for branch in branches:
#         #     leafs = list(self.treeview.get_children(branch))
#         #     for leaf in leafs:
#         #         if item.lower() not in leaf[:leaf.find('_')].lower():
#         #             item_parent = self.treeview.parent(leaf)
#         #             item_no = self.treeview.index(leaf)
#         #             self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': leaf})
#         #             self.treeview.detach(leaf)
#         # remade for lvl 3
#         for leaves in branch:
#             leafs = list(self.treeview.get_children(leaves))
#             if leafs:
#                 self.filter_leafs(item, self.treeview.get_children(leaves))
#                 if not self.treeview.get_children(leaves):
#                     # if no more leaves in this branch, hide branch too. we can only interact with leaves.
#                     # print('koniec lisci na = ' + leaves)
#                     item_parent = self.treeview.parent(leaves)
#                     item_no = self.treeview.index(leaves)
#                     self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': leaves})
#                     self.treeview.detach(leaves)
#             # for branch in branches:
#             #     leafs = list(self.treeview.get_children(branch))
#             #
#             #     for leaf in leafs:
#             #
#             #         lvl_2_leaf = self.treeview.get_children(leaf)
#             #         if lvl_2_leaf:
#             #             print(leaf)
#             #     if "_" not in leaves:
#             #         continue
#             else:
#                 if item.lower() not in self.treeview.item(leaves)['text'].lower():
#                 # if item.lower() not in leaves[:leaves.find('_')].lower():
#                     item_parent = self.treeview.parent(leaves)
#                     item_no = self.treeview.index(leaves)
#                     self.hidden_leafs.append({'itemNumber': item_no, 'itemParent': item_parent, 'itemID': leaves})
#                     self.treeview.detach(leaves)
#
#     def display_all(self):
#         for hiddenleafs in reversed(self.hidden_leafs):
#             self.treeview.reattach(hiddenleafs['itemID'], hiddenleafs['itemParent'], hiddenleafs['itemNumber'])
#
#     def selected_item(self, value='name'):
#         # curItem = self.treeview.selection()  # element, który otrzymał fokus
#         if self.treeview.selection():
#             curItem = self.treeview.selection()[0]
#         else:
#             curItem = ''
#         curItemname = self.treeview.item(curItem)["text"]
#         if value == 'name':
#             return self.treeview.item(curItem)["text"]
#         elif value == 'data':
#             return self.treeview.item(curItem)
#         elif value == 'id':
#             return curItem
#         elif value == 'tags':
#             return self.treeview.item(curItem)['tags']
#         elif value == 'both':
#             return {'code': curItem, 'name': self.treeview.item(curItem)["text"]}
#         else:
#             return curItem
#
#     def searchval(self, name='', index='', mode=''):
#         # self.list_specific_functions.delete_leaf("SEARCH RESULT")
#         # print(self.search_var.get())
#         # children = list(self._detached) + list(self.tree.get_children())
#         sval = self.search_var.get()
#         for hiddenleafs in reversed(self.hidden_leafs):
#             checkid = hiddenleafs['itemID']
#             if sval.lower() in self.treeview.item(checkid)['text'].lower():
#             # if sval.lower() in checkid[:checkid.find('_')].lower():
#                 self.treeview.reattach(checkid, hiddenleafs['itemParent'], hiddenleafs['itemNumber'])
#         i_r = -1
#         if sval:
#             self.filter_leafs(sval, self.treeview.get_children())
#         else:
#             self.display_all()
#
#     def find_iid(self, iid, branch=''):
#         childs = self.treeview.get_children(branch)
#         target = ''
#         for children in childs:
#             if children == iid:
#                 return children
#             if children.find('_') < 0:
#                 temp = children
#             else:
#                 temp = children[:children.find('_')]
#             if temp == iid:
#                 return children
#             else:
#                 target = self.find_iid(iid, children)
#             if target:
#                 return target
#     def find_iid2(self, iid, branch=''):
#         childs = self.treeview.get_children(branch)
#         target = ''
#         for children in childs:
#             if self.treeview.item(children)['text'] == iid:
#                 return children
#             # if children.find('_') < 0:
#             #     temp = children
#             # else:
#             #     temp = children[:children.find('_')]
#             # if temp == iid:
#             #     return children
#             else:
#                 target = self.find_iid2(iid, children)
#             if target:
#                 return target
#
#     def open_tree(self):
#         for items in self.treeview.get_children(''):
#             self.treeview.item(items, open=True)
#
#     def find_root_parent(self, child):
#         parent = self.treeview.parent(child)
#         if parent:
#             parent = self.find_root_parent(parent)
#             return parent
#         else:
#             return child
#
#     def change_size(self, wid, hei):
#         if wid:
#             self.treeview.column("#0", width=wid)
#         if hei:
#             self.treeview.configure(height=hei)
#
#     def deselect_row(self):
#         self.treeview.selection_remove(self.treeview.selection()[0])
#
#     def update_row(self, new_text, update=False):
#         """get selection. if escaped, selection is empty, while focus always remains on the item."""
#         current_item = self.treeview.selection()
#         """if selected, if in branch, focus on branch,  get its position, if not, then we add at the end"""
#         if current_item:
#             if self.treeview.parent(current_item[0]):
#                 current_item = [self.treeview.parent(current_item[0])]
#             update_position = self.treeview.index(current_item[0])
#         else:
#             update_position = 'end'
#         """if update, delete current selection and put new text on that place.
#             otherwise, just add leave, index will increase on its own."""
#         if update:
#             self.treeview.delete(current_item[0])
#             # update_position += 1
#         self.add_branch(new_text, [], position=update_position, update_flag=False)
#         # self.add_leaves('', [new_text], position=update_position, update_flag=False)
#
#     def gather_data(self, branch=''):
#         temp_list = []
#         for leaves in self.treeview.get_children(branch):
#             if not self.treeview.get_children(leaves):
#                 temp_list.append(self.treeview.item(leaves)['text'])
#             else:
#                 temp_dict = {self.treeview.item(leaves)['text']: self.gather_data(leaves)}
#                 # temp_dict[leaves] = self.gather_data(leaves)
#                 temp_list.append(temp_dict)
#         return temp_list
#
#     def update_branch(self, new_data):
#         """update entire branch, so delete it and put anew. new_data should be a dictionary"""
#         item = self.treeview.selection()[0]
#         if item:
#             for items in self.treeview.get_children(item):
#                 self.treeview.delete(items)
#             for values in new_data:
#                 self.treeview.insert(item, 'end', text=values)
#
#     def add_leaves_simple(self, iid, values):
#         for i in values:
#             self.treeview.insert(iid, 'end', text=i)
#     def add_leaf(self, iid, code, txt):
#         """used to add single leaves with specific id, to be able to delete later without searching"""
#         return self.treeview.insert(iid, 'end', code, text=txt)
#     # TODO add moving selection up and down
#     def move_up(self):
#         return
#     #     selected_items = self.treeview.selection_get()
#     def move_down(self):
#         return
#     def insert_row(self, new_rows):
#         current_item = self.treeview.selection()
#         """if selected, get its position"""
#         if current_item:
#             update_position = self.treeview.index(current_item[0])
#         else:
#             return
#         selected_parent = self.treeview.parent(current_item[0])
#         new_rows.reverse()
#         for value in new_rows:
#             self.treeview.insert(selected_parent, update_position, text=value)
#
#     def delete_with_backup(self):
#         # deleted_element_dict_data = {}
#         temp_list = []
#         for element in self.treeview.selection():
#             deleted_element_dict_data = {'index': self.treeview.index(element), 'parent': self.treeview.parent(element),
#                                          'item': self.treeview.item(element)['text']}
#             temp_list.append(deleted_element_dict_data)
#         for element in self.treeview.selection():
#             self.treeview.delete(element)
#             # self.treeview.detach(element)
#         if temp_list:
#             if len(self.back_up_deleted) > 5:
#                 self.back_up_deleted.pop(0)
#             self.back_up_deleted.append(temp_list)
#
#     def restore_deleted(self):
#         if self.back_up_deleted:
#             element_to_restore = self.back_up_deleted.pop(-1)
#             for elements in element_to_restore:
#                 # self.treeview.reattach(elements['item'], elements['parent'], elements['index'])
#                 self.treeview.insert(elements['parent'], elements['index'], text=elements['item'])
#
#
# class SceneCreateToolTip(object):
#     """ tk_ToolTip_class101.py
#     gives a Tkinter widget a tooltip as the mouse is above the widget
#     tested with Python27 and Python34  by  vegaseat  09sep2014
#     www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
#
#     Modified to include a delay time by Victor Zaccardo, 25mar16
#     """
#     """
#     create a tooltip for a given widget
#     """
#
#     def __init__(self, widget, text='widget info'):
#         self.waittime = 500  # miliseconds
#         self.wraplength = 180  # pixels
#         self.widget = widget
#         self.text = text
#         self.widget.bind("<Enter>", self.enter)
#         self.widget.bind("<Leave>", self.leave)
#         self.widget.bind("<ButtonPress>", self.leave)
#         self.id = None
#         self.tw = None
#
#     def enter(self, event=None):
#         self.schedule()
#
#     def leave(self, event=None):
#         self.unschedule()
#         self.hidetip()
#
#     def schedule(self):
#         self.unschedule()
#         self.id = self.widget.after(self.waittime, self.showtip)
#
#     def unschedule(self):
#         id = self.id
#         self.id = None
#         if id:
#             self.widget.after_cancel(id)
#
#     def showtip(self, event=None):
#         x = y = 0
#         x, y, cx, cy = self.widget.bbox("insert")
#         x += self.widget.winfo_rootx() + 25
#         y += self.widget.winfo_rooty() + 20
#         # creates a toplevel window
#         self.tw = tk.Toplevel(self.widget)
#         # Leaves only the label and removes the app window
#         self.tw.wm_overrideredirect(True)
#         self.tw.wm_geometry("+%d+%d" % (x, y))
#         label = tk.Label(self.tw, text=self.text, justify='left',
#                          background="#ffffff", relief='solid', borderwidth=1,
#                          wraplength=self.wraplength)
#         label.pack(ipadx=1)
#
#     def hidetip(self):
#         tw = self.tw
#         self.tw = None
#         if tw:
#             tw.destroy()
#
#
# # class SceneSimpleEntry(tk.Entry):
# #     def __init__(self, master=None, field_name='', tooltip_text='', field_data={}, **kwargs):
# #         if 'default' in field_data:
# #             self.default_value = field_data['default']
# #         else:
# #             self.default_value = ''
# #         if field_name:
# #             self.label = tk.Label(master=master, text=field_name)
# #             self.label.grid(row=0, column=0)
# #             if tooltip_text:
# #                 SceneCreateToolTip(self.label, tooltip_text)
# #         self.title = field_name
# #         self.var = tk.StringVar()
# #         # self.temp_master = master
# #         self.type = 'text'
# #         self.hidden_flag = True
# #         self.field_frame = master
# #         tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
# #         self.grid(row=1, column=0)
# #         # self.field = tk.Entry(master, textvariable=self.var, **kwargs)
# #         # self.field.grid(row=0, column=1, sticky='E')
# #         # self.field.getvar()
# #         self.old_value = ''
# #         # self.winfo_parent = self.field.winfo_parent
# #         # self._nametowidget = self.field._nametowidget
# #         self.get, self.set = self.var.get, self.var.set
# #         # if 'optiones' in field_data:
# #         #     if 'function' in field_data['optiones']:
# #         #         self.bind('<Button-1>', lambda event: self.test())
# #
# #     def test(self):
# #         print('test shortcut')
# #         # SceneWindow('', self, master=self.temp_master)
# #
# #     def get_val(self):
# #         # if self["state"] == 'disabled':
# #         #     self["state"] = 'normal'
# #         # print(self.var.get())
# #         return self.var.get()
# #
# #     def set_val(self, value):
# #         # self.insert(0, value)
# #         self.set(value)
# #
# #     def clear_val(self):
# #         self.set(self.default_value)
# #
# #     def hide_field(self):
# #         self.field_frame.pack_forget()
# #         self.hidden_flag = True
# #
# #     def show_field(self):
# #         self.field_frame.pack(side=tk.LEFT)
# #         self.hidden_flag = False
# """seems not used"""
# class SceneSimpleEntry(SimpleFields.SimpleEntry):
#     def __init__(self, master=None):
#         super().__init__(master=master, field_name='temp', label_position='U', tooltip_text=None, field_data=None)
#         # self.hidden_flag = True
#
#     def hide_field(self):
#         self.pack_forget()
#         # self.hidden_flag = True
#
#     def show_field(self):
#         self.pack(side=tk.LEFT)
#         # self.hidden_flag = False
#
# """should be obsolete"""
# class SceneAreaEntry(tk.Text):
#     def __init__(self, master=None, field_name='', widthI=20, heighI=4, tooltip_text='', **kwargs):
#         if field_name:
#             self.label = tk.Label(master=master, text=field_name)
#             self.label.grid(row=0, column=0)
#         if tooltip_text:
#             SceneCreateToolTip(self.label, tooltip_text)
#         self.title = field_name
#         # self.var = tk.StringVar()
#         self.type = 'area'
#         self.hidden_flag = False
#         self.field_frame = master
#         tk.Text.__init__(self, master, **kwargs)
#         self.grid(row=1, column=0)
#         self.old_value = ''
#         tk.Text.configure(self, width=widthI, heigh=heighI)
#
#     def get_val(self):
#         area_field = self.get(1.0, tk.END)
#         area_field = area_field[:-1]
#         area_field = area_field.replace('\n', ' ')
#         return area_field
#
#     def set_val(self, value):
#         self.insert(1.0, value)
#
#     def clear_val(self):
#         self.delete(1.0, tk.END)
#
#     def hide_field(self):
#         self.field_frame.pack_forget()
#         self.hidden_flag = True
#
#     def show_field(self):
#         self.field_frame.pack()
#         self.hidden_flag = False
#
#     def change_size(self, wide, height):
#         self.configure(width=wide, height=height)
#
#
# class SceneSingleList(SimpleFields.SingleList):
#     def __init__(self, master=None, list_path=[]):
#         super().__init__( master=master, field_name='temp', tooltip_text=None, label_position='U', list_path=list_path)
#         # if frame_type:
#         #     self.field_frame = tk.Frame(master)
#         #     # for some reason i put here additional frame. try to change it into optional based on parameter in creation.
#         #     self.field_frame.pack(side=tk.LEFT)
#         # else:
#         #     self.field_frame = master
#         # self.hidden_flag = True
#         self.traceId = ''
#
#     def clear_val(self, mode='all'):
#         # if self.traceId:
#         if mode:
#             if self.traceId:
#                 self.var.trace_vdelete('w', self.traceId)
#                 self.traceId = ''
#         self.var.set('select options')
#         self.field['menu'].delete(0, 'end')
#         self.list = []
#
#     def hide_field(self):
#         self.pack_forget()
#         # self.hidden_flag = True
#
#     def show_field(self):
#         self.pack(side=tk.LEFT)
#         # self.hidden_flag = False
#
#     def update_list(self, choices):
#         self.list = otherFunctions.getListOptions(choices, "single")
#         menu = self.field["menu"]
#         menu.delete(0, "end")
#         for string in self.list:
#             menu.add_command(label=string,
#                              command=lambda value=string: self.var.set(value))
# # class SceneSingleList(SimpleFields.SingleList):
# #     def __init__(self, master=None, list_path=[], field_name='', tooltip_text='', frame_type=True):
# #         # super().__init__( master=None, field_name=None, tooltip_text=None, label_position=None, list_path=None)
# #         if frame_type:
# #             self.field_frame = tk.Frame(master)
# #             # for some reason i put here additional frame. try to change it into optional based on parameter in creation.
# #             self.field_frame.pack(side=tk.LEFT)
# #         else:
# #             self.field_frame = master
# #         self.hidden_flag = True
# #         if field_name:
# #             self.label = tk.Label(master=self.field_frame, text=field_name)
# #             self.label.grid(row=0, column=0)
# #         if tooltip_text:
# #             SceneCreateToolTip(self.label, tooltip_text)
# #         self.var = tk.StringVar()
# #         self.type = 'singlelist'
# #         self.title = field_name
# #         self.list = otherFunctions.getListOptions(list_path, "single")
# #         if len(self.list) == 0:
# #             self.list.append('placeholder')
# #         tk.OptionMenu.__init__(self, self.field_frame, self.var, *self.list)
# #         self.grid(row=0, column=1)
# #         self.get, self.set = self.var.get, self.var.set
# #         """for hiding and showing with pack manager. in adding functions it is using pack, in scene window its grid"""
# #         self.field_frame_2 = master
# #         self.traceId = ''
# #
# #         # label = tk.Label(master=self.field_frame, text='test place')
# #         # label.grid(row=0, column=1)
# #
# #     def get_val(self):
# #         return self.get()
# #
# #     def set_val(self, value):
# #         if len(value) > 1:
# #             self.list = value
# #             self.var = ''
# #             self['menu'].delete(0, 'end')
# #             for val in self.list:
# #                 self['menu'].add_command(label=val, command=tk._setit(self.var, val))
# #                 # print('test')
# #                 # self.list = otherFunctions.getListOptions(value, "single")
# #                 # self.var.set(self.list[0])
# #         else:
# #             self.set(value)
# #
# #     def clear_val(self):
# #         if self.traceId:
# #             self.var.trace_vdelete('w', self.traceId)
# #             self.traceId = ''
# #         self.var.set('select options')
# #
# #     def hide_field(self):
# #         self.field_frame_2.pack_forget()
# #         self.hidden_flag = True
# #
# #     def show_field(self):
# #         self.field_frame_2.pack(side=tk.LEFT)
# #         self.hidden_flag = False
# #
# #     def update_list(self, choices):
# #         self.list = otherFunctions.getListOptions(choices, "single")
# #         menu = self["menu"]
# #         menu.delete(0, "end")
# #         for string in self.list:
# #             menu.add_command(label=string,
# #                              command=lambda value=string: self.var.set(value))
#
# class SceneMultiList(SimpleFields.MultiList):
#     def __init__(self, master=None, list_path=[], field_options=[]):
#         super().__init__(master, 'temp', '', 'U', list_path, field_options=field_options)
#         # self.hidden_flag = True
#         self.traceId = ''
#         # self.frame_multi = tk.Frame(self)
#         # self.data_tree = SimpleFields.ElementsList(self.frame_multi, 1, 0, '', colspan=2, treeview_height=3)
#         # self.data_tree.treeview.configure(selectmode='extended')
#         # self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
#         # self.edit_flag = False
#
#     def hide_field(self):
#         self.pack_forget()
#         self.hidden_flag = True
#
#     def show_field(self):
#         self.pack(side=tk.LEFT)
#         # self.hidden_flag = False
#
#     def clear_val(self, all_flag=None):
#         if self.var.trace_info():
#             if self.traceId:
#                 self.var.trace_vdelete('w', self.traceId)
#                 self.traceId = ''
#             if self.var.trace_id:
#                 self.var.trace_vdelete('w', self.var.trace_id)
#         self.var.set('OPTIONS')
#         # self.clear_all_tags()
#         # if self.single_item != 0:
#         #     self.single_item = 1
#         for item in self.tree_options_choose.treeview.selection():
#             self.tree_options_choose.treeview.selection_remove(item)
#         if self.version != 'single':
#             for item in self.data_tree.treeview.get_children():
#                 self.data_tree.treeview.delete(item)
#         """temporary solution"""
#         if all_flag:
#             for item in self.tree_options_choose.treeview.get_children():
#                 self.tree_options_choose.treeview.delete(item)
#         self.tree_options_choose.treeview.unbind('<<TreeviewSelect>>')
#
#     def update_list(self, choices):
#         for item in self.tree_options_choose.treeview.get_children():
#             self.tree_options_choose.treeview.delete(item)
#         self.list = otherFunctions.getListOptions(choices, "multi")
#         for element_name in self.list:
#             self.tree_options_choose.add_branch(element_name, self.list[element_name], update_flag=True)
#         # for val in choices:
#         #     if 'current' in val:
#         #         target_leaf = val[7:]
#         #         element_to_update = val[11:]
#         #         for element_lists in GlobalVariables.list_elementlists:
#         #             if element_lists.treeview.heading("#0")['text'] == element_to_update:
#         #                 otherFunctions.duplicate_treeview(element_lists.treeview, self.tree_options_choose.treeview, destination_leaf=target_leaf)
#         #                 break
#         #         break
#
#     def set_up_multi(self, flag_unique=False):
#         print('set up multi')
#         if flag_unique:
#             self.version = 'unique'
#             print('set up unique')
#         else:
#             self.version = 'multi'
#         self.tree_options_choose.treeview.configure(selectmode='extended')
#         self.tree_options_choose.treeview.bind('<a>', lambda event: self.add_multi_value())
#         self.data_tree.show_tree()
#         # self.configure(textvariable=tk.StringVar)
#         # self.button_select['text'] = 'Add'
#         # self.button_select.configure(command=self.add_multi_value)
#         # self.button_clear['text'] = 'Delete'
#         # self.button_clear.configure(command=self.delete_multi_value)
#         # self.tree_options_choose.treeview.bind('<s>', lambda event: self.add_multi_value())
#         # self.frame_multi.grid(row=5, column=1)
#         # self.multi_value_flag = True
#         # self.single_item = 0
#     def set_up_single(self):
#         # print('set up single')
#         self.version = 'single'
#         self.tree_options_choose.treeview.configure(selectmode='browse')
#         self.data_tree.hide_tree()
#         # self.configure(textvariable=tk.StringVar)
#         # self.button_select['text'] = 'Select'
#         # self.button_select.configure(command=self.select_row)
#         # self.button_clear['text'] = 'Clear'
#         # self.button_clear.bind('<Button-1>', self.clear_selected)
#         # self.tree_options_choose.treeview.bind('<s>', lambda event: self.select_row())
#         # self.frame_multi.grid_forget()
#         # self.multi_value_flag = False
#         # self.single_item = items
#
# # class SceneMultiList(tk.Button):
# #     def __init__(self, master=None, list_path=[], rowposition=1, colpos=0,
# #                  field_name='',  field_options=[], autonomus=True):
# #         """here it shoould always be with all fields. for multivalue, in separate frame. Functions only hide or show,
# #          so it should also read options in structure and change this field to it"""
# #         if 'autonomus' in field_options:
# #             self.autonomus = autonomus
# #         else:
# #             self.autonomus = ''
# #         if 'multi_item' in field_options:
# #             self.multi_value_flag = True
# #         else:
# #             self.multi_value_flag = False
# #         if 'single_item' in field_options:
# #             self.single_item = 1
# #         else:
# #             self.single_item = 0
# #         self.autonomus = autonomus
# #         if self.autonomus:
# #             if field_name:
# #                 self.label = tk.Label(master=master, text=field_name)
# #                 self.label.grid(row=0, column=0, columnspan=3)
# #             self.button_select = tk.Button(master, text='SELECT', command=self.select_row)
# #             # self.button_select.grid(row=rowposition, column=colpos)
# #             self.button_clear = tk.Button(master, text='Clear', command=self.clear_selected)
# #             self.button_clear.bind('<Shift-c>', self.clear_selected)
# #             # self.button_clear.grid(row=rowposition, column=colpos + 5)
# #             # self.button_done = tk.Button(master, text='DONE', command=self.done)
# #             self.button_done = tk.Button(master, text='DONE')
# #             self.button_done.bind('<Button-1>', self.done)
# #         self.start_pos_row = rowposition
# #         self.start_pos_col = colpos
# #         self.var = tk.StringVar()
# #         self.title = field_name
# #         self.type = 'multilist'
# #         self.field_frame = master
# #         self.hidden_flag = True
# #         # if single_item:
# #         #     self.single_item = 1
# #         # else:
# #         #     self.single_item = 0
# #         self.list = otherFunctions.getListOptions(list_path, 'multi')
# #         # if 'current' in list_path
# #         self.var.set('OPTIONS')
# #         self.treeview_optionstochoose = SceneElementsList(self.field_frame, self.start_pos_row + 1, 0,
# #                                                           listTitle=field_name, treeview_height=3)
# #         # masterWun, rowPos, colPos, listTitle, colspan = 1,
# #         for element_name in self.list:
# #             self.treeview_optionstochoose.add_branch(element_name, self.list[element_name])
# #         self.treeview_optionstochoose.hide_tree()
# #         self.treeview_optionstochoose.treeview.configure(selectmode='extended')
# #         self.treeview_optionstochoose.treeview.tag_configure('selected', background='red')
# #         # self.butCommand = partial(display_options_tree, self.treeview_optionstochoose, self.var)
# #         # self.butCommand = partial(self.open_tree())
# #         # self.button_controlTreeview = tk.Button.__init__(self, master, text='OPTIONS', wraplength=150,
# #         #                                                  textvariable=self.var, command=self.butCommand)
# #         self.button_controlTreeview = tk.Button.__init__(self, self.field_frame, text='OPTIONS', wraplength=150,
# #                                                          textvariable=self.var, command=self.open_tree)
# #         # if self.multi_value_flag:
# #         #     self.treeview_optionstochoose.treeview.bind('<s>', lambda event: self.add_multi_value())
# #         # else:
# #         self.treeview_optionstochoose.treeview.bind('<s>', lambda event: self.select_row())
# #         # self.button_done.grid(row=rowposition, column=colpos + 6)
# #         # self.button_controlTreeview = tk.Button.__init__(self, master, text='OPTIONS', wraplength=150,
# #         #                                                  textvariable=self.var, command=self.butCommand, **kwargs)
# #         self.selected_items = []
# #         self.grid(row=self.start_pos_row + 1, column=0, columnspan=5)
# #         self.get, self.set = self.var.get, self.var.set
# #         self.display_flag = True
# #         self.frame_multi = tk.Frame(self.field_frame)
# #         # if self.multi_value_flag:
# #             # self.configure(textvariable=tk.StringVar)
# #             # self.button_select['text'] = 'Add'
# #             # self.button_select.configure(command=self.add_multi_value)
# #             # self.button_clear['text'] = 'Delete'
# #             # self.button_clear.configure(command=self.delete_multi_value)
# #         self.data_tree = SceneElementsList(self.frame_multi, self.start_pos_row + 1, 0, '', colspan=2, treeview_height=3)
# #         self.data_tree.treeview.configure(selectmode='extended')
# #         self.data_tree.treeview.bind('<Escape>', lambda event: self.deselect_row())
# #         self.edit_flag = False
# #
# #         for key in self.list.keys():
# #             if 'Mod' in key:
# #                 # if key.find('/') < 0:
# #                 #     end_val_index = len(key)
# #                 # else:
# #                 #     end_val_index = key.find('/')
# #                 element = key[4:]
# #                 GlobalVariables.multi_lists_to_refresh[element].append(self.treeview_optionstochoose)
# #                 break
# #     def set_val(self, values):
# #         if self.multi_value_flag:
# #             for value in values:
# #                 self.data_tree.add_branch(value, [], update_flag=False)
# #         else:
# #             temp = 'OPTIONS'
# #             if not isinstance(values, list):
# #                 values = [values]
# #             for value in values:
# #                 if value == '':
# #                     continue
# #                 temp = temp + '\n' + value
# #             self.var.set(temp)
# #     def get_val(self, temp_dict_container=None):
# #         temp = self.var.get()
# #         temp = temp.split('\n')
# #         if temp[0] == 'OPTIONS' and len(temp) == 1:
# #             # temp[0] = ''
# #             temp.remove('OPTIONS')
# #         else:
# #             temp.remove('OPTIONS')
# #         # if len(temp) == 1:
# #         #     temp.append('')
# #         if self.single_item:
# #             temp = temp[0]
# #         elif self.multi_value_flag:
# #             all_vals = self.data_tree.treeview.get_children()
# #             for value in all_vals:
# #                 temp.append(self.data_tree.treeview.item(value)['text'])
# #         if temp_dict_container is not None:
# #             temp_dict_container[self.title] = temp
# #         else:
# #             return temp
# #
# #     def clear_val(self):
# #         self.var.set('OPTIONS')
# #         for item in self.treeview_optionstochoose.treeview.selection():
# #             self.treeview_optionstochoose.treeview.selection_remove(item)
# #         if self.multi_value_flag:
# #             for item in self.data_tree.treeview.get_children():
# #                 self.data_tree.treeview.delete(item)
# #
# #     def open_tree(self):
# #         # print('test')
# #         selected_values = self.var.get().split('\n')
# #         # print(selected_values)
# #         self.grid_forget()
# #         """for now, there is usually word OPTION in list, so if there is something selected, there will be more
# #         since selectItemsInTree removes items from the selectedItems list, i make a temp list, which later is
# #         copied back to the selectedItems. This way, when done selecting, no need to iterate over the treeview to check
# #         for selected tags, just display what is in the selectedItems list"""
# #         if len(selected_values) > 1:
# #             self.selected_items = selected_values[1:]
# #             self.select_loaded_items_in_tree()
# #             self.selected_items = selected_values[1:]
# #         # self.var.set("                                                              ")
# #         # self.button_select.grid(row=self.start_pos_row, column=self.start_pos_col)
# #         # self.button_clear.grid(row=self.start_pos_row, column=self.start_pos_col + 1)
# #         # self.button_done.grid(row=self.start_pos_row, column=self.start_pos_col + 2)
# #         if self.autonomus:
# #             self.button_select.grid(row=self.start_pos_row, column=self.start_pos_col, sticky='W', columnspan=4)
# #             self.button_clear.grid(row=self.start_pos_row, column=self.start_pos_col, columnspan=3)
# #             self.button_done.grid(row=self.start_pos_row, column=self.start_pos_col, sticky='E', columnspan=3)
# #         self.treeview_optionstochoose.show_tree()
# #     def select_row(self):
# #         # print(self.selected_items)
# #         # print(str(self.treeview_optionstochoose.treeview.selection()))
# #         user_selection = self.treeview_optionstochoose.treeview.selection()
# #         if self.single_item and len(user_selection)>1:
# #             messagebox.showwarning('only single item allowed','Please select only 1 item')
# #             return
# #         for selection in user_selection:
# #             if self.treeview_optionstochoose.treeview.get_children(selection) == ():
# #                 if 'selected' in self.treeview_optionstochoose.treeview.item(selection)['tags']:
# #                     self.treeview_optionstochoose.treeview.item(selection, tags=())
# #                     self.selected_items.remove(self.treeview_optionstochoose.treeview.item(selection)['text'])
# #                     if self.single_item > 0:
# #                         self.single_item -= 1
# #                 else:
# #                     if self.single_item > 0:
# #                         if self.single_item > 1:
# #                             messagebox.showwarning('only single item allowed', 'Please deselect previous item')
# #                             return
# #                         else:
# #                             self.single_item += 1
# #                     self.treeview_optionstochoose.treeview.item(selection, tags='selected')
# #                     self.selected_items.append(self.treeview_optionstochoose.treeview.item(selection)['text'])
# #         self.treeview_optionstochoose.treeview.selection_remove(self.treeview_optionstochoose.treeview.selection()[0])
# #         self.edit_flag = True
# #     def clear_selected(self):
# #         warning = messagebox.askokcancel("clearing all items", "are you sure you want to clear all selected items?")
# #         if warning:
# #             self.clear_all_tags()
# #             self.selected_items = []
# #             if self.single_item > 1:
# #                 self.single_item -= 1
# #         self.edit_flag = True
# #     def clear_all_tags(self, item=''):
# #         # print('test')
# #         # recursivly search all lowest levels and clear tags
# #         children_of_item = self.treeview_optionstochoose.treeview.get_children(item)
# #         if children_of_item:
# #             for items in children_of_item:
# #                 self.clear_all_tags(items)
# #         else:
# #             if 'selected' in self.treeview_optionstochoose.treeview.item(item)['tags']:
# #                 self.treeview_optionstochoose.treeview.item(item, tags=())
# #
# #     def select_loaded_items_in_tree(self, item_to_check=''):
# #         children_of_item = self.treeview_optionstochoose.treeview.get_children(item_to_check)
# #         if children_of_item:
# #             for items in children_of_item:
# #                 self.select_loaded_items_in_tree(items)
# #         else:
# #             for select in self.selected_items:
# #                 if select == self.treeview_optionstochoose.treeview.item(item_to_check)['text']:
# #                     self.treeview_optionstochoose.treeview.item(item_to_check, tags='selected')
# #                     self.selected_items.remove(select)
# #                     break
# #
# #     def done(self, *args):
# #         """similar to function display list tree, hide buttons, treeview and update main button with items from
# #         selectedItems list"""
# #         # self.treeview_optionstochoose.hide_tree()
# #         # print(str(self.treeview_optionstochoose.treeview.item(self.treeview_optionstochoose.treeview.focus())))
# #         if self.treeview_optionstochoose.treeview.winfo_ismapped():
# #             self.treeview_optionstochoose.hide_tree()
# #         if self.autonomus:
# #             self.button_select.grid_forget()
# #             self.button_clear.grid_forget()
# #             self.button_done.grid_forget()
# #             if self.edit_flag:
# #                 if self.multi_value_flag:
# #                     for branches in self.data_tree.treeview.get_children():
# #                         self.selected_items.append(self.data_tree.treeview.item(branches)['text'])
# #                 final_selected_items_text = 'OPTIONS'
# #                 for selected in self.selected_items:
# #                     final_selected_items_text += '\n' + selected
# #                 self.var.set(final_selected_items_text)
# #         self.grid(row=self.start_pos_row + 1, column=0, columnspan=7)
# #         self.edit_flag = False
# #
# #     def display(self, flag=None):
# #         if flag is None:
# #             flag = self.display_flag
# #         if flag:
# #             self.grid_forget()
# #             self.treeview_optionstochoose.hide_tree()
# #             self.display_flag = False
# #         else:
# #             self.grid(row=self.start_pos_row + 1, column=0, columnspan=7)
# #             self.treeview_optionstochoose.show_tree()
# #             self.display_flag = True
# #
# #     def hide_field(self):
# #         self.field_frame.pack_forget()
# #         self.hidden_flag = True
# #
# #     def show_field(self):
# #         self.field_frame.pack(side=tk.LEFT)
# #         self.hidden_flag = False
# #
# #     def add_multi_value(self):
# #         item = self.treeview_optionstochoose.selected_item()
# #         self.data_tree.add_branch(item,[], update_flag=False)
# #         # self.selected_items.append(item)
# #         # self.var.set(self.var.get() + '\n' + item)
# #
# #     def delete_multi_value(self):
# #         item = self.data_tree.selected_item(value='code')
# #         self.data_tree.delete_leaf(item)
# #
# #     def deselect_row(self):
# #         self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])
# #
# #     def update_list(self, choices):
# #         self.list = otherFunctions.getListOptions(choices, "multi")
# #         for element_name in self.list:
# #             self.treeview_optionstochoose.add_branch(element_name, self.list[element_name])
# #
# #     def set_up_multi(self):
# #         self.configure(textvariable=tk.StringVar)
# #         self.button_select['text'] = 'Add'
# #         self.button_select.configure(command=self.add_multi_value)
# #         self.button_clear['text'] = 'Delete'
# #         self.button_clear.configure(command=self.delete_multi_value)
# #         self.treeview_optionstochoose.treeview.bind('<s>', lambda event: self.add_multi_value())
# #         self.frame_multi.grid(row=5, column=0)
# #         self.multi_value_flag = True
# #     def set_up_single(self):
# #         # self.configure(textvariable=tk.StringVar)
# #         self.button_select['text'] = 'Select'
# #         self.button_select.configure(command=self.select_row)
# #         self.button_clear['text'] = 'Clear'
# #         self.button_clear.bind('<Button-1>', self.clear_selected)
# #         self.treeview_optionstochoose.treeview.bind('<s>', lambda event: self.select_row())
# #         self.frame_multi.grid_forget()
# #         self.multi_value_flag = False
#
# class SceneSpeaks:
#     def __init__(self, master_frame, title_frame):
#         self.title_field = title_frame
#         self.var = tk.StringVar()
#         self.values_list = []
#         temp_list = GlobalVariables.templates['Events'].frame_fields['Speakers'].get_val()
#         for dict_data in temp_list:
#             self.values_list.append(dict_data['name'])
#
#         self.value_field_list = tk.OptionMenu(master_frame, self.var, *self.values_list)
#         self.var.trace('w', self.set_val)
#
#
#     def destroy(self):
#         # self.value_field_list.pack_forget()
#         return
#
#     def show_field(self):
#         self.value_field_list.pack(side=tk.LEFT)
#         self.hidden_flag = False
#
#     def set_val(self, *args):
#         val_idx = self.values_list.index(self.var.get())
#         if val_idx == 0:
#             val_idx = ''
#         self.title_field.set_val('Speaks' + str(val_idx))
#     def get_val(self):
#         self.value_field_list.destroy()
#
class StatCheckField:
    def __init__(self, master_frame):
        self.frame_data = tk.Frame(master_frame)
        # TODO correct path for function
        self.sub_functions_structure_data = GlobalVariables.functions_data['Event Only']['Stat Checks'][0]['subfunction']
        self.button_start = tk.Button(master=self.frame_data, text='Change difficulty options', command=self.display_data)
        self.flag_displayed_data = False
        self.col_span = 6
        self.button_start.grid(row=0, columnspan=self.col_span)

        self.list_options_values = list(self.sub_functions_structure_data['structure'].keys())
        self.var_list = tk.StringVar()
        self.var_list.set('')
        self.list_options = tk.OptionMenu(self.frame_data, self.var_list, *self.list_options_values)
        self.var_list.trace('w', self.set_fields)

        self.fields_list = []
        """button with treeview to control data"""
        self.button_add = tk.Button(self.frame_data, text='SAVE', command=self.add_value)
        self.button_edit = tk.Button(self.frame_data, text='EDIT', command=self.edit_value)
        # self.button_delete = tk.Button(self.frame_data, text='DELETE', command=self.delete_value)
        self.update_flag = False
        self.temp_selection = None
        # self.list = otherFunctions.getListOptions(list_path, 'multi')
        # self.var.set('Clicktoselect values')
        # self.tree_data = SimpleFields.ElementsList(self.frame_data, 10, 0, 'Conditions', self.col_span)
        self.tree_data = SceneElementsList(self.frame_data, 10, 0, 'Conditions', self.col_span)
        self.tree_data.hide_tree()

    def set_val(self, values_list):
        """data is not marked, but more or less has a pattern. last 5 values i main statcheck data, before that are various options"""
        main_stat_data = values_list[-5:]
        difficulty_options = values_list[:-6]
        branch = None
        for options in difficulty_options:
            if options == 'ChangeStatCheckDifficulty':
                continue
            if options in self.list_options_values:
                branch = self.tree_data.add_branch(options,update_flag=False)
            self.tree_data.add_leaves_simple(branch, [options])
        for stat_data, fields in zip(main_stat_data, self.fields_list[-5:]):
            fields.set_val(stat_data)

    def get_val(self):
        temp_list = []
        roots = self.tree_data.treeview.get_children()
        for root in roots:
            temp_list.append('ChangeStatCheckDifficulty')
            temp_list.append(self.tree_data.treeview.item(root)['text'])
            leaves = self.tree_data.treeview.get_children(root)
            for leaf in leaves:
                temp_list.append(self.tree_data.treeview.item(leaf)['text'])
        return temp_list

    def clear_val(self):
        self.var_list.set('')


    def show_field(self):
        self.frame_data.pack(side=tk.LEFT)
    def hide_field(self):
        self.frame_data.pack_forget()

    def display_data(self):
        if self.flag_displayed_data:
            self.list_options.grid_forget()
            self.button_add.grid_forget()
            self.button_edit.grid_forget()
            # self.button_delete.grid_forget()
            self.tree_data.hide_tree()
            self.flag_displayed_data = False
        else:
            self.list_options.grid(row=1, columnspan=self.col_span)
            self.button_add.grid(row=9, columnspan=self.col_span, sticky=tk.W)
            self.button_edit.grid(row=9, columnspan=self.col_span)
            # self.button_delete.grid(row=9, columnspan=self.col_span, sticky=tk.E)
            self.tree_data.show_tree()
            self.flag_displayed_data = True
        return

    def set_fields(self, *args):
        for field in self.fields_list:
            field.destroy()
        self.fields_list.clear()
        sub_function_name = self.var_list.get()
        if sub_function_name:
            structure = self.sub_functions_structure_data['structure'][sub_function_name]
            row_no = 2
            column_no = 0
            for field in structure:
                tooltip = ''
                tempfield = ''
                if structure[field]["type"] == "text":
                    tempfield = SimpleFields.SimpleEntry(master=self.frame_data, field_name=field, label_position='L'
                                                         , tooltip_text=tooltip, field_data=structure[field])
                elif structure[field]["type"] == "int":
                    tempfield = SimpleFields.NumericEntry(master=self.frame_data, wid=4, field_name=field,
                                                          label_position='L'
                                                          , tooltip_text=tooltip, field_data=structure[field])
                    tempfield.bind("<Tab>", otherFunctions.focus_next_window)
                elif structure[field]["type"] == "singlelist":
                    # tempfield = SimpleFields.SingleList(self.frame_data, field, tooltip, 'L', structure[field]['choices'])
                    tempfield = SceneSingleList(self.frame_data)
                    tempfield.update_list(structure[field]['choices'])
                    tempfield.update_label(field)
                elif structure[field]["type"] == 'multilist':
                    tempfield = SceneMultiList(self.frame_data, structure[field]['choices'],
                                               field_options=structure[field]['options'])
                    tempfield.update_label(field)
                elif structure[field]['type'] == 'choiceField':
                    tempfield = Choices(self.frame_data)
                    tempfield.field_choice_no.grid(row=row_no, column=column_no)
                    tempfield.field_choice_text.grid(row=row_no+1, column=column_no)
                    self.fields_list.append(tempfield.field_choice_no)
                    self.fields_list.append(tempfield.field_choice_text)
                    column_no += 1
                    continue

                tempfield.grid(row=row_no, column=column_no)
                column_no += 1
                self.fields_list.append(tempfield)
        return

    def add_value(self):
        branch = self.var_list.get()
        values_list = []
        for fields in self.fields_list:
            values_list.append(fields.get_val())
            fields.clear_val()
        if self.update_flag:
            self.tree_data.update_branch(values_list)
            self.update_flag = False
        else:
            branch = self.tree_data.add_branch(branch, values_list, update_flag=False)
            # self.tree_data.add_leaves_simple(branch, values_list)
        # self.tree_data.add_branch(branch, values_list)

    def edit_value(self):
        self.update_flag = True
        select_item = self.tree_data.selected_item(value='code')
        # self.temp_selection = select_item
        item_data = self.tree_data.treeview.get_children(select_item)
        if not item_data:
            """user selected leaf node"""
            select_item = self.tree_data.treeview.parent(select_item)
        difficulty_option = self.tree_data.treeview.item(select_item)['text']
        self.var_list.set(difficulty_option)
        temp_data = self.tree_data.treeview.get_children(select_item)
        difficulty_data = []
        for tdata in temp_data:
            difficulty_data.append(self.tree_data.treeview.item(tdata)['text'])
        for field, set_data in zip(self.fields_list, difficulty_data):
            field.set_val(set_data)

    # def delete_value(self):
    #     select_item = self.tree_data.selected_item(value='code')
    #     item_data = self.tree_data.treeview.get_children(select_item)
    #     if not item_data:
    #         """user selected leaf node"""
    #         select_item = self.tree_data.treeview.parent(select_item)
    #     self.tree_data.delete_leaf(select_item)

    def destroy(self):
        self.frame_data.destroy()
#
class MenuField(QtWidgets.QWidget):
    def __init__(self, master_frame=None, mod_elements_treeview=None):
        super().__init__(None)
        self.treeview_main_game_items = mod_elements_treeview
        master_frame.addWidget(self)
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.custom_layout)
        """first, menu options - MaxMenuSlots and ShuffleMenu"""
        self.main_layout = self.custom_layout
        self.menu_main_options = SimpleFields.SingleList(None, 'Options',
                                                         {'choices': ['blank', 'MaxMenuSlots', 'ShuffleMenu']}, edit=False)
        self.menu_main_options.set_val('blank')
        self.menu_main_options.set_up_widget(self.main_layout)
        self.maxmenu_amount = SimpleFields.NumericEntry(None)
        """to add options amount next to Single list"""
        self.maxmenu_amount.set_up_widget(self.menu_main_options.custom_layout)
        # self.options_amount.set_up_widget(self.main_layout)
        self.maxmenu_amount.hide()
        self.menu_main_options.currentTextChanged.connect(self.menu_slots)

        """second, text field called 'choices-scenes' its selection are scenes in current event.
        Press enter to add new choice to menu - new branch to tree called same as scene"""

        self.choices_text = SimpleFields.MultiListDisplay(None, 'choices-scenes',
                                      field_data={'choices': ["Scenes-current"], 'options': ["single_item", "search"]},
                                      main_data_treeview=self.treeview_main_game_items)
        self.choices_text.final_data.returnPressed.connect(self.new_choice)
        self.choices_text.set_up_widget(self.main_layout)

        """now make creator of choices conditions. This has lots of options"""
        conditions_list = ['', 'FinalOption', 'EventJump', 'HideOptionOnRequirementFail', 'InverseRequirement',
                        'RequiresStat','RequiresItem', 'RequiresSkill', 'RequiresPerk', 'RequiresEnergy',
                        'RequiresVirility', 'RequiresItemEquipped', 'RequiresTime', 'RequiresFetishLevelEqualOrGreater',
                        'RequiresFetishLevelEqualOrLess', 'RequiresMinimumProgress', 'RequiresMinimumProgressFromEvent',
                        'RequiresLessProgress', 'RequiresLessProgressFromEvent', 'RequiresChoice',
                        'RequiresChoiceFromEvent']
        conditions_list.sort()
        self.menu_conditions = SimpleFields.SingleList(None, 'Conditions', label_pos='V')
        self.menu_conditions.label_custom.change_position('C')
        self.menu_conditions.reload_options(conditions_list)
        """connect to def that controls fields to display and hide and load choices"""
        self.menu_conditions.currentTextChanged.connect(self.menu_choice_options)
        self.menu_conditions.set_up_widget(self.main_layout)
        """not all elements should be added to main layouts, so other stuff should be in seperate widget"""
        self.field_widget_for_easy_remove = QtWidgets.QWidget()
        self.created_fields_layout = QtWidgets.QHBoxLayout()
        self.created_fields_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.field_widget_for_easy_remove.setLayout(self.created_fields_layout)
        self.main_layout.addWidget(self.field_widget_for_easy_remove)
        """these fields are what will be used"""
        field_number = SimpleFields.NumericEntry(edit=False)
        field_list = SimpleFields.SingleList(edit=False)
        field_list_2 = SimpleFields.SingleList(edit=False)
        field_multi = SimpleFields.MultiListDisplay(None, field_data={'options': ["single_item"]},main_data_treeview=self.treeview_main_game_items)
        field_multi.final_data.textChanged.disconnect()
        field_multi2 = SimpleFields.MultiListDisplay(None, field_data={'choices': ["Scenes"], 'options': ["single_item"]},main_data_treeview=self.treeview_main_game_items)
        field_multi2.final_data.textChanged.disconnect()
        field_checkbox = SimpleFields.CheckBox(None, 'ThenJumpToScene', 'ThenJumpToScene')
        field_checkbox.change_f(self.set_up_scene_field)
        # field_checkbox.value.trace_id = field_checkbox.value.trace('w', lambda *args: self.set_up_scene_field())
        self.fields_list = {'multi': field_multi, 'list1': field_list, 'list2': field_list_2,
                            'check': field_checkbox, 'multi2': field_multi2, 'int': field_number}
        for field in self.fields_list:
            self.fields_list[field].set_up_widget(self.created_fields_layout)
            self.fields_list[field].hide()
        """here is where all is displayed"""

        self.button_add_condition = SimpleFields.CustomButton(None, 'Add Condition')
        self.button_add_condition.clicked.connect(self.add_condition)
        self.main_layout.addWidget(self.button_add_condition)
        # self.data_display = SimpleFields.ElementsList(self.frame_for_fields, 2, 0, 'Menu choices', 2, False)
        self.final_data = SimpleFields.ElementsList(None, 'Menu choices', all_edit=True)
        self.final_data.set_up_widget(self.main_layout)
        self.prev_options = ''
        self.options_row = 1
        self.selected_filter_fields = []
    def set_val(self, values_to_set_list):
        """should accept list of values"""
        """first check for main menu options"""
        length_of_list = len(values_to_set_list)
        start_checking = 0
        if length_of_list[start_checking] in 'MaxMenuSlots ShuffleMenu':
            value = length_of_list[start_checking]
            if value == 'MaxMenuSlots':
                start_checking = 2
                self.menu_main_options.set_val('MaxMenuSlots')
                self.max_menu_slots.set_val(int(length_of_list[1]))
            elif value == 'ShuffleMenu':
                self.menu_main_options.set_val('ShuffleMenu')
                start_checking = 1
        choices_no = 1
        temp_list = []
        skip_no = 0
        for index in range(start_checking, length_of_list):
            if skip_no >= 0:
                skip_no -= 1
                continue
            selected_option = values_to_set_list[index]
            temp_list.append(selected_option)
            if selected_option in 'FinalOption HideOptionOnRequirementFail InverseRequirement':
                continue
            elif selected_option in 'RequiresMinimumProgress RequiresLessProgress RequiresEnergy RequiresVirility' \
                                    'RequiresItem RequiresItemEquipped RequiresPerk RequiresSkill RequiresTime' \
                                    ' EventJump ThenJumpToScene':
                temp_list.append(values_to_set_list[index + 1])
                skip_no = 1
            elif selected_option in 'RequiresFetishLevelEqualOrGreater RequiresFetishLevelEqualOrLess RequiresStat ' \
                                    'RequiresMinimumProgressFromEvent RequiresLessProgressFromEvent RequiresChoice':
                temp_list.append(values_to_set_list[index + 1])
                temp_list.append(values_to_set_list[index + 2])
                skip_no = 2
            elif selected_option in 'RequiresChoiceFromEvent':
                temp_list.append(values_to_set_list[index + 1])
                temp_list.append(values_to_set_list[index + 2])
                temp_list.append(values_to_set_list[index + 3])
                skip_no = 3
            else:
                self.data_display.add_branch('Choice ' + str(choices_no), temp_list, update_flag=False)
                temp_list.clear()
                choices_no += 1
                # data_to_load.append({str(len(data_to_load)+1): temp_list})








        return
    def get_val(self):
        return_values = []
        """first get main options, then what was added in the data display"""
        main_options = self.menu_main_options.get_val()
        if main_options != 'blank':
            return_values.append(main_options)
            if main_options == 'MaxMenuSlots':
                return_values.append(self.maxmenu_amount.get_val())
        displayed_data_list = self.final_data.get_data()
        for choice in displayed_data_list:
            for choice_element in choice:
                choice_elements_list = choice[choice_element]
                return_values += choice_elements_list
                return_values.append(choice_element)
        self.final_data.clear_tree()
        return return_values
    def clear_val(self):
        self.pack_forget()
    def destroy(self):
        self.setParent(None)
        self.deleteLater()

    def options_no(self, options_value):
        if options_value == 'MaxMenuSlots':
            self.maxmenu_amount.show()
        else:
            self.maxmenu_amount.hide()
    def new_choice(self):
        new_choice = self.choices_text.get_val()
        self.final_data.add_data(new_choice)

    def add_condition(self):
        """add condition to choice. Choice is branch name in final data."""
        selected_choice_name = self.final_data.selected_element()
        if selected_choice_name:
            choice_condition = self.menu_conditions.get_val()
            if choice_condition == 'Choice':
                final_values_to_add = []
            else:
                final_values_to_add = [choice_condition]
            for field in self.selected_filter_fields:
                if self.fields_list[field].get_val():
                    final_values_to_add.append(self.fields_list[field].get_val())
            self.final_data.add_data_to_display(final_values_to_add, selected_choice_name)
    def menu_slots(self, slots_val):
        # slots_val = self.menu_main_options.get_val()
        if slots_val == 'MaxMenuSlots':
            self.maxmenu_amount.show()
        else:
            self.maxmenu_amount.hide()
    def menu_choice_options(self, selected_option):
        # selected_option = self.menu_choice_list.get_val()
        if selected_option not in self.prev_options:
            self.clear_fields()
            self.prev_options = selected_option
            if selected_option in 'FinalOption HideOptionOnRequirementFail InverseRequirement':
                self.prev_options = 'FinalOption HideOptionOnRequirementFail InverseRequirement'
                self.selected_filter_fields = []
            elif selected_option in 'RequiresMinimumProgress RequiresLessProgress RequiresEnergy RequiresVirility':
                self.prev_options = 'RequiresMinimumProgress RequiresLessProgress RequiresEnergy RequiresVirility'
                self.setup_int()
            elif selected_option in 'RequiresFetishLevelEqualOrGreater RequiresFetishLevelEqualOrLess RequiresStat':
                self.setup_list_int()
            elif selected_option in 'RequiresItem RequiresItemEquipped RequiresPerk RequiresSkill':
                self.setup_multi()
            elif selected_option in 'RequiresMinimumProgressFromEvent RequiresLessProgressFromEvent':
                self.prev_options = 'RequiresMinimumProgressFromEvent RequiresLessProgressFromEvent'
                self.setup_int_multi()
            elif selected_option in 'RequiresTime':
                self.setup_list()
            elif selected_option == 'RequiresChoice':
                self.set_up_choice('current')
            elif selected_option == 'RequiresChoiceFromEvent':
                self.set_up_choice('event')
            else:
                # self.prev_options = 'EventJump ThenJumpToScene' - thise should be together, not separate
                self.prev_options = 'EventJump'
                self.setup_scene()
    def clear_fields(self):
        for field in self.fields_list:
            self.fields_list[field].hide()
            self.fields_list[field].clear_val()
    def setup_int(self):
        self.fields_list['int'].show()
        # self.fields_list['int'].grid(row=self.options_row, column=2)
        self.selected_filter_fields = ['int']
    def setup_list_int(self):
        self.fields_list['list1'].show()
        # self.fields_list['list1'].grid(row=self.options_row, column=2)
        data_to_load = self.menu_conditions.get_val()
        if 'Stat' in data_to_load:
            # values = GlobalVariables.Glob_Var.game_hard_data
            values = otherFunctions.getListOptions(['game-core stats-simple'], 'single')
        else:
            values = otherFunctions.getListOptions(['Fetishes'], 'single')
            # values = otherFunctions.getListOptions(['Fetishes'], 'single')
        self.fields_list['list1'].reload_options(values)
        self.fields_list['int'].show()
        # self.fields_list['int'].grid(row=self.options_row, column=3)
        self.selected_filter_fields = ['list1', 'int']
    def setup_list(self):
        self.fields_list['list1'].show()
        # self.fields_list['list1'].grid(row=self.options_row, column=2)
        self.fields_list['list1'].reload_options(["Day", "Night", "DayFaked", "DayTrue", "NightFaked", "NightTrue", "Morning", "Noon", "Afternoon", "Dusk", "Evening", "Midnight"])
        self.selected_filter_fields = ['list1']
    def setup_multi(self):
        self.fields_list['multi'].show()
        data_to_load = self.menu_conditions.get_val()
        if 'Item' in data_to_load:
            data_to_load = 'Items'
        elif 'Perk' in data_to_load:
            data_to_load = 'Perks'
        elif 'Skill' in data_to_load:
            data_to_load = 'Skills'
        self.fields_list['multi'].selection_type = data_to_load
        self.treeview_main_game_items.disconnect_multilist()
        self.selected_filter_fields = ['multi']
    def setup_int_multi(self):
        self.fields_list['multi'].show()
        self.fields_list['int'].show()
        self.fields_list['multi'].selection_type = 'Events'
        self.fields_list['multi'].label_custom.setText('Events')
        self.selected_filter_fields = ['multi', 'int']
    def setup_scene(self):
        data_to_load = self.menu_conditions.get_val()
        if data_to_load == 'EventJump':
            # if eventjump, need to set first multilist display for events.
            # second multi could display scenes. either from current event - "choice" options, or from selected event from eventjump - first multi
            values = ['Events']

            self.fields_list['multi'].label_custom.setText('Events')
            self.fields_list['multi'].selection_type = 'Events'
            self.fields_list['multi'].show()
            # self.fields_list['multi'].var.trace_id = self.fields_list['multi'].var.trace('w', lambda *args: self.special_event_jumping_load_scenes_to_list(''))
            self.fields_list['multi'].final_data.function_on_modify(self.special_event_jumping_load_scenes_to_list)
            self.fields_list['check'].show()
            self.selected_filter_fields = ['multi', 'check']
        #     Else below never happens, since this reacts to option value, which is only EventText. Scene is a checkbox
        # else:
        #     self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
        #     # values = ['Scenes']
        #     # self.fields_list['multi2'].update_list(values)
        #     self.fields_list['multi2'].show()
        #     # self.fields_list['multi2'].grid(row=self.options_row, column=2)
        #     self.selected_filter_fields = ['multi2']
        # # values = otherFunctions.getListOptions(['currentmod-Events'], 'multi')
        # # self.fields_list['multi'].update_list(values)

        # self.fields_list['multi'].grid(row=self.options_row, column=3)
    def set_up_scene_field(self):
        flag_trigger = self.fields_list['check'].get_val()
        if flag_trigger:
            self.fields_list['multi2'].show()
            # self.fields_list['multi2'].grid(row=1, column=5)
            self.selected_filter_fields.append('multi2')
        else:
            self.fields_list['multi2'].hide()
            if len(self.selected_filter_fields) == 5:
                self.selected_filter_fields.pop()
    def set_up_choice(self, with_event):
        self.selected_filter_fields = ['list1', 'list2']
        choice_startup = 'current'
        if with_event == 'event':
            self.fields_list['multi'].selection_type = 'Events'
            self.fields_list['multi'].label_custom.setText('Events')
            self.fields_list['multi'].show()
            self.selected_filter_fields.insert(0, 'multi')
            choice_startup = 'Event'

        self.fields_list['list1'].show()
        self.fields_list['list2'].show()
        self.Special_Set_Up_Choices_Fields(choice_startup)

    def Special_Set_Up_Choices_Fields(self, function_name):
        if 'Event' in function_name:
            """if event, link first multi field with function to find choices based on event"""
            # self.fields_list['list1'].clear_val()
            # otherFunctions.duplicate_treeview(GlobalVariables.list_elementlists[1].treeview,
            #                                   self.function_fields_list[0].tree_options_choose.treeview,
            #                                   destination_leaf='mod-Events')
            # self.fields_list['multi'].var.trace_id =\
            #     self.fields_list['multi'].var.trace("w", lambda *args, arg1='true': self.special_set_up_choices_1(arg1))
            self.fields_list['multi'].final_data.function_on_modify(self.special_set_up_choices_1)
        else:
            """if not event, then return choices from current scene"""

            event_name = SimpleFields.mod_temp_data.current_editing_event
            self.prev_options = event_name
            self.special_set_up_choices_1()
        """first field should be choice number, second field should be choice text"""
        # # self.function_fields_list[field_order].var.trace_add("write", lambda order: self.Special_Set_Up_Choices_2(field_order))
        self.fields_list['list1'].currentTextChanged.connect(self.Special_Set_Up_Choices_2)
        # self.fields_list['list1'].var.trace_id =\
        #     self.fields_list['list1'].var.trace("w", lambda *args: self.Special_Set_Up_Choices_2())
        # self.fields_list['list1'].delete_place = 'gate'
        # self.fields_list['list2'].delete_place = 'choice'
        # self.fields_list['list2'].choice_no_field = self.fields_list['list1']
        # self.fields_list['list2'].currentTextChanged.connect(self.Special_Set_Up_Choices_2_1)
        # self.fields_list['list2'].var.trace_id = self.fields_list[
        #     'list2'].var.trace("w", lambda *args: self.Special_Set_Up_Choices_2_1())

        # old version, when it searched on the spot
        # choices_list = []
        # if 'Event' in function_name:
        #     return
        # else:
        #     if self.event == 'EventText':
        #         element = 'Events'
        #     else:
        #         element = 'Monsters'
        #     list_of__dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
        #     for dictionary_scene in list_of__dictionary_scenes:
        #         theText = dictionary_scene['theScene']
        #         index = 0
        #         for texts in theText:
        #             if len(texts) == 9:
        #                 if texts == 'SetChoice':
        #                     choices_list.append(theText[index+1])
        #             index += 1
        #     self.function_fields_list[1].reload_options(choices_list)

    def special_set_up_choices_1(self):
        if 'multi' in self.selected_filter_fields:
            """this means choices should be set by event name in first field"""
            event_name = self.fields_list['multi'].get_val()
            self.prev_options = event_name
        """first field should be choice number, second field should be choice text"""
        choice_list = SimpleFields.mod_temp_data.get_choices(get_val='gate', event_name=self.prev_options)
        self.fields_list['list1'].reload_options(choice_list)
        # self.fields_list['list1'].event_name = event_name
        choice_list = SimpleFields.mod_temp_data.get_all_choices_text(event_name=self.prev_options)
        self.fields_list['list2'].reload_options(choice_list)
        # self.fields_list['list2'].event_name = event_name

    def Special_Set_Up_Choices_2(self, choice_gate):
        """get choice number and load choices text"""
        # choice_text = self.fields_list['list2'].get_val()
        # if not choice_text:
        # choice_gate = choice_no
        # choice_gate = self.fields_list['list1'].get_val()
        if choice_gate:
            choices_list = SimpleFields.mod_temp_data.get_choices(get_val=choice_gate, event_name=self.prev_options)
            self.fields_list['list2'].reload_options(choices_list)

    # def Special_Set_Up_Choices_2_1(self):
    #     """get choice text and load its number"""
    #     choice_no = self.fields_list['list1'].get_val()
    #     if not choice_no:
    #         choice_text = self.fields_list['list2'].get_val()
    #         if choice_text:
    #             choices_no = SimpleFields.mod_temp_data.get_gates(choice=choice_text, event_name=self.prev_options)
    #             self.fields_list['list1'].set_val(choices_no)

        return
    def special_event_jumping_load_scenes_to_list(self, event, flag_current_event=False):
        self.fields_list['multi2'].clear_val()
        if flag_current_event:
            self.treeview_main_game_items.scene_source = 'current'
            # event_name = GlobalVariables.templates['Events'].frame_fields['name'].get_val()
            # list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates['Events'].frame_fields['EventText'].get_val()
            # for scene in list_of_dictionary_scenes:
            #     # self.fields_list['multi2'].tree_options_choose.treeview.insert('mod-Scenes', 'end', text=scene['NameOfScene'])
            #     self.fields_list['multi2'].tree_options_choose.treeview.insert('', 'end', text=scene['NameOfScene'])
            # return
        # selected_item = self.fields_list['multi'].tree_options_choose.treeview.selection()
        selected_event = self.fields_list['multi'].get_val()
        if selected_event:
            self.treeview_main_game_items.scene_source = selected_event
            # self.fields_list['multi2'].clear_val('all')
            # selected_event = self.fields_list['multi'].tree_options_choose.treeview.item(selected_item)['text']
            # scenes_list = GlobalVariables.current_mod['Events'][selected_event]['EventText']
            # temp_scene_names = []
            # for scene in scenes_list:
            #     self.fields_list['multi2'].tree_options_choose.treeview.insert('', 'end',
            #                                                                      text=scene['NameOfScene'])
            # temp_scene_names.append(scene['NameOfScene'])
        # self.function_fields_list[2].treeview_optionstochoose.treeview.insert('', 'end',values=temp_scene_names)
#
#
class Choices:
    def __init__(self, event_field=None):
        self.field_choice_no = SimpleFields.InputList(field_name='Choice')
        self.field_choice_no.field.setMaximumWidth(60)
        self.field_choice_text = SimpleFields.InputList(field_name='Text')
        self.event_source = ''
        if event_field:
            self.event_source_field = event_field
            self.event_source_field.final_data.function_on_modify(self.set_up_event_source)
        else:
            """what if creating event? then inputfilename might be empty"""
            self.event_source = SimpleFields.mod_temp_data.current_editing_event
            self.set_up_event_source()
        self.field_choice_no.field.currentTextChanged.connect(self.set_up_choices_text)
        self.field_choice_no.delete_place = 'gate'
        self.field_choice_text.delete_place = 'choice'
        self.field_choice_text.choice_no_field = self.field_choice_no
        # self.field_choice_text.var.trace_id = self.field_choice_text.var.trace("w", lambda *args: self.set_up_choices_no())
    def set_up_event_source(self):
        if not self.event_source:
            self.event_source = self.event_source_field.get_val()
        """first field should be choice number, second field should be choice text"""
        choice_list = SimpleFields.mod_temp_data.get_choices(get_val='gate', event_name=self.event_source)
        self.field_choice_no.reload_options(choice_list)
        # self.field_choice_no.event_name = event_name
        choice_list = SimpleFields.mod_temp_data.get_all_choices_text(event_name=self.event_source)
        self.field_choice_text.reload_options(choice_list)
        # self.field_choice_text.event_name = event_name

    def set_up_choices_text(self):
        """get choice number and load choices text"""
        choice_gate = self.field_choice_no.get_val()
        if choice_gate:
            choices_list = SimpleFields.mod_temp_data.get_choices(get_val=choice_gate,
                                                                  event_name=self.event_source)
            self.field_choice_text.limit_options(choices_list)

    def set_up_choices_no(self):
        """get choice text and load its number"""
        choice_text = self.field_choice_text.get_val()
        if choice_text:
            choices_no = SimpleFields.mod_temp_data.get_gates(choice=choice_text,
                                                              event_name=self.event_source)
            self.field_choice_no.set_val(choices_no)
    def set_up_widget(self, outside_layout):
        outside_layout.addWidget(self.field_choice_no.field)
        outside_layout.addWidget(self.field_choice_text.field)
        # self.frame_fields.destroy()
#
#
# class CombatEncounter:
#     def __init__(self, master_frame):
#         """first, menu options - MaxMenuSlots and ShuffleMenu"""
#         self.frame_for_fields = tk.Frame(master=master_frame)
#         button_add_choice_check = tk.Button(self.frame_for_fields, text='Add condition', command=self.add_condition)
#         button_add_choice_check.grid(row=1, column=0)
#         self.menu_main_options = SimpleFields.SingleList(self.frame_for_fields, 'Options', '', 'L', ['blank', 'NoRunning', 'RunningWontSkipEvent', 'SetBGOnRun', 'DenyInventory'])
#         self.menu_main_options.set_val('blank')
#         # lamba problem ') takes 0 positional arguments but 3 were given' as always
#         self.menu_main_options.var.trace_id = self.menu_main_options.var.trace('w', lambda *args: self.menu_background())
#         # trace above with funkc to display maxmenuslots
#         self.menu_main_options.grid(row=0, column=1)
#         self.background_file = SimpleFields.FileField(self.frame_for_fields, 'Background', '', 'L')
#         """now make creator of menu choices."""
#         choices_list = ['Monster', 'ApplyStance', 'Restrainer']
#         self.menu_choice_list = SimpleFields.SingleList(self.frame_for_fields, 'Conditions', '', 'L', choices_list)
#         """trace var to def that controls fields to display and hide and load choices"""
#         self.menu_choice_list.var.trace_id = self.menu_choice_list.var.trace('w', lambda *args: self.menu_choice_options())
#         self.menu_choice_list.grid(row=1, column=1)
#         """these fields are what will be used"""
#         field_multi = SceneMultiList(self.frame_for_fields, list_path=['placeholder'], field_options=['single_item'])
#         field_multi.update_label('Monsters')
#         field_multi2 = SceneMultiList(self.frame_for_fields, list_path=['placeholder'], field_options=['single_item'])
#         field_multi2.update_label('Stances')
#         self.fields_list = {'multi': field_multi, 'multi2': field_multi2}
#         """here is where all is displayed"""
#         self.data_display = SceneElementsList(self.frame_for_fields, 2, 0, 'Encounters', 6)
#
#         self.prev_options = ''
#         self.options_row = 1
#         self.selected_filter_fields = []
#     def set_val(self, values_to_set_list):
#         """should accept list of values"""
#         """first check for main menu options"""
#         length_of_list = len(values_to_set_list)
#         start_checking = 0
#         if values_to_set_list[start_checking] in 'NoRunning RunningWontSkipEvent SetBGOnRun DenyInventory':
#             value = values_to_set_list[start_checking]
#             if value == 'SetBGOnRun':
#                 start_checking = 2
#                 self.menu_main_options.set_val('SetBGOnRun')
#                 self.background_file.set_val(values_to_set_list[1])
#             elif value == 'NoRunning RunningWontSkipEvent DenyInventory':
#                 self.menu_main_options.set_val(value)
#                 start_checking = 1
#         # choices_no = 1
#         # temp_list = []
#         skip_no = 0
#         """now start checking for all conditional choices"""
#         for index in range(start_checking, length_of_list):
#             if skip_no >= 0:
#                 skip_no -= 1
#                 continue
#             selected_option = values_to_set_list[index]
#             # temp_list.append(selected_option)
#             if selected_option in 'Restrainer':
#                 self.data_display.add_leaves_simple(current_leaf, [selected_option])
#                 continue
#             elif selected_option in 'ApplyStance':
#                 self.data_display.add_leaves_simple(current_leaf, [selected_option, values_to_set_list[index + 1]])
#                 # temp_list.append(values_to_set_list[index + 1])
#                 skip_no = 1
#             else:
#                 current_leaf = self.data_display.add_leaf('', 'monster' + str(index), selected_option)
#                 # self.data_display.add_branch('Choice ' + str(choices_no), temp_list, update_flag=False)
#                 # temp_list.clear()
#                 # choices_no += 1
#                 # data_to_load.append({str(len(data_to_load)+1): temp_list})
#
#         return
#     def get_val(self):
#         return_values = []
#         """first get main options, then what was added in the data display"""
#         main_options = self.menu_main_options.get_val()
#         if main_options != 'blank':
#             return_values.append(main_options)
#             if main_options == 'SetBGOnRun':
#                 return_values.append(self.background_file.get_val())
#         displayed_data_list = self.data_display.gather_data()
#         for choice in displayed_data_list:
#             for choice_element in choice:
#                 choice_elements_list = choice[choice_element]
#                 return_values += choice_elements_list
#         return return_values
#     def clear_val(self):
#         self.pack_forget()
#     def destroy(self):
#         self.frame_for_fields.destroy()
#     def pack(self):
#         self.frame_for_fields.pack(side=tk.LEFT)
#     def pack_forget(self):
#         self.frame_for_fields.pack_forget()
#     def add_condition(self):
#         """if selected monster, add new leaf with that monster as branch. otherwise, add to selected item or to last leaf"""
#         choice_condition = self.menu_choice_list.get_val()
#         if choice_condition == 'Monster':
#             current_leaves = self.data_display.treeview.get_children()
#             if len(current_leaves) == 12:
#                 messagebox.showwarning("Monster Limit", "Too many enemies. Cannot add more")
#                 return
#             new_branch = self.fields_list[self.selected_filter_fields[0]].get_val()
#             self.data_display.add_leaves_simple('', [new_branch])
#             current_leaves = self.data_display.treeview.get_children()
#             self.data_display.add_leaves_simple(current_leaves[-1], [new_branch])
#             return
#         elif choice_condition == 'Restrainer':
#             value_to_add = ['Restrainer']
#         elif choice_condition == 'ApplyStance':
#             value_to_add = ['ApplyStance', self.fields_list[self.selected_filter_fields[0]].get_val()]
#         else:
#             return
#         """now to add in selected branch or last branch"""
#         selected_choice_code = self.data_display.selected_item(value='code')
#         if selected_choice_code:
#             selected_choice_parent = self.data_display.treeview.parent(selected_choice_code)
#             if selected_choice_parent:
#                 self.data_display.add_leaves_simple(selected_choice_parent, value_to_add)
#             else:
#                 self.data_display.add_leaves_simple(selected_choice_code, value_to_add)
#         else:
#             current_leaves = self.data_display.treeview.get_children()
#             self.data_display.add_leaves_simple(current_leaves[-1], value_to_add)
#
#     def menu_background(self):
#         val = self.menu_main_options.get_val()
#         if val == 'SetBGOnRun':
#             self.background_file.grid(row=0, column=2)
#         else:
#             self.background_file.grid_forget()
#     def menu_choice_options(self):
#         # 'Monster', 'ApplyStance', 'Restrainer']
#         selected_option = self.menu_choice_list.get_val()
#         if selected_option not in self.prev_options:
#             self.clear_fields()
#             if selected_option in 'Restrainer':
#                 self.prev_options = 'Restrainer'
#                 self.selected_filter_fields = []
#                 return
#             elif selected_option in 'ApplyStance':
#                 self.prev_options = 'ApplyStance'
#                 self.setup_multi()
#             elif selected_option in 'Monster':
#                 self.prev_options = 'Monster'
#                 self.setup_multi()
#             else:
#                 # self.prev_options = 'EventJump ThenJumpToScene' - thise should be together, not separate
#                 self.prev_options = 'test'
#     def clear_fields(self):
#         for field in self.fields_list:
#             self.fields_list[field].grid_forget()
#             self.fields_list[field].clear_val()
#         self.fields_list['multi'].var.trace_id = ''
#         return
#     def setup_multi(self):
#         self.fields_list['multi'].grid(row=self.options_row, column=2)
#         data_to_load = self.menu_choice_list.get_val()
#         if 'Monster' in data_to_load:
#             values = ['currentmod-Monsters', 'main/Monsters']
#             self.fields_list['multi'].update_label(values[0][11:])
#         elif 'Stance' in data_to_load:
#             values = ['Stances']
#             self.fields_list['multi'].update_label(values)
#         self.fields_list['multi'].update_list(values)
#         self.selected_filter_fields = ['multi']
#
class FunctionTests(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Events')
        # Dialog.resize(310, 299)
        # self.widget.setGeometry(QtCore.QRect(0, 10, 301, 281))
        self.setObjectName("FunctionWin")
        self.resize(900, 500)
        main_lay = QtWidgets.QVBoxLayout()
        self.setLayout(main_lay)
        self.temp = SwapLine_Field(main_lay)
        self.button_test = QtWidgets.QPushButton(text='test closing')
        self.button_test.clicked.connect(self.test)
        main_lay.addWidget(self.button_test)

    def test(self):
        self.temp.get_val()
        # self.temp.field_text.label_custom.change_position('C')


class SwapLine_Field:
    def __init__(self, main_layout=None, main_game_items=None):
        # TODO for some reason, when this is created, other function after it are created at the bottom of main layout instead of the top
        """main idea:
        first line - dropdown with options
        second line - will create fields according to above. mostly int and text, sometime input with staff from tree
        last line - element tree with columns, all editable"""

        # "Options": {"type": "singlelist",
        #             "choices": ["Random", "Stat", "Arousal", "MaxArousal", "Energy", "MaxEnergy", "Virility",
        #                         "HasFetish", "HasFetishLevelEqualOrGreater", "Perk", "EncounterSize", "Item", "Eros",
        #                         "IfTimeIs", "Progress", "OtherEventsProgress", "Choice", "OtherEventsChoice"]}

        self.main_layout = main_layout
        self.treeview_main_game_items = main_game_items
        # options = {'choices': ["","Random", "Stat", "Arousal", "MaxArousal", "Energy", "MaxEnergy", "Virility",
        #                         "HasFetish", "HasFetishLevelEqualOrGreater", "Perk", "EncounterSize", "Item", "Eros",
        #                         "IfTimeIs", "Progress", "OtherEventsProgress", "Choice", "OtherEventsChoice"]
        #            }
        # self.list_options = SimpleFields.SingleList(field_data=options)
        # self.list_options.set_up_widget(self.main_layout)
        # self.list_options.currentTextChanged.connect(self.prepare_line_fields)
        self.list_fields_not_going_to_treeview = []
        """in case options has additional options, like event for progress, which should not repeat for each text"""
        self.field_widget_for_easy_remove = QtWidgets.QWidget()
        self.created_fields_layout = QtWidgets.QHBoxLayout()
        self.created_fields_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.field_widget_for_easy_remove.setLayout(self.created_fields_layout)
        self.main_layout.addWidget(self.field_widget_for_easy_remove)
        self.field_text = SimpleFields.SimpleEntry(None, 'Text', label_pos='V')
        self.field_text.label_custom.change_position('C')
        self.field_text.center()
        self.field_text.set_up_widget(self.main_layout)
        self.field_text.returnPressed.connect(self.add_multi_value)
        # self.button_add = tk.Button(master, text='Add', command=self.add_multi_value)
        # self.button_add.grid(row=10, column=0)
        # self.button_clear = tk.Button(master, text='Delete', command=self.delete_multi_value)
        # self.button_clear.grid(row=10, column=1)
        self.data_tree = SimpleFields.ElementsList(None,folders=True, all_edit=True)
        self.data_tree.set_up_widget(self.main_layout)
        self.data_tree.setWordWrap(True)
        self.fields_list = []
        self.changed_selection = 'none'

    def add_multi_value(self):
        title = ''
        for field in self.fields_list:
            title += field.get_val() + '   '
        title = title.rstrip()
        text = self.field_text.get_val()
        self.data_tree.add_data({title: text})
        self.data_tree.change_row_height(40)
        self.data_tree.expandAll()

    def deselect_row(self):
        self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])
    def prepare_line_fields(self, prepare_options):
        # probably useless, as for example, from fetish to fetish level will not update
        # if prepare_options in self.changed_selection:
        #     return
        # else:
        #     self.changed_selection = prepare_options
        # self.treeview_main_game_items.disconnect_multilist()
        for field in self.fields_list:
            field.destroy()
        self.fields_list = []
        for field in self.list_fields_not_going_to_treeview:
            field.destroy()
        self.list_fields_not_going_to_treeview = []
        self.data_tree.clear_tree()
        if prepare_options == 'Stat':
            field_atr1 = SimpleFields.SingleList(label_text='Core Attribute',
                                                 field_data={'choices': ["Power", "Technique", "Willpower", "Allure",
                                                                         "Intelligence", "Luck"]}, label_pos='V')
            field_atr1.set_up_widget(self.created_fields_layout)
            self.fields_list.append(field_atr1)
            field_atr2 = SimpleFields.NumericEntry(None)
            self.fields_list.append(field_atr2)
            field_atr2.set_up_widget(self.created_fields_layout)
        elif prepare_options in "Arousal MaxArousal Energy MaxEnergy Virility EncounterSize Eros Progress":
            field_atr1 = SimpleFields.NumericEntry(None)
            field_atr1.set_up_widget(self.created_fields_layout)
            self.fields_list.append(field_atr1)
            self.changed_selection = "Arousal MaxArousal Energy MaxEnergy Virility EncounterSize Eros Progress"
        elif prepare_options == 'HasFetish':
            field_atr1 = SimpleFields.SingleList(label_text='Fetishes', label_pos='V',
                                                 field_data={'choices': ["Fetishes"]})
            field_atr1.set_up_widget(self.created_fields_layout)
            self.fields_list.append(field_atr1)
        elif prepare_options == 'HasFetishLevelEqualOrGreater':
            field_atr1 = SimpleFields.SingleList(label_text='Fetishes', label_pos='V',
                                                 field_data={'choices': ["Fetishes"]})
            field_atr1.set_up_widget(self.created_fields_layout)
            self.list_fields_not_going_to_treeview.append(field_atr1)
            # self.fields_list.append(field_atr1)
            field_atr2 = SimpleFields.NumericEntry(None)
            self.fields_list.append(field_atr2)
            field_atr2.set_up_widget(self.created_fields_layout)
        elif prepare_options == 'Perk':
            field_atr1 = SimpleFields.MultiListDisplay(None, 'Perks',
                                                       field_data={'choices': ["Perks"], 'options': ["single_item", "search"]},
                                                       main_data_treeview=self.treeview_main_game_items)
            self.fields_list.append(field_atr1)
            field_atr1.set_up_widget(self.created_fields_layout)
        elif prepare_options == 'Item':
            field_atr1 = SimpleFields.MultiListDisplay(None, 'Items',
                                                       field_data={'choices': ["Items"], 'options': ["single_item", "search"]},
                                                       main_data_treeview=self.treeview_main_game_items)
            self.fields_list.append(field_atr1)
            field_atr1.set_up_widget(self.created_fields_layout)
        elif prepare_options == 'IfTimeIs':
            field_atr1 = SimpleFields.SingleList(label_text='Time of day', label_pos='V',
                                                 field_data={'choices': ["Day", "Night"]})
            self.fields_list.append(field_atr1)
            field_atr1.set_up_widget(self.created_fields_layout)
        elif prepare_options == 'OtherEventsProgress':

            field_atr1 = SimpleFields.MultiListDisplay(None, 'Events',
                                                       field_data={'choices': ["Events"], 'options': ["single_item", "search"]},
                                                       main_data_treeview=self.treeview_main_game_items)
            # field_atr1 = SceneMultiList(self.fields_master, list_path=["currentmod-Events"], field_options=["single_item", "search"])
            # field_atr1.update_label('Events')
            # field_atr1 = SimpleFields.MultiList(self.fields_master, field_name='Events', label_position='U',
            #                                     list_path=["currentmod-Events"], field_options=["single_item", "search"])
            self.list_fields_not_going_to_treeview.append(field_atr1)
            field_atr1.set_up_widget(self.created_fields_layout)
            field_atr2 = SimpleFields.NumericEntry(None)
            self.fields_list.append(field_atr2)
            field_atr2.set_up_widget(self.created_fields_layout)
        elif prepare_options == 'Choice':
            field_list = Choices()
            field_list.set_up_widget(self.created_fields_layout)
            self.fields_list.append(field_list.field_choice_no)
            self.fields_list.append(field_list.field_choice_text)
        #     TODO this is not working for some reason. when event is selected, choice fields are not updated.
        elif prepare_options == 'OtherEventsChoice':
            field_atr1 = SimpleFields.MultiListDisplay(None, 'Event',
                                                       field_data={'choices': ["Events"], 'options': ["single_item", "search"]},
                                                       main_data_treeview=self.treeview_main_game_items)
            self.list_fields_not_going_to_treeview.append(field_atr1)
            field_atr1.set_up_widget(self.created_fields_layout)
            field_list = Choices(field_atr1)
            field_list.set_up_widget(self.created_fields_layout)
            self.fields_list.append(field_list.field_choice_no)
            self.fields_list.append(field_list.field_choice_text)

    def get_val(self):
        templist = []
        for additiona_field in self.list_fields_not_going_to_treeview:
            templist.append(additiona_field.get_val())
        swap_attributes = self.data_tree.get_data()
        for dict_in_list in swap_attributes:
            for keyV in dict_in_list:
                templist.append(keyV)
                templist.append(dict_in_list[keyV][0])
        return templist
    def clear_val(self):
        self.data_tree.clear_tree()
    def destroy(self):
        self.main_layout.removeWidget(self.field_text)
        self.field_text.destroy()
        self.main_layout.removeWidget(self.field_widget_for_easy_remove)
        self.field_widget_for_easy_remove.deleteLater()
        self.main_layout.removeWidget(self.data_tree)
        self.data_tree.deleteLater()
        # self.main_layout.removeWidget(self.list_options)
        # self.list_options.destroy()

class Special_Options(QtWidgets.QWidget):
    # TODO
    """functions like MENU, SWAPLINE and now i see that STATCHECK, got options with various values to select.
    Some if not most of those options seems different, but are actually the same. So instead of having
    different code(menu has different way to working for that), I've decided to create seperate class, that should
    work on those options itself."""
    def __init__(self):
        super().__init__()
        # options = {'choices': ["","Random", "Stat", "Arousal", "MaxArousal", "Energy", "MaxEnergy", "Virility",
        #                         "HasFetish", "HasFetishLevelEqualOrGreater", "Perk", "EncounterSize", "Item", "Eros",
        #                         "IfTimeIs", "Progress", "OtherEventsProgress", "Choice", "OtherEventsChoice"]
        #            }
        # self.list_options = SimpleFields.SingleList(field_data=options)
        # self.list_options.set_up_widget(self.main_layout)
        # self.list_options.currentTextChanged.connect(self.prepare_line_fields)
        """in case options has additional options, like event for progress, which should not repeat for each text"""
        self.field_widget_for_easy_remove = QtWidgets.QWidget()
        self.created_fields_layout = QtWidgets.QHBoxLayout()
        self.created_fields_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.field_widget_for_easy_remove.setLayout(self.created_fields_layout)
        self.main_layout.addWidget(self.field_widget_for_easy_remove)


class main_game_for_functions_treeview:
    """fused with maine game items treeview."""
    def __init__(self, master=None, field_name=None):
        # super().__init__(master=master, label=field_name, tooltip=tooltip_text, label_pos=label_position)
        """similar to mainGameItems treeview, but instead of always on, only appear when preparing functions that
        needs some game items. And then, instead of limiting access, display only what should be available.
        So load all game items into separate variable, when user click prepare, pass info what should be prepared"""
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.title = field_name
        self.type = 'main_multilist'
        self.edit_flag = False
        select_mode = 'extended'
        self.data_for_display = []
        # self.field_frame = master
        """ this contains necessary mod and game items. so Always display treeview and need
         to be updated when adding new mod items."""
        self.main_data = SimpleFields.ElementsList(master, 'Available element', search_field=True,
                                      folders=True)
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

        """scene source is for functions jump to scene. if its 'current', get data from global-template-field.
        if something else, it should be event name, get also from global-events-search for scenes"""
        self.scene_source = ''

    def set_up_widget(self, outside_layout, if_grid=None):
        if if_grid:
            outside_layout.addWidget(self.label_info, 7, 0, 1, 1)
            outside_layout.addWidget(self.main_data, 8, 0, 1, 1)
        else:
            outside_layout.addLayout(self.custom_layout)

    def set_up_data_for_display(self, data_to_display=list):
        """Another approach. Previously it was {MOD:events and stuff, Adventure, Items, etc}
        New approach {Adventure:files from mods, Game:game files}"""
        """take out first element - mod data"""
        mod_elements = data_to_display.pop(0)
        """data to display got all possible elements types"""
        for elements in data_to_display:
            """take element name - Events"""
            element_name = list(elements.keys())[0]
            """copy in seperate var in branch 'Game'"""
            temp_game_element = {'Game': elements[element_name]}
            """search for elements Events in Mod data"""
            temp_mod_element = []
            if not isinstance(mod_elements, str):
                for element in mod_elements['MOD']:
                    if list(element.keys())[0] == element_name:
                        temp_mod_element = element[element_name]
                        break
            """first add elements from MOD"""
            elements[element_name] = temp_mod_element
            # for element in temp_mod_element:
            #     elements[element_name].append(element)
            """add Game elements at the end"""
            elements[element_name].append(temp_game_element)
        self.data_for_display = data_to_display


    def connect_multilist(self, multilist):
        if self.connected_multilist == multilist or multilist == self:
            return
        self.connected_multilist = multilist
        self.main_data.clear_tree()
        self.filter_options(multilist.selection_type)
        # print(multilist.selection_type)
    def disconnect_multilist(self):
        # might not be needed
        # print('disconnected')
        if self.connected_multilist:
            self.connected_multilist = None
            # self.label_info.clicked.disconnect()
            # self.main_data.restore_deleted()
            self.filter_options([])

    def filter_options(self, filter):
        """filter should be list of values"""
        # self.main_data.clear_tree()
        """here add scenes. this might change while making events, so it needs to reload each time."""
        """and the rest of stuff"""
        if 'scenes' in filter:
            """if current, need to load from field in templates"""
            if self.scene_source == 'current' or 'current' in filter:
                # if self.connected_multilist.selection_type:
                #     if self.connected_multilist.selection_type == 'EventText':
                #         element = 'Events'
                #     else:
                #         element = 'Monsters'
                list_of_dictionary_scenes = GlobalVariables.Glob_Var.access_templates['Events'].frame_fields['EventText'].get_val()
                # list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates[element].frame_fields[self.connected_multilist.selection_type].get_val()
                scene_names = []
                for scene in list_of_dictionary_scenes:
                    scene_names.append(scene['NameOfScene'])
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

        else:
            for element in self.data_for_display:
                if isinstance(element, str):
                    value_to_check = element
                else:
                    value_to_check = list(element.keys())[0]
                if value_to_check in filter:
                    self.main_data.add_data(element[value_to_check])
    def filter_options_origin(self, filter=None):
        root_elements_no = self.main_data.tree_model.rowCount()
        for idx in range(1, root_elements_no):
            block_element = self.main_data.tree_model.item(idx)
            if block_element.text() in filter:
                if block_element.flags() & QtCore.Qt.ItemNeverHasChildren:
                    block_element.setFlags(block_element.flags() & ~QtCore.Qt.ItemNeverHasChildren)
            else:
                block_element.setFlags(block_element.flags() | QtCore.Qt.ItemNeverHasChildren)
        # maindata treemodel is changed to sorting model to be able to filter results, so it should emit that model
        # self.main_data.tree_model.layoutChanged.emit()
        self.main_data.sorting.layoutChanged.emit()
        # this is mine, with use of selecting element in treeview and deleting with backup selected elements
        # if filter:
        #     self.main_data.select_element(filter, inverse_selection=True)
        #     self.main_data.delete_with_backup()
    def add_item_to_multilist(self, element_index):
        """elementtree here is with search, which have proxy model. Selected element maps data and returns correct
        standardItem but only for first column. I dont know how to get it not from double click, so here it
        checks selected element, which is correct, then gets data from clicked index """
        selected_item = self.main_data.selected_element()
        if selected_item and self.connected_multilist:
            if not selected_item[0].child(0, 0):
                """this was used in case of several different elements. for example, items and skills, to put
                in correct fields.But here if possible, data will be in top level, so there is no parent"""
                # selected_item_type = self.main_data.find_root_parent(selected_item)
                # selection_type = self.connected_multilist.selection_type
                # """if there is a parent, check if correct field is selected. If no parent, there is 1 field type only"""
                # if selected_item_type:
                #     if selected_item_type.text() in selection_type:
                #         self.connected_multilist.set_val(selected_item.text())
                # else:
                self.connected_multilist.set_val(element_index.data())
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
    # def add_main_game_items(self):
    #     """instead to treeview, add items to variable. Then when preparing function, load correct items to display"""
    #     # self.main_data.add_data(data='MOD')
    #     main_game_items = GlobalVariables.Glob_Var.main_game_items
    #     for element in main_game_items:
    #         if main_game_items[element]:
    #             if element == 'Fetishes':
    #                 temp_dict = {'Fetish': list(main_game_items[element]['Fetish'].keys()),
    #                              'Addiction': list(main_game_items[element]['Addiction'].keys())}
    #
    #             else:
    #                 temp_dict = {element: main_game_items[element]['path']}
    #             # self.main_data.add_data(data=[temp_dict])
    #             self.data_for_display.append(temp_dict)
    #     """for main multilist, it works different. it is created one, loads main game items"""
    #     # for element in GlobalVariables.Glob_Var.lineTriggers:
    #     #     temp_dict = {element:GlobalVariables.Glob_Var.lineTriggers[element]['path']}
    #     #     self.main_data.add_data(data=[temp_dict])
    #     # self.main_data.add_data(data=[GlobalVariables.Glob_Var.line_trigger_display_data])
    #     self.data_for_display.append(GlobalVariables.Glob_Var.line_trigger_display_data)
    #     skill_tags = ["Sex","displaySex","Ass","displayAss","Breasts","displayBreasts","Mouth","displayMouth",
    #                   "Seduction","displaySeduction","Magic","displayMagic","Pain","displayPain","Holy","displayHoly",
    #                   "Unholy","displayUnholy"]
    #     # self.main_data.add_data(data={'Sensitivity': skill_tags})
    #     self.data_for_display.append({'Sensitivity': skill_tags})
    #     self.filter_options([])
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

    def delete_multi_value(self):
        item = self.data_tree.selected_item(value='code')
        self.data_tree.delete_leaf(item)
        if not self.data_tree.treeview.get_children():
            self.data_tree.hide_tree()
        self.edit_flag = True

    def deselect_row(self):
        self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])

    def hide(self):
        self.main_data.clear_tree()
        self.main_data.hide()
        self.main_data.entry_search.hide()

    def show(self):
        self.main_data.show()
        self.main_data.entry_search.show()
    # def update_with_mod_item(self, mod_tree_copy):
    #     """just add copy of mod elements to mod item - first item in tree."""
    #     mod_item = self.main_data.tree_model.item(0, 0)
    #     mod_tree_copy.pop(4)
    #     mod_tree_copy.pop(0)
    #     for idx in range(len(mod_tree_copy), 0, -1):
    #         if isinstance(mod_tree_copy[idx-1], str):
    #             mod_tree_copy.pop(idx-1)
    #     self.main_data.add_data(mod_item, mod_tree_copy, True)


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

    # def reload_mod_data(self, new_values):
    #     mod_item = self.main_data.tree_model.item(0, 0)
    #     mod_item.removeRows(0,mod_item.rowCount())
    #     new_values_without_empty_items = {}
    #     for items in new_values:
    #
    #         if len(new_values[items]) > 0:
    #             new_values_without_empty_items[items] = new_values[items]
    #     self.main_data.add_data_to_display(mod_item, new_values_without_empty_items)

    # def add_folder(self, parent_text, folder_name):
    #     # mod_item = self.main_data.tree_model.item(0, 0)
    #     node = self.main_data.find_node(parent_text, self.main_data.tree_model.index(0, 0))
    #     if node == None:
    #         node = self.main_data.tree_model.item(0, 0)
    #         add_element_type_as_folder = QStandardItem()
    #         add_element_type_as_folder.setText(parent_text)
    #         add_element_type_as_folder.setEditable(True)
    #         add_element_type_as_folder.setWhatsThis('folder')
    #         node.appendRow(add_element_type_as_folder)
    #         node = add_element_type_as_folder
    #     else:
    #         node = self.main_data.tree_model.itemFromIndex(node)
    #         if node.whatsThis() != 'folder':
    #             node = node.parent()
    #     new_folder = QStandardItem()
    #     new_folder.setText(folder_name)
    #     new_folder.setEditable(True)
    #     new_folder.setWhatsThis('folder')
    #     node.appendRow(new_folder)


class Function_Gui:
    def __init__(self, functionType=None, game_data=None, master=None, event_type=None, fields_lay=None, target_area=None,
                 adding_config=None, scene_list=None):
        """functionType - scene or text
        list_flag - should probably be flag if include event functions
        event_type - if eventtext, losscene, victoryscene
        fields_lay - this is part of bigger layout, so fields lay is layout only for fields from functions
        adding config. list of 3 values. first is flag, second area displa and 3 is scene display, might be none"""
        if event_type:
            self.event = event_type
        else:
            self.event = None
        self.functions_layout = fields_lay
        # """target type is either TRUE - add data to treeview display, or FALSE, add as text to area"""
        # self.target_type = functionType
        """temp data is for holding temporary data to display in fields"""
        self.temp_data = None
        """event temporary data"""
        self.displayed_characters = []
        """in custom layout put treeview with functions, area with explanations and buttons to add"""
        self.custom_layout = QtWidgets.QVBoxLayout()
        self.parent_widget = master
        """list of created fields. from this gather data"""
        self.function_fields_list = []
        self.target_area = target_area
        # self.frame_for_end_loop_fields = tk.Frame(self.frame_function_fields)
        # self.field_for_end_loop = SwapLine_Field(self.frame_for_end_loop_fields, self.function_fields_list)
        # end_loop_frame = tk.Frame(self.frame_function_fields)
        """this ending field is for endlopps. data is taken from function fields by getVal. If here is endloop,
        this field is added to the list at specific place and value taken from it."""
        self.ending_field = SimpleFields.SimpleEntry(None)
        # self.ending_field = SimpleFields.SimpleEntry(master=end_loop_frame, field_name='temp', label_position='U',
        #                                              tooltip_text=None, field_data=None)
        # self.prepared_fields['text'].append(SceneSimpleEntry(master=end_loop_frame))
        """checkboxes and buttons. check for adding as function or text, button to prepare and add functions"""
        h_lay_checkboxes = QtWidgets.QHBoxLayout()

            # tk.Button(self.frame_functions, text='Prepare function', wraplength=50,
            #                                     command=lambda: self.prepare_function_fields())
        self.buttonADD_function = SimpleFields.CustomButton(None, 'Add')
        self.buttonADD_function.setMaximumWidth(40)
        self.buttonADD_function.clicked.connect(self.add_function_fields)
        h_lay_checkboxes.addWidget(self.buttonADD_function)
        self.checkbox_text = SimpleFields.CheckBox(self.parent_widget, 'TEXT', 't')
        self.checkbox_text.set_up_widget(h_lay_checkboxes)
        self.checkbox_event = SimpleFields.CheckBox(self.parent_widget, 'EVENT', 'e')
        self.checkbox_event.set_up_widget(h_lay_checkboxes)
        self.buttonPREPARE_function = SimpleFields.CustomButton(None, 'Prep')
        self.buttonPREPARE_function.setMaximumWidth(40)
        self.buttonPREPARE_function.clicked.connect(self.prepare_function_fields)
        h_lay_checkboxes.addWidget(self.buttonPREPARE_function)
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.checkbox_text)
        self.button_group.addButton(self.checkbox_event)
        self.button_group.buttonToggled.connect(self.on_checkbox_toggled)
        """flag function will be list. first its a 0/1, second, target field"""
        self.flag_function_target_type = []
        self.adding_config = adding_config
        if not adding_config[0]:
            # if 0, only text, disable event adding
            self.checkbox_event.setEnabled(False)
            self.checkbox_text.set_val(True)
            self.checkbox_text.setEnabled(False)
        h_lay_checkboxes.setAlignment(QtCore.Qt.AlignCenter)
        self.custom_layout.addLayout(h_lay_checkboxes)

        self.treeview_functions = SimpleFields.ElementsList(None, 'functions', True, False, False, delete_flag=False)
        self.treeview_functions.setMinimumWidth(300)
        self.treeview_functions.set_up_widget(self.custom_layout)
        self.treeview_functions.add_data(data=GlobalVariables.Glob_Var.functions_display)
        self.treeview_functions.clicked.connect(self.display_explanation)
        self.area_instruction = SimpleFields.AreaEntry()
        self.area_instruction.setMaximumSize(300, 200)
        self.area_instruction.set_up_widget(self.custom_layout)

        # self.function_data = otherFunctions.load_json_data('game/_textfunction.json')
        # for function_place in GlobalVariables.functions_data:
        #     self.list_functions.add_branch(function_place)
        #     for function_groups in GlobalVariables.functions_data[function_place]:
        #         # testing
        #         self.list_functions.add_leaves(function_place, [function_groups], update_flag=False)
        #         for function_name in GlobalVariables.functions_data[function_place][function_groups]:
        #             # testing
        #             self.list_functions.add_leaves(function_groups, [function_name['title']], update_flag=False)
        #     functiontreeview = ''
        #     if functions == 'general' or functions == 'asset':
        #         functiontreeview = self.list_functions
        #         functiontreeview.change_title('general')
        #     elif functions == 'events' or functions == 'combat':
        #         functiontreeview = self.list_functions
        #         functiontreeview.change_title('events')
        #     else:
        #         break
        #     for insideFunctions in self.function_data[functions]:
        #         templist = []
        #         branch = insideFunctions
        #         for names in self.function_data[functions][branch]:
        #             templist.append(names['name'])
        #     functiontreeview.add_branch(branch, templist)
        """here add main_game_treeview with items from main game and mod. Not all functions need them,
        so hide and show when needed and make it work same as in main window"""
        self.treeview_main_game_items = SimpleFields.Main_MultiList(None, "Game items", main_label_flag=False)
        self.treeview_main_game_items.current_scene_list = scene_list
        # self.treeview_main_game_items = main_game_for_functions_treeview(None, "Game items")
        # self.treeview_main_game_items.main_data.setMaximumHeight(200)
        # self.treeview_main_game_items.data_for_display = GlobalVariables.Glob_Var.display_elements_game_and_mod
        # self.treeview_main_game_items.set_up_data_for_display(game_data)
        self.flag_main_game_items = False
        # self.treeview_main_game_items.add_main_game_items()
        # temp_list = []
        # temp_mod = copy.copy(GlobalVariables.Mod_Var.mod_data)
        # for item in temp_mod:
        #     tempd = {item: temp_mod[item]}
        #     temp_list.append(tempd)
        # self.treeview_main_game_items.update_with_mod_item(temp_list)
        self.treeview_main_game_items.set_up_widget(self.functions_layout)
        self.treeview_main_game_items.hide()

        self.field_title = SimpleFields.SimpleEntry(None, 'Title')
        self.field_title.setEnabled(False)
        self.field_title.set_up_widget(self.functions_layout)
        self.field_title.setMaximumWidth(300)

        self.flag_error_checkbox = False
        # self.field_title = SceneSimpleEntry(self.frame_function_fields)
        # self.field_title = SimpleFields.SimpleEntry(self.frame_function_fields, field_name='temp', label_position='U',
        #                                             tooltip_text=None, field_data=None, fill_option='left')

    def set_up_widget(self, outside_layout):
        outside_layout.addLayout(self.custom_layout)

    def create_function_field(self, structure):
        # TODO check all specials now
        """this is for creation fields that will be destroyed, instead of premaking them"""
        for field in structure:
            tempfield = None
            if structure[field]["type"] == "text":
                tempfield = SimpleFields.SimpleEntry(None, field_name=field,
                                                     field_data=structure, main_data_treeview=self.treeview_main_game_items)
            elif structure[field]["type"] == "int":
                tempfield = SimpleFields.NumericEntry(None, wid=4, field_name=field,
                                                      field_data=structure)
                # tempfield.bind("<Tab>", otherFunctions.focus_next_window)
            elif structure[field]["type"] == "singlelist":
                tempfield = SimpleFields.SingleList(None, field, structure)
                # TODO for damage from monster - dropdown is too small. either make it wider or change to multilist
                # tempfield = SceneSingleList(self.frame_function_fields)
                tempfield.reload_options(structure[field]['choices'])
                # tempfield.update_label(field)
            elif structure[field]["type"] == 'multilist':
                # tempfield = SceneMultiList(self.frame_function_fields, structure[field]['choices'],
                #                                    field_options=structure[field]['options'])
                # tempfield.update_label(field)
                tempfield = SimpleFields.MultiListDisplay(None, field, structure[field], main_data_treeview=self.treeview_main_game_items)
                self.flag_main_game_items = True
            elif structure[field]["type"] == 'combobox':
                tempfield = SimpleFields.InputList(None, flag_delete=True, field_name=field
                                                   , field_data=structure[field])
            elif structure[field]["type"] == 'filePath':
                tempfield = SimpleFields.FileField(None, 'File', field_data=structure[field])
            # if 'choices' in structure[field]:
            #     if 'Scene' in structure[field]['choices']:
            self.function_fields_list.append(tempfield)
            # if field == 'Scenes':
            #         self.special_event_jumping_load_scenes_to_list("", flag_current_event=True)
            # tempfield.pack(side=tk.LEFT, fill=tk.BOTH)
            if tempfield is not None:
                tempfield.set_up_widget(self.functions_layout, True)
            if self.flag_main_game_items:
                self.treeview_main_game_items.show()

    # def close_window(self):
    #     self.flag_if_window_open = False
    #     self.window_function.destroy()
#     # TODO check setchoice if choice is deleted when press X on input least. maybe add confirmation window too.
    def display_explanation(self):
        # treevieID is just variable for elementlist, so access treeview in it, gets its name and parent name and search
        # in function_data for explanation to put
        selected_function_item = self.treeview_functions.selected_element()
        if not selected_function_item.child(0,0):
            """clear current list of prepare fields. should work each time user select different function"""
            if self.function_fields_list:
                for field in self.function_fields_list:
                    """if its just function name, here is simple string"""
                    if isinstance(field, str):
                        continue
                    else:
                        field.destroy()
                self.function_fields_list.clear()
            # function_data = GlobalVariables.Glob_Var.functions_data[selected_function_item.text()]
            function_data = GlobalVariables.Glob_Var.get_functions(selected_function_item.text())
            explanation_text = function_data['explanation']
            self.area_instruction.clear_val()
            self.area_instruction.set_val(explanation_text)
            """also, if there is only 1 step it is title, might as well hide prep button and add button will add it"""
            if function_data['steps'] == '1':
                self.buttonPREPARE_function.hide()
                self.buttonADD_function.show()
                self.function_fields_list.append(function_data['title'])
            else:
                self.buttonPREPARE_function.show()
                self.buttonADD_function.hide()
            self.field_title.set_val(function_data['title'])
            self.field_title.adjustSize()
        else:
            self.buttonADD_function.hide()
            self.buttonPREPARE_function.hide()
        self.treeview_main_game_items.hide()

    def prepare_function_fields(self, function_values=[]):
        """function_values - in case user wants to edit function from scene, here should be passed list
        where 0 is function title, rest are attributes"""
        if function_values:
            function_name = function_values[0]
        else:
            function_item = self.treeview_functions.selected_element()
            function_name = function_item.text()
        function_data = GlobalVariables.Glob_Var.get_functions(function_name)
        # function_data = GlobalVariables.Glob_Var.functions_data[function_name]
        self.buttonADD_function.show()
        # field_data = function_data['structure']
        """fields data should be a dictionary with all data for specific funtion from file."""
        # if field_data:
        # flag if display treeview for game items selection
        self.flag_main_game_items = False
        """prepare correct fields. read structure in function data and make something like create field.
                    some fields are related to each other so put them in special and code manually"""
        # if "simple" in function_data['options']:
        # self.prepare_title(function_name)
        # self.frame_function_fields.pack()
        if "TODO" in function_data['options']:
            struct_len = len(function_data['structure'].keys())
            function_data['structure'] = {}
            function_data['options'] = []
            for idx in range(1, struct_len + 1):
                function_data['structure'][idx] = {"type": "text"}
        if function_data['steps'] != '1':
            """create all fields for function. Later, if special, adjust them"""
            self.create_function_field(function_data['structure'])
            if "special" in function_data['options']:
                self.prepare_special(function_name)
            print('making fields for function')
        # for field in self.function_fields_list:
        #     field.show_field()
        print('stuff to do after fields are prepared')
        """add separate EndLoop field to the list of fields. if steps is just EndLoop, add at the end, if there is a
         number, it is number of steps before end"""
        if 'EndLoop' in function_data['steps'] or 'EndMusicList' in function_data['steps']:
        # if len(function_data['steps']) > 2:
            """codename should be 'EndLoop-2' first part is string, usually EndLoop, sometime EndMusicList,
             second is where"""
            end_loop_place = function_data['steps'].split('-')
            self.ending_field.set_val(end_loop_place[0])
            if len(end_loop_place) > 1:

                self.function_fields_list.insert(len(self.function_fields_list) - int(end_loop_place[1]),
                                                 self.ending_field)
            else:
                self.function_fields_list.append(self.ending_field)
        """previously it was separated, but now i dont see purpose for it"""
        ## self.prepare_function_fields_step2(function_name, function_data)
            # if function_values:
            #     self.load_function_attributes(function_values, field_data)
            #     # return
            #     #      how to deal with endloop? Fields are probably ready.
            #     """this needs to load values into fields, but problem when endloop is used. So this need another
            #      function to analyzed function structure and divide it accordingly to endloop. Might need to
            #       restructurize function json"""
            #     # for field, values in zip(self.function_fields_list, function_data[1:]):
            #     #     field.set_val(values)
        # else:
        #     self.function_fields_list = ['nothing to make']
        self.buttonPREPARE_function.hide()
        # print(final_functions)

    # def prepare_function_fields_step2(self, function_name, function_data):

    def add_function_fields(self):
        """add prepared data from function fields to target area, scene text or just input text"""
        tag = self.field_title.get_val()
        if not tag:
            return
        checked_button = self.button_group.checkedButton()
        if checked_button is None:
            for checkbox in self.button_group.buttons():
                checkbox.setStyleSheet("QCheckBox { color: red }")
                self.flag_error_checkbox = True
            return
        """if flag TRUE, should add as data to treeview(scene)2
        if flag FALSE, add as text to area1"""
        if checked_button.text() == 'EVENT':
            selected_element = self.adding_config[2].selected_element()
            if isinstance(self.function_fields_list[0], str):
                function_values = self.function_fields_list[0]
            else:
                # final_function = []
                index = 0
                # EndLoop_flag =
                # tag = self.function_fields_list[0].get_val()
                if tag == 'DisplayCharacters':
                    # add later updating list of currect characters in window markup text
                    self.displayed_characters = self.function_fields_list[0].get_val()
                elif 'Choice' in tag:
                    """when choice is typed in fields and user clicked 'add function'"""
                    SimpleFields.mod_temp_data.add_choice(self.function_fields_list[0].get_val(), self.function_fields_list[1].get_val())
                elif 'ChoiceTo' in tag:
                    self.function_fields_list.pop(-1)
                temp_vals = []
                for function_field in self.function_fields_list:
                    value = function_field.get_val()
                    if isinstance(value, list):
                        for val in value:
                            temp_vals.append(val)
                    else:
                        if value == 'blank':
                            value = ''
                        elif not value:
                            continue
                        temp_vals.append(value)
                function_values = {tag: temp_vals}
            """depending on selected element, add without node or with to treeview'"""
            if selected_element:
                if not selected_element.child(0, 0):
                    parent = selected_element.parent()
                    if parent:
                        self.adding_config[2].new_insert_data(function_values, parent)
                        return
            self.adding_config[2].new_insert_data(function_values)
        else:
            final_function = self.field_title.get_val() + '|'
            # else:
            for function in self.function_fields_list:
                if isinstance(function, str):
                    break
                value = function.get_val()
                final_function += value + '|'
            self.adding_config[1].insert_text('|f|' + final_function + 'n|')

    def prepare_special(self, function_name):
        if 'Jump' in function_name or "Call" in function_name:
            """this should cover all jumping to other scenes and events. If event jump, load event data with scenes
            if just scenes, load current event scenes"""
            if "Event" in function_name:
                """first copy content of treeview from current mod """
                # GlobalVariables.list_elementlists[1].treeview_optionstochoose
                # self.function_fields_list[1].treeview_optionstochoose
                self.function_fields_list[0].clear_val()
                # line below should be obsolete, takes care by otherfunctions-getlistopiotns
                # otherFunctions.duplicate_treeview(GlobalVariables.list_elementlists[0].treeview,
                #                                   self.function_fields_list[0].tree_options_choose.treeview,
                #                                   destination_leaf='mod-Events')
                # if 'JumpToNPCEvent' in function_name:
                """from available event, remove all not in town"""
                #     leaves = self.function_fields_list[0].tree_options_choose.treeview.get_children()
                #     for leaf in leaves[1:]:
                #         if 'Town' not in self.function_fields_list[0].tree_options_choose.treeview.item(leaf)['text']:
                #             self.function_fields_list[0].tree_options_choose.treeview.delete(leaf)
                # if function_name == 'JumpToLossEvent':
                #     leaves = self.function_fields_list[0].tree_options_choose.treeview.get_children()
                #     for leaf in leaves[1:]:
                #         if 'Loss' not in self.function_fields_list[0].tree_options_choose.treeview.item(leaf)['text']:
                #             self.function_fields_list[0].tree_options_choose.treeview.delete(leaf)
                if 'Scene' in function_name:
                    self.function_fields_list[0].final_data.function_on_modify(self.special_event_jumping_load_scenes_to_list)
            elif 'Scene' in function_name:
                self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
        elif function_name == "SwapLineIf":
            special_field = SwapLine_Field(self.functions_layout, self.treeview_main_game_items)
            self.function_fields_list.append(special_field)
            self.function_fields_list[0].currentTextChanged.connect(special_field.prepare_line_fields)
            self.function_fields_list[0].set_val('')
            self.flag_main_game_items = True
            self.treeview_main_game_items.show()
        elif 'Damage' in function_name:
            self.function_fields_list[0].final_data.function_on_modify(self.skills_from_monster)
        #     TODO
        # elif function_name == 'DisplayCharacters':
        #     PrepareSpeakers(self.function_fields_list[0])
        elif function_name == 'ChangeImageLayer':
            self.SpecialChangeImageLayer_prep_speakers_field(1)
            self.function_fields_list[1].currentTextChanged.connect(lambda: self.load_layer_picture_data('Layer'))
            self.function_fields_list[0].currentTextChanged.connect(lambda: self.load_layer_picture_data('Image'))

        elif function_name == 'AnimateImageLayer':
            self.SpecialChangeImageLayer_prep_speakers_field(2)
            # self.function_fields_list[2].var.trace_id = self.function_fields_list[2].var.trace(
            #     'w', lambda *args, data_level='Layer', girl_field=2: self.load_layer_picture_data(data_level, girl_field))
            self.function_fields_list[2].currentTextChanged.connect(lambda: self.load_layer_picture_data('Layer'))
        elif 'Choice' in function_name:
            if 'Event' in function_name:
                SimpleFields.mod_temp_data.prepare_fields_for_choice_set_up(self.function_fields_list[1], self.function_fields_list[2], self.function_fields_list[0])
            else:
                SimpleFields.mod_temp_data.prepare_fields_for_choice_set_up(self.function_fields_list[0], self.function_fields_list[1])
            if function_name == 'GetEventAndIfChoiceIs':
                self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
            # field = Choices(self.frame_function_fields)
            # field.field_choice_no.pack(side=tk.LEFT)
            # field.field_choice_text.pack(side=tk.LEFT)
            # field.pack()
            # self.function_fields_list.append(field)
            # self.function_fields_list.append(field.field_choice_no)
            # self.function_fields_list.append(field.field_choice_text)
            # self.Special_Set_Up_Choices_Fields(function_name)

        elif function_name == 'Speaks':
            temp_field = SceneSpeaks(self.frame_function_fields, self.field_title)
            temp_field.show_field()
            self.function_fields_list.append(temp_field)
            self.temp_data = temp_field
        elif function_name == 'StatCheck':
            self.function_fields_list[3].set_val('Fail')
            self.function_fields_list.insert(0, StatCheckField(self.frame_function_fields))
            self.function_fields_list[0].show_field()
            if self.event == 'EventText':
                element = 'Events'
            else:
                element = 'Monsters'
            list_of__dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
            for scene in list_of__dictionary_scenes:
                self.function_fields_list[-1].tree_options_choose.treeview.insert('mod-Scene', 'end',
                                                                                 text=scene['NameOfScene'])
                self.function_fields_list[-3].tree_options_choose.treeview.insert('mod-Scene', 'end',
                                                                                 text=scene['NameOfScene'])
        elif function_name == 'PlayMotionEffectCustom':
            self.function_fields_list[1].var.trace_id = self.function_fields_list[1].var.trace(
                'w', lambda *args: self.Set_Up_Motion_Effect())
        elif function_name == 'ApplyStance':
            temp_field = SimpleFields.CheckBox(self.frame_function_fields, 'SetAttack', 'SetAttack')
            temp_field.field.configure(command=lambda: self.set_attack(temp_field.value))
            temp_field.pack()
            self.function_fields_list.append(temp_field)
            # temp_field.change_f(command=self.set_attack(temp_field.value))
        elif function_name == 'Menu':
            temp_field = MenuField(self.functions_layout, self.treeview_main_game_items)
            self.function_fields_list.append(temp_field)
            self.flag_main_game_items = True
            self.treeview_main_game_items.show()
        elif function_name == 'CombatEncounter':
            temp_field = CombatEncounter(self.frame_function_fields)
            temp_field.pack()
            self.function_fields_list.append(temp_field)

        return
    def special_event_jumping_load_scenes_to_list(self, selected_event, flag_current_event=False):
        """for function 'jump to scene'.Since there is 1 field with data, it should not change when something is selected.
        instead, on selection, put same value in second field in 'scene_source'. when clicked on second field
        load data depending on tha value. it will be done similar to loading other stuff in main_data"""
        """if current event, jump only to scenes define in the field. they might not be saved to mod var"""
        if flag_current_event:
            self.treeview_main_game_items.scene_source = 'current'
            # if self.event == 'EventText':
            #     element = 'Events'
            # else:
            #     element = 'Monsters'
            # # list_of_dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
            # list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates[element].frame_fields[self.event].get_val()
            # for scene in list_of_dictionary_scenes:
            #     self.function_fields_list[-1].tree_options_choose.treeview.insert('mod-Scenes', 'end',
            #                                                                      text=scene['NameOfScene'])
            # return
        # selected_event = self.function_fields_list[0].get_val()
        else:
            self.treeview_main_game_items.scene_source = selected_event

            # if not self.function_fields_list[0].tree_options_choose.treeview.get_children(selected_item):
            #     self.function_fields_list[1].clear_val('all')
            #     selected_event = self.function_fields_list[0].tree_options_choose.treeview.item(selected_item)['text']
            #     temp_scene_names = []
            #     if 'mod-Events' in selected_item[0]:
            #         scenes_list = GlobalVariables.current_mod['Events'][selected_event]['EventText']
            #         for scene in scenes_list:
            #             temp_scene_names.append(scene['NameOfScene'])
            #     else:
            #         scenes_list = GlobalVariables.main_game_items['Events']['data'][selected_event]
            #         temp_scene_names = scenes_list
            #     # for scene in scenes_list:
            #         # self.function_fields_list[1].tree_options_choose.treeview.insert('mod-Scenes', 'end', text=scene['NameOfScene'])
            #     # self.function_fields_list[1].tree_options_choose.treeview.insert('', 'end', text=scene['NameOfScene'])
            #     self.function_fields_list[1].tree_options_choose.add_leaves('', temp_scene_names)
            #     # temp_scene_names.append(scene['NameOfScene'])
            # # self.function_fields_list[2].treeview_optionstochoose.treeview.insert('', 'end',values=temp_scene_names)

    # def Special_function_swapline(self, *args):
    #     self.field_for_end_loop.prepare_line_fields(self.function_fields_list[0].get_val())

    def SpecialChangeImageLayer_prep_speakers_field(self, field_no):
        """almost done, but its not gonna work. Speaker show not from speaker fields, but from function
         displayCharacters, which are based on speakers list. So first, it need to check displaycharacters in memory
          somewher, if not used, because we loaded the mod, then it need to find that by searching backwards by scene
           names and when found, load data and then load speakers in current displayedcharacters"""
        """first prepare list of speakers used in current event.These come from DisplayCharacters function,
         should be saved in function.displayed_characters var"""

        """for now, load data according to speakers. Stuff above will be fixed some other time."""
        # if not self.displayed_characters:
        #     self.displayed_characters = otherFunctions.find_current_displayed_characters(self.event, self.target_field)
        # speakers = PrepareSpeakers()
        # displayed_speakers_list = []
        # index = 0
        # for character in self.displayed_characters:  # this is probably list of indexed characters from "speakers" field
        #     for speaker in speakers:  # this should be list of dictionary of all speakers in event
        #         index += 1
        #         if character == speaker['name'] or character == str(index):  # displayed characters might be index number or character id
        #             # first is number then name, because later it easier to first get number, and then id and prepare
        #             #  data with ready title
        #             displayed_speakers_list.append(str(index))
        #             displayed_speakers_list.append(speaker['name'])
        #             index = 0
        #             break
        # TODO might be problem when girls name is not equeal to girl id or something like that
        speaker_data = PrepareSpeakers()
        temp_list = ['']
        for speaker in speaker_data:
            if speaker['name'] not in temp_list:
                temp_list.append(speaker['name'])
        self.function_fields_list[field_no].reload_options(temp_list)
        """looks good. now, prepare layers data for first field, based on speakers. All should be in currentmod, if need
         layers from main game it would need to load all mosnters data...so just search for specific monster by its id."""

        # layer_data = {}
        # branch = ''
        # for speaker in displayed_speakers_list:
        #     if len(speaker) > 2:
        #         branch += speaker
        #         girl_id = speaker
        #         for girls in GlobalVariables.current_mod['Monsters']:
        #             if girl_id == GlobalVariables.current_mod['Monsters'][girls]['IDname']:
        #                 temp_dict = {}
        #                 for layers in GlobalVariables.current_mod['Monsters'][girls]['pictures']:
        #                     # temp_dict[layers['Name']] = []
        #                     # for image_layer in layers['Images']:
        #                     #     temp_dict[layers['Name']].append(image_layer['Name'])
        #                     temp_dict[layers['Name']] = {}
        #                     for image_layer in layers['Images']:
        #                         temp_dict[layers['Name']][image_layer['Name']] = {}
        #                 layer_data[branch] = temp_dict
        #                 branch = ''
        #                 break
        #     else:
        #         branch = speaker
        #     # displayed_speakers_list is list of displayed characters, so need to find speakers based on their ids
        #     # """get layer data for each speaker that is a monster"""
        #     # if speaker['SpeakerType'] == 'Monster':
        #     #     girl_id = speaker['name']
        #     #     for girls in GlobalVariables.current_mod['Monsters']:
        #     #         if girl_id == GlobalVariables.current_mod['Monsters'][girls]['IDname']:
        #     #             temp_dict = {}
        #     #             for layers in GlobalVariables.current_mod['Monsters'][girls]['pictures']:
        #     #                 # temp_dict[layers['Name']] = []
        #     #                 # for image_layer in layers['Images']:
        #     #                 #     temp_dict[layers['Name']].append(image_layer['Name'])
        #     #                 temp_dict[layers['Name']] = {}
        #     #                 for image_layer in layers['Images']:
        #     #                     temp_dict[layers['Name']][image_layer['Name']] = {}
        #     #             """since speaker list also containes postname and number, it should be able to search by them
        #     #             for now, just add that to the key and later search in"""
        #     #             layer_data[girl_id + '-' + speaker['postName']] = temp_dict
        #     #             break
        # self.temp_data = layer_data

    def load_layer_picture_data(self, data_level='temp', girl_id_field=1):
        """find field with speaker name - should be labeled Speaker"""
        # girl_id = girl[0].lower()
        # girl_id = girl_id.replace(' ', '')
        # girl_id = girl[0]
        for field in self.function_fields_list:
            if field.title == 'Speaker':
                girl_id = field.get_val()
                # girl_id = field.get_val().lower()
                # girl_id = girl_id.replace(' ', '')
                break
        # girl_id = self.function_fields_list[girl_id_field].get_val().lower()
        if girl_id == 'select options' or girl_id == '' or len(girl_id) < 3:
            return
        """get pictures of girls, first check mod, if not there, look in main game data"""
        if girl_id in GlobalVariables.Mod_Var.mod_data['Monsters']:
            pictures_list = GlobalVariables.Mod_Var.mod_data['Monsters'][girl_id]['pictures']
        else:
            pictures_list = GlobalVariables.Glob_Var.main_game_data['Girls'][girl_id]['pictures']

        results_list = []
        if data_level == 'Layer':
            for field in self.function_fields_list:
                if field.title == 'Layer Type':
                    """instead of hardcoded field no, find field by label"""
                    # self.function_fields_list[0].clear_val('')
                    field.clear_val()
                    for pictures in pictures_list:
                        if 'Set' in pictures:
                            for pict_set in pictures['Set']:
                                results_list.append(pict_set['Name'])
                            break
                        else:
                            results_list.append(pictures['Name'])
                    # results_list.append('ImageSet')
                    # results_list.append('ImageSetPersist')
                    # results_list.append('ImageSetDontCarryOver')
                    field.reload_options(results_list)
                    field.add_items_to_skip_sort(['ImageSet', 'ImageSetPersist', 'ImageSetDontCarryOver'])
                    # self.function_fields_list[0].reload_options(results_list)
                    break
        elif data_level == 'Image':
            for field in self.function_fields_list:
                if field.title == 'Layer Type':
                    layer_name = field.get_val()
                    break
            # layer_name = self.function_fields_list[0].get_val()
            # self.function_fields_list[2].clear_val('')
            if 'ImageSet' in layer_name:
                for pictures in pictures_list:
                    results_list.append(pictures['Name'])
            else:
                for pictures in pictures_list:
                    if pictures['Name'] == layer_name:
                        if 'Set' in pictures:
                            for pict_set in pictures['Set']:
                                for images in pict_set['Images']:
                                    results_list.append(images['Name'])
                            break
                        else:
                            for images in pictures['Images']:
                                results_list.append(images['Name'])
            # results_list.append('ActivateOverlay')
            # results_list.append('DeactivateOverlay')
            # results_list.append('None')

            for field in self.function_fields_list:
                if field.title == 'Image':
                    field.reload_options(results_list)
                    field.add_items_to_skip_sort(['ActivateOverlay', 'DeactivateOverlay', 'None'])
                    break
            # self.function_fields_list[2].reload_options(results_list)

    def SpecialChangeImageLayerStep2(self, source_field=0, target_field=0, data_level=0):
        self.function_fields_list[target_field].clear_val('')
        target_data = self.function_fields_list[source_field].get_val()
        if target_data == 'select options' or target_data == '':
            return
        for lvl1 in self.temp_data:
            if data_level == 1:
                if target_data in lvl1:
                    temp_list = list(self.temp_data[lvl1].keys())
                    self.function_fields_list[target_field].reload_options(temp_list)
                    return
            else:
                for lvl2 in self.temp_data[lvl1]:
                    if data_level == 2:
                        if target_data in lvl2:
                            temp_list = list(self.temp_data[lvl1][lvl2].keys())
                            self.function_fields_list[target_field].reload_options(temp_list)
                            return
                    else:
                        for lvl3 in self.temp_data[lvl1][lvl2]:
                            if data_level == 3:
                                if target_data in lvl3:
                                    temp_list = list(self.temp_data[lvl1][lvl2][lvl3].keys())
                                    self.function_fields_list[target_field].reload_options(temp_list)
                                    return
    def SpecialChangeImageLayerStep3(self, source_field=0, target_field=0, data_level=0):

        self.function_fields_list[target_field].clear_val('')
        target_data = self.function_fields_list[source_field].get_val()
        if target_data == 'select options' or target_data == '':
            return
        """first prepare that temp_data. since this def is used to damage from monster and should use all girls from game"""
        skills = otherFunctions.FindMonsterSkills(target_data)
        temp_dict = {target_data:{}}
        for skill in skills:
            temp_dict[target_data][skill] = {}
        self.temp_data = temp_dict

        for lvl1 in self.temp_data:
            if data_level == 1:
                if target_data in lvl1:
                    temp_list = list(self.temp_data[lvl1].keys())
                    self.function_fields_list[target_field].reload_options(temp_list)
                    return
            else:
                for lvl2 in self.temp_data[lvl1]:
                    if data_level == 2:
                        if target_data in lvl2:
                            temp_list = list(self.temp_data[lvl1][lvl2].keys())
                            self.function_fields_list[target_field].reload_options(temp_list)
                            return
                    else:
                        for lvl3 in self.temp_data[lvl1][lvl2]:
                            if data_level == 3:
                                if target_data in lvl3:
                                    temp_list = list(self.temp_data[lvl1][lvl2][lvl3].keys())
                                    self.function_fields_list[target_field].reload_options(temp_list)
                                    return
    def skills_from_monster(self, source_field=0, target_field=0, data_level=1):
        self.function_fields_list[1].clear()
        target_data = self.function_fields_list[0].get_val()
        if target_data == 'select options' or target_data == '':
            return
        """first prepare that temp_data. since this def is used to damage from monster and should use all girls from game"""
        skills = otherFunctions.FindMonsterSkills(target_data)
        self.function_fields_list[1].reload_options(skills)

    """should be obsolete"""
    def Special_Set_Up_Choices_Fields(self, function_name):
        if 'Event' in function_name:
            field_order = 1
            self.function_fields_list[0].clear_val()
            # otherFunctions.duplicate_treeview(GlobalVariables.list_elementlists[1].treeview,
            #                                   self.function_fields_list[0].tree_options_choose.treeview,
            #                                   destination_leaf='mod-Events')
            self.function_fields_list[0].var.trace_id = self.function_fields_list[0].var.trace("w", lambda *args, arg1=field_order, arg2='true': self.special_set_up_choices_1(
                arg1, arg2))
            if len(self.function_fields_list) == 4:
                if self.event == 'EventText':
                    element = 'Events'
                else:
                    element = 'Monsters'
                list_of__dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
                for scene in list_of__dictionary_scenes:
                    self.function_fields_list[3].tree_options_choose.treeview.insert('mod-Scene', 'end',
                                                                                     text=scene['NameOfScene'])
        else:
            field_order = 0
            event_name = GlobalVariables.templates['Events'].input_filename.get_val()
            self.special_set_up_choices_1(field_order, event_name)
        """first field should be choice number, second field should be choice text"""
        # choice_list = SimpleFields.mod_temp_data.get_choices(get_val='gate')
        # self.function_fields_list[field_order].reload_options(choice_list)
        # choice_list = SimpleFields.mod_temp_data.get_all_choices_text()
        # self.function_fields_list[field_order+1].reload_options(choice_list)
        # choices_list = SimpleFields.mod_temp_data.get_choices(get_val='gate')
        # # self.function_fields_list[field_order].var.trace_add("write", lambda order: self.Special_Set_Up_Choices_2(field_order))
        self.function_fields_list[field_order].var.trace_id = self.function_fields_list[field_order].var.trace("w", lambda *args, arg1=field_order: self.Special_Set_Up_Choices_2(arg1))
        self.function_fields_list[field_order].delete_place = 'gate'
        self.function_fields_list[field_order+1].delete_place = 'choice'
        self.function_fields_list[field_order+1].choice_no_field = self.function_fields_list[field_order]
        self.function_fields_list[field_order+1].var.trace_id = self.function_fields_list[field_order+1].var.trace("w",
                                                         lambda *args, arg1=field_order: self.Special_Set_Up_Choices_2_1(
                                                             arg1))

        # old version, when it searched on the spot
        # choices_list = []
        # if 'Event' in function_name:
        #     return
        # else:
        #     if self.event == 'EventText':
        #         element = 'Events'
        #     else:
        #         element = 'Monsters'
        #     list_of__dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
        #     for dictionary_scene in list_of__dictionary_scenes:
        #         theText = dictionary_scene['theScene']
        #         index = 0
        #         for texts in theText:
        #             if len(texts) == 9:
        #                 if texts == 'SetChoice':
        #                     choices_list.append(theText[index+1])
        #             index += 1
        #     self.function_fields_list[1].reload_options(choices_list)

    """should be obsolete"""
    def special_set_up_choices_1(self, field_order, event_name=None):
        if event_name:
            event_name = self.function_fields_list[0].get_val()
        """first field should be choice number, second field should be choice text"""
        choice_list = SimpleFields.mod_temp_data.get_choices(get_val='gate', event_name=event_name)
        self.function_fields_list[field_order].reload_options(choice_list)
        self.function_fields_list[field_order].event_name = event_name
        choice_list = SimpleFields.mod_temp_data.get_all_choices_text(event_name=event_name)
        self.function_fields_list[field_order+1].reload_options(choice_list)
        self.function_fields_list[field_order+1].event_name = event_name

        # choices_list = SimpleFields.mod_temp_data.get_choices(get_val='gate')
        # # self.function_fields_list[field_order].var.trace_add("write", lambda order: self.Special_Set_Up_Choices_2(field_order))
        # self.function_fields_list[field_order].var.trace("w", lambda *args, arg1=field_order: self.Special_Set_Up_Choices_2(arg1))
        # self.function_fields_list[field_order].delete_place = 'gate'
        # self.function_fields_list[field_order+1].delete_place = 'choice'
        # self.function_fields_list[field_order+1].choice_no_field = self.function_fields_list[field_order]
        # self.function_fields_list[field_order+1].var.trace("w",
        #                                                  lambda *args, arg1=field_order: self.Special_Set_Up_Choices_2_1(
        #                                                      arg1))

    """should be obsolete"""
    def Special_Set_Up_Choices_2(self, order):
        """get choice number and load choices text"""
        choice_gate = self.function_fields_list[order].get_val()
        if choice_gate:
            choices_list = SimpleFields.mod_temp_data.get_choices(get_val=choice_gate, event_name=self.function_fields_list[order+1].event_name)
            self.function_fields_list[order+1].limit_options(choices_list)
    """should be obsolete"""
    def Special_Set_Up_Choices_2_1(self, order):
        """get choice text and load its number"""
        choice_text = self.function_fields_list[order+1].get_val()
        if choice_text:
            choices_no = SimpleFields.mod_temp_data.get_gates(choice=choice_text, event_name=self.function_fields_list[order].event_name)
            self.function_fields_list[order].set_val(choices_no)

    def Set_Up_Motion_Effect(self):
        setup_val = self.function_fields_list[1].get_val()
        if len(self.function_fields_list) == 5:
            """not sure if pop here is enough, might need to change to destroy"""
            field = self.function_fields_list.pop(2)
            field.destroy()
        elif len(self.function_fields_list) == 6:
            field = self.function_fields_list.pop(2)
            field.destroy()
            field = self.function_fields_list.pop(2)
            field.destroy()
        if setup_val in 'Character Bodypart':
            temp_field = SimpleFields.InputList(self.frame_function_fields, field_name='Speaker')
            speakers = PrepareSpeakers()
            temp_list = []
            for speaker in speakers:
                if speaker['name'] not in temp_list:
                    temp_list.append(speaker['name'])
            temp_field.reload_options(temp_list)
            temp_field.pack(side=tk.LEFT)
            self.function_fields_list.insert(2, temp_field)
            if setup_val == 'Bodypart':
                temp_field = SceneSingleList(self.frame_function_fields)
                temp_field.update_label('Layer Type')
                self.function_fields_list[2].traceId = self.function_fields_list[2].var.trace(
                    'w', lambda *args, data_level='Layer', girl_field=1: self.load_layer_picture_data(data_level,
                                                                                                      girl_field))
                self.function_fields_list.insert(3, temp_field)
                temp_field.pack(side=tk.LEFT)

    def set_attack(self, check_val):
        if check_val.get() == 1:
            print('it might work')
            # TODO here create multilist with ...something
            temp_field = SimpleFields.MultiList(self.frame_function_fields, 'Skills', '', 'U',
                                                ['currentmod-Skills', 'main-inc-/Skills'], ['single_item', 'search'])
            self.function_fields_list.append(temp_field)
            temp_field.pack(side=tk.LEFT)
        elif check_val.get() == 0:
            temp = self.function_fields_list.pop(-1)
            temp.destroy()
            print('still work')
        else:
            print('fuck it')
        return
    def load_function_attributes(self, attributes_list, function_data):
        if len(function_data['steps']) == 1:
            for field, values in zip(self.function_fields_list, attributes_list[1:]):
                field.set_val(values)

    def on_checkbox_toggled(self, checkbox, checked):
        if self.flag_error_checkbox:
            if checked:
                for button in self.button_group.buttons():
                    button.setStyleSheet("QCheckBox { color: black }")


#
#
#
#     # def connect_fields_difficult_idea(self, function_name):
#     #     """trying to combine other defs were we connect fields"""
#     #     if 'Jump' in function_name or "Call" in function_name:
#     #         """this should cover all jumping to other scenes and events. If event jump, load event data with scenes
#     #         if just scenes, load current event scenes"""
#     #         if "Event" in function_name:
#     #             """first copy content of treeview from current mod """
#     #             # GlobalVariables.list_elementlists[1].treeview_optionstochoose
#     #             # self.function_fields_list[1].treeview_optionstochoose
#     #             self.function_fields_list[1].clear_val()
#     #             otherFunctions.duplicate_treeview(GlobalVariables.list_elementlists[1].treeview,
#     #                                               self.function_fields_list[1].tree_options_choose.treeview,
#     #                                               destination_leaf='mod-Events')
#     #             if 'JumpToNPCEvent' in function_name:
#     #                 leaves = self.function_fields_list[1].tree_options_choose.treeview.get_children()
#     #                 for leaf in leaves[1:]:
#     #                     if 'Town' not in self.function_fields_list[1].tree_options_choose.treeview.item(leaf)['text']:
#     #                         self.function_fields_list[1].tree_options_choose.treeview.delete(leaf)
#     #             elif function_name == 'JumpToLossEvent':
#     #                 leaves = self.function_fields_list[1].tree_options_choose.treeview.get_children()
#     #                 for leaf in leaves[1:]:
#     #                     if 'Loss' not in self.function_fields_list[1].tree_options_choose.treeview.item(leaf)['text']:
#     #                         self.function_fields_list[1].tree_options_choose.treeview.delete(leaf)
#     #             if 'Scene' in function_name:
#     #                 self.function_fields_list[1].tree_options_choose.treeview.bind("<<TreeviewSelect>>",
#     #                                                                                self.special_event_jumping_load_scenes_to_list)
#     #         if 'Scene' in function_name:
#     #             self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
#
def PrepareSpeakers(target_field=None):
    """first prepare list of speakers used in current event. This should also include ordered numbers"""
    speaker_data = GlobalVariables.Glob_Var.access_templates['Events'].frame_fields['Speakers'].get_val()
    index = 1
    """this is for field with treeview"""
    if target_field:
        target_field.clear_val(all_flag=True)
        for item in target_field.tree_options_choose.treeview.get_children():
            target_field.tree_options_choose.treeview.delete(item)
        for speaker in speaker_data:
            target_field.tree_options_choose.add_branch(speaker['name'] + '-' + str(index), [speaker['name'], str(index)], update_flag=False)
            index += 1
    else:
        return speaker_data
#
#
# def SpecialChangeImageLayerStep5(temp_data, source_field, target_field, data_level):
#     target_data = source_field.get_val()
#     temp_list = None
#     index = 1
#     for lvl1 in temp_data:
#         if index == data_level:
#             if target_data == lvl1:
#                 temp_list = list(temp_data[lvl1].keys())
#                 break
#         else:
#             index += 1
#             for lvl2 in temp_data[lvl1]:
#                 if index == data_level:
#                     if target_data == lvl1:
#                         temp_list = list(temp_data[lvl1][lvl2].keys())
#                         break
#             else:
#                 index += 1
#                 for lvl3 in temp_data[lvl1]:
#                     if index == data_level:
#                         if target_data == lvl1:
#                             temp_list = list(temp_data[lvl1][lvl2][lvl3].keys())
#                             break
#     if temp_list:
#         target_field.reload_options(temp_list)
#     else:
#         print('SpecialChangeImageLayerStep2 problem - no layer list to display. how did this happen? is this used outside of events?')
# def SpecialChangeImageLayerStep4(self, *args):
#     girl_layer = self.function_fields_list[2].get_val()
#     temp_list = None
#     for girl_target_layers in self.temp_data:
#         if girl_layer == girl_target_layers:
#             temp_list = list(girl_target_layers.keys())
#             break
#     if temp_list:
#         self.function_fields_list[1].reload_options(temp_list)
#     else:
#         print('SpecialChangeImageLayerStep2 problem - no layer list to display. how did this happen? is this used outside of events?')
#
# def function_steps_no(function_name):
#     for function_place in GlobalVariables.functions_data:
#         for function_groups in GlobalVariables.functions_data[function_place]:
#             for function in GlobalVariables.functions_data[function_place][function_groups]:
#                 if function['title'] == function_name:
#                     if 'EndLoop' in function['steps']:
#                         temp = function['steps'].split('-')
#                         if len(temp) > 1:
#                             """there is number which should mean which field from the ending should have endloop
#                             i need this as minus number, and counting from last, last element
#                              start at -1 so need to increase by 1"""
#                             return (int(temp[1])+1) * -1
#                         else:
#                             return -1
#                     else:
#                         return int(function['steps'])-1
#     """if function not found, return 0"""
#     return 0
#         #  TODO i wanted this to check how many steps involved in function, but Im afraid it is dynamic,
#         #   as i dont see it written anywhere. will probaly have to add key to the file. I see that either
#         #   function has static number of steps, or dynamic which end with EndLoop. So will have to work with that.
#         #   This should return string or number.
