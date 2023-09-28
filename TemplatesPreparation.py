import json
import textwrap
import re
from os import makedirs
from os import access, F_OK
# import re
from collections import OrderedDict
# from GUIFieldClasses import createField
# from GUIFieldClasses import CreateToolTip, ExpandDictionaryField, ListDictionaryField,\
#     MonsterGroups, DeckField, Picturedisplay, Speaker, PerkDoubleList, RestOfPerks, SkillsType, OptionalFields, \
#     FetishApply, FunctionField, Functional_Dummy, SimpleEntry
# from FunctionalWindow import , Functional_Dummy
# from GUIFieldClasses import FunctionField, Functional_Dummy
from SimpleFields import SimpleEntry, SimpleEntryDisplay, mod_temp_data
from CustomFields import createField, OptionalFields, FunctionField, Functional_Dummy
    # , OptionalFields, FunctionField,
from otherFunctions import error_log, show_message
import GlobalVariables
import tkinter as tk
from tkinter import ttk
# from tkinter import messagebox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
def test_out_file(test):
    print(test)

class Templates:
    def __init__(self, file_path_template, element_name, addition_field='', master=None):
        """template layouts are StacketLayout. Each new widget is another layer. But I need each template in one layer,
        so each template with have main Widget - this is where all other widgets will be place. main widget will have
        layouts etc."""
        self.main_widget = QtWidgets.QWidget()
        self.main_template_layout = QtWidgets.QHBoxLayout()
        #
        # self.main_widget.setLayout(self.layout)
        # self.main_widget = QtWidgets.QWidget()
        # self.main_template_layout = QtWidgets.QHBoxLayout()
        # # Create a widget and set the layout as its layout
        # self.scroll_widget = QtWidgets.QWidget()
        # self.scroll_widget.setLayout(self.main_template_layout)
        #
        # # Create a scroll area and set the widget as its widget
        # self.scroll_area = QtWidgets.QScrollArea()
        # self.scroll_area.setWidget(self.scroll_widget)
        # self.scroll_area.setWidgetResizable(True)
        #
        # # Create a vertical layout and add the scroll area to it
        # self.layout = QtWidgets.QVBoxLayout()
        # self.layout.addWidget(self.scroll_area)
        # # self.layout.setStyleSheet("background-color:black;")
        #
        # # Set the layout for the widget
        #
        # self.main_widget.setLayout(self.layout)


        #
        # self.main_widget = QtWidgets.QWidget()
        # self.main_template_layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.main_template_layout)
        self.layer_index = 0
        self.widgets_in_template = {}

        self.dict_optional_fields = {}
        self.file_template = file_path_template
        self.frame_fields = {}
        self.json_templates = {}
        self.element_type = element_name
        self.input_filename = None
        self.addition_field = addition_field
        self.field_used_in_additions = []
        self.flag_additional_marking = False
        self.optional_class_worker = ''
        self.size = []
        self.flag_fields_marked_for_addition = False
        try:
            # for template_path in self.file_templates:
            with open(self.file_template, encoding='utf-8-sig') as Blank:
                self.json_templates = json.load(Blank, object_hook=OrderedDict)
                # self.frame_fields = {}
        except Exception as e:
            show_message("template loading error", 'A issue has occured loading template ' +
                         self.file_template + '.\nTraceback:\n{0}'.format(str(e)),"")
            exit()
        # for field in self.json_templates:
        #     if 'options' in self.json_templates[field]:
        #         if 'addition' in self.json_templates[field]['options']:
        #             self.addition_field_list.append(field)

    def prepItemGui(self):
        functional_field_repeat = None

        row_max_size=15
        currect_size = 0
        col_place = 1
        # self.layout_template = QtWidgets.QVBoxLayout()
        # self.main_template_layout.addLayout(self.layout_template)
        layout_template = QtWidgets.QVBoxLayout()
        self.main_template_layout.addLayout(layout_template)
        self.input_filename = SimpleEntry(self.main_widget, 'File name', {'tooltip': 'Provide name for file. If empty,'
                                                              ' name without spaces will become file name.'})
        self.input_filename.set_up_widget(layout_template)

        # if self.element_type != 'Fetishes':
        #     self.input_filename.pack(fill='both')
        for field in self.json_templates:
            # GuiFieldName = element_name + field
            # try:
            #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
            #         element_frame = temp_frame
            #     else:
            #         element_frame = temp_frame
                # field_value = createField(element_frame, field, self.json_templates[field])
                field_value = createField(None, field, self.json_templates[field], template_name=self.element_type)
                # if field_value == '':
                #     continue
                # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
                if self.json_templates[field]["type"] in 'functionfield':
                    functionflag = ''
                    if self.element_type == 'Events':
                        functionflag = self.json_templates['CardType']
                    """similar to perk double list, there are dummy objects of function field. They have reference
                     to main fields and their task to to set and get vals, by calling first function field"""
                    if functional_field_repeat:
                        # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                        #                                       field)
                        field_value.main_field = functional_field_repeat
                        self.frame_fields[field] = field_value
                        # label_field.destroy()
                    else:
                        functional_field_repeat = FunctionField(functionflag, master=None, view_title=field)
                        # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                        # self.frame_fields[field] = functional_field_repeat
                        field_value = Functional_Dummy(functional_field_repeat, field)
                        self.frame_fields[field] = field_value
                    functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                                                          , dummy_field=field_value)
                    field_value = functional_field_repeat
                if field_value == '':
                    # print(field)
                    # continue
                    # continue
                #     if self.json_templates[field]["type"] in 'skilltype':
                #         continue
                #         # advance_field = SkillsType(frame_advancedFields, self.frame_fields, field)
                #         # self.frame_fields[field] = advance_field
                #         self.frame_fields[field] = SkillsType(element_frame, self.frame_fields, field)
                #         field_value = self.frame_fields[field].skill_type_field
                #
                    # if self.json_templates[field]["type"] in 'optional':
                        # field_value = OptionalFields(self.frame_gui, self.json_templates[field])
                        # self.optional_class_worker = field_value
                    if self.json_templates[field]["type"] in 'optional':
                        field_value = OptionalFields(self.main_widget, self.json_templates[field], self.main_template_layout)
                        self.optional_class_worker = field_value
                    """"""
                    # if self.json_templates[field]["type"] in 'optional' and mode == 1:
                    #     field_value = OptionalFields(self.frame_gui, self.json_templates[field])
                    # else:
                    #     field_value = OptionalFields(self.frame_gui)
                    # self.optional_class_worker = field_value
                    """"""
                # elif self.json_templates[field]["type"] in 'functionfield':
                #         functionflag = ''
                #         if self.element_type == 'Events':
                #             functionflag = self.json_templates['CardType']
                #         #     TODO somehow i need to know if this advance field in this element type was created already
                #         #             if yes, then just add another branch with name of new field
                #         #           answer - list with number of field name. add new field should add proper branch
                #         """similar to perk double list, there are dummy objects of function field. They have reference
                #          to main fields and their task to to set and get vals, by calling first function field"""
                #         if functional_field_repeat:
                #         # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                #         #                                       field)
                #             advance_field = Functional_Dummy(functional_field_repeat, field)
                #             self.frame_fields[field] = advance_field
                #             label_field.destroy()
                #         else:
                #             functional_field_repeat = FunctionField(functionflag, frame_advancedFields
                #                                                     , view_title=field, label_field=label_field)
                #             # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                #             self.frame_fields[field] = functional_field_repeat
                #             advance_field = Functional_Dummy(functional_field_repeat, field)
                #         functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                #                                                   , dummy_field = advance_field)

                # else:
                # if isinstance(field_value, list):
                #     self.frame_fields[field] = field_value[0]
                #     self.frame_fields[field_value[1].title] = field_value[1]
                #     field_value = field_value[0]
                # else:
                #     if not self.json_templates[field]["type"] == 'optional':
                #         self.frame_fields[field] = field_value
                # print(field_value.title + ' ' + str(field_value.row_size))
                # print(field)
                field_value.set_up_widget(layout_template)
                """set aside info if field is in addition"""
                if 'options' in self.json_templates[field]:
                    if 'addition' in self.json_templates[field]['options']:
                        self.field_used_in_additions.append(field)
                currect_size += field_value.row_size
                if currect_size >= 15:
                    currect_size = 0
                    col_place += 1
                    layout_template.addStretch(1)
                    layout_template = QtWidgets.QVBoxLayout()
                    self.main_template_layout.addLayout(layout_template)
                self.frame_fields[field] = field_value
        layout_template.addStretch(1)
        self.main_template_layout.addStretch(1)

        self.custom_fields_functionality()
            # except:
            #     error_log('error in TemplatesPreparation starting in line 82')
            #     error_log('something wrong with ' + field + ' in file of ' + self.element_type)
            #     error_log(sys.exc_info()[1])


            #     field_value = createField(frame_singleline_fields.scrollable_frame, field, self.json_templates[field])
            #     self.frame_fields[field] = field_value
            # else:
            #     field_value = createField(frame_advance_fields.scrollable_frame, field, self.json_templates[field])
            #     if field_value == '':
            #         frame_advancedFields = tk.Frame(master=frame_advance_fields.scrollable_frame, bg='blue')
            #         frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
            #         label_field = tk.Label(master=frame_advancedFields, text=field)
            #         label_field.grid(row=0, column=0, columnspan=3)
            #         if self.json_templates[field]["type"] in 'PairFields':
            #             advance_field = PerkDoubleList(self.json_templates[field], frame_advancedFields)
            #             self.frame_fields[field] = advance_field
            #             for field in self.json_templates[field]['fields'][1:]:
            #                 connected_field = RestOfPerks(field)
            #                 self.frame_fields[field['name']] = connected_field
            #                 advance_field.add_other_fields(connected_field)
            #         elif self.json_templates[field]["type"] in 'functionfield':
            #             functionflag = ''
            #             if self.element_type == 'Events':
            #                 functionflag = self.json_templates['CardType']
            #             #      somehow i need to know if this advance field in this element type was created already
            #             #             if yes, then just add another branch with name of new field
            #             #           answer - list with number of field name. add new field should add proper branch
            #             """similar to perk double list, there are dummy objects of function field. They have reference
            #              to main fields and their task to to set and get vals, by calling first function field"""
            #             if functional_field_repeat:
            #                 # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
            #                 #                                       field)
            #                 advance_field = Functional_Dummy(functional_field_repeat, field)
            #                 self.frame_fields[field] = advance_field
            #                 label_field.destroy()
            #             else:
            #                 functional_field_repeat = FunctionField(functionflag, frame_advancedFields
            #                                                         , view_title=field, label_field=label_field)
            #                 # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
            #                 self.frame_fields[field] = functional_field_repeat
            #                 advance_field = Functional_Dummy(functional_field_repeat, field)
            #             functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
            #                                                   , dummy_field=advance_field)
            #
            #         elif self.json_templates[field]["type"] in 'skilltype':
            #             advance_field = SkillsType(self.json_templates[field], frame_advancedFields, self.frame_fields, field)
            #             self.frame_fields[field] = advance_field
            #         elif self.json_templates[field]["type"] in 'optional':
            #             advance_field = OptionalFields(self.json_templates[field], frame_advancedFields, self.frame_fields, frame_optional_fields)
            #     else:
            #         self.frame_fields[field] = field_value

    def clear_template(self):
        self.input_filename.clear_val()
        for field in self.frame_fields:
            self.frame_fields[field].clear_val()

    def load_element_data(self, element_name, element_data=None):
        """below is in case element data is just file name, but i dont see reason for this anymore
           ....oooo, its for addition loading"""
        if isinstance(element_data, str):
            temp = element_data.split('/')
            element_file_name = temp[-1][:-5]
            with open(GlobalVariables.Glob_Var.start_path + '/' + element_data, encoding='utf-8-sig') as file:
                element_data = json.load(file, object_hook=OrderedDict)
        if element_name == '':
            show_message("Nothing", "No details to display", "Warning")
        else:
                # self.input_filename.set_val(element_name)
                if element_data is None:
                    element_data = GlobalVariables.Mod_Var.mod_data[self.element_type][element_name]
                    element_file_name = GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name]
                if self.element_type != 'Fetishes':
                    self.input_filename.set_val(element_file_name)
            # elementType == 'Items':
            # try:
                # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
                # for field, value in current_mod[self.element_type][element_name].items():
                #     if field in self.frame_fields:
                #         # try:
                #         self.frame_fields[field].clear_val()
                #         self.frame_fields[field].set_val(value)
                """clearing is separate, because there are some double fields. like, appear twice,
                 but are controlled by 1 element. so if first time it puts data, it will delete it afterwards"""
                for field in self.frame_fields:
                    self.frame_fields[field].clear_val()
                for field in element_data:
                    # try:
                    if field in self.frame_fields:
                        self.frame_fields[field].set_val(element_data[field])
                        # TODO change labels colour back, but also include if displayed addition or not.
                        # self.frame_fields[field].label_change_colour('reset')
                        # except:
                        #     error_log('error in TemplatesPreparation in line 554')
                        #     error_log('problem with template data load for - ' + self.element_type)
                        #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))
                    else:
                        self.optional_class_worker.set_val(field, element_data[field])
                # for field in self.frame_fields:
                #     # try:
                #     if field in element_data:
                #         self.frame_fields[field].set_val(element_data[field])
                #         # TODO change labels colour back, but also include if displayed addition or not.
                #         # self.frame_fields[field].label_change_colour('reset')
                #         # except:
                #         #     error_log('error in TemplatesPreparation in line 554')
                #         #     error_log('problem with template data load for - ' + self.element_type)
                #         #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))
                #     else:
                #         self.optional_class_worker.set_val(field, element_data[field])

        # if (GlobalVariables.flag_addition or 'Addition' in element_data) and not self.flag_fields_marked_for_addition:
        #     for field in self.addition_field_list:
        #         self.frame_fields[field].label_change_colour('red')
        #         self.flag_fields_marked_for_addition = True
        #         GlobalVariables.flag_modify_addition = True
        # elif (not GlobalVariables.flag_addition and 'Addition' not in element_data) and self.flag_fields_marked_for_addition:
        #     for field in self.addition_field_list:
        #         self.frame_fields[field].label_change_colour(reset=True)
        #         self.flag_fields_marked_for_addition = False
        #         GlobalVariables.flag_modify_addition = False

    def mark_additional_fields(self):
        """go over field in field for additionsl and mark labels in different colour.
        maybe even lock others?"""
        for field in self.field_used_in_additions:
            self.frame_fields[field].label_custom.change_background_color()

    def clear_markings(self):
        for field in self.field_used_in_additions:
            self.frame_fields[field].label_custom.clear_color()


    def save_data_in_current_mod(self, current_mod, flag_addition='1/2'):
        # save element data into the current mod dictionary and add it into the lists.
        item_temp = OrderedDict()
        error_flag = False
        if 'name' in list(self.frame_fields.keys()):
            unique_field = 'name'
        elif self.element_type == 'Monsters':
            unique_field = 'IDname'
        else:
            unique_field = 'Name'
        file_name = self.input_filename.get_val()
        if not file_name and self.element_type != 'Fetishes':
            show_message('File name', 'Please provide', 'Error 1')
            return
        element_name = self.frame_fields[unique_field].get_val()
        """if provided only filename, it should return with prefix and add only 1 row, as folder"""
        if element_name == '':
            return 'folder_' + file_name
        # current_mod[elementType] = elementname
        GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name] = file_name
        # if 'Addition' in current_mod[self.element_type][element_name]:
        """if object already exists in mod, wait, this does not make sense, i dont remember its previous workings"""
        # if element_name in current_mod[self.element_type]:
        if flag_addition == 2:
            """yeah, insteaf of true false, i gave it numbers"""
            item_temp['Addition'] = 'Yes'
            # for field, value in self.frame_fields.items():
            #     if field in self.addition_field_list:
            for field in self.field_used_in_additions:
                self.frame_fields[field].get_val(temp_dict_container=item_temp)
        else:
            for field, value in self.frame_fields.items():
                # print(self.templates[elementType][field].get())
                # print(self.templates[elementType][field].get_val())
                # i dont know what that optional was here for. maybe for optional fields.
                # if value.get_val() == 'OPTIONAL' or value.get_val() == 'optional':
                #     continue
                """IMPORTAN CHANGE!!!"""
                # itemTemp[field] = value.get_val()
                value.get_val(temp_dict_container=item_temp)
        current_mod[self.element_type][element_name] = item_temp
        return element_name

    def save_element_in_file(self, element_name, file_path):
        file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][element_name]
        file_name = GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name]
        elementPath = file_path + '/'
        if not access(elementPath, F_OK):
            makedirs(elementPath)
            # print(elementPath)
        # file_name = item_file_name
        file_name = re.sub('[^A-Za-z0-9]+', '', file_name)
        with open(elementPath + file_name + '.json', 'w') as objectF:
            objectF.write(json.dumps(file_data, indent='\t'))

    def custom_fields_functionality(self):
        return

class AdventureTemplate(Templates):
    def __init__(self, master=None):
        # super().__init__('files/_fields.json', 'Adventures', master=master)
        super().__init__('files/_BlankAdventure_modtemplate.json', 'Adventures', master=master)

        self.size = [800, 620]

class EventsTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankEvent_modtemplate.json', 'Events', master=master)
        # TODO update for what is this map ? :P
        self.scenes_map = {}
        #TODO check size after adding other stuff
        self.size = [800, 620]

    def load_element_data(self, element_name, element_data=None):
        mod_temp_data.current_editing_event = element_name
        super().load_element_data(element_name, element_data)
        # print('check if this apepares after super is done')
        # mod_temp_data.current_editing_event = self.input_filename.get_val()
    def save_element_details_in_current_mod(self, current_mod):
        return
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True


class Templates_old:
    # file_templates = {
    #     "Adventures": 'files/_BlankAdventure_modtemplate.json',
    #     "Events": 'files/_BlankEvent_modtemplate.json',
    #     "Fetishes": 'files/_BlankFetish_modtemplate.json',
    #     "Items": 'files/_BlankItem_modtemplate.json',
    #     "Locations": 'files/_BlankLocation_modtemplate.json',
    #     "Monsters": 'files/_BlankMonster_modtemplate.json',
    #     "Perks": 'files/_BlankPerk_modtemplate.json',
    #     "Skills": 'files/_BlankSkill_modtemplate.json'}
    def __init__(self, file_path_template, element_name, addition_field='', master=None):

        self.frame_gui = tk.Frame(master=master, bg='green')


        # self.frame_create_data = None
        # self.frame_display_data = tk.Frame(bg='green')
        self.frame_fields = {}
        # self.fields_for_create_frame = {}
        # self.fields_for_display_frame = {}
        # self.frame_gui = self.frame_display_data

        self.dict_optional_fields = {}
        self.file_template = file_path_template
        self.json_templates = {}
        self.element_type = element_name
        self.input_filename = None
        self.addition_field = addition_field
        self.addition_field_list = []
        self.optional_class_worker = ''
        self.flag_fields_marked_for_addition = False
        try:
            # for template_path in self.file_templates:
            with open(self.file_template, encoding='utf-8-sig') as Blank:
                self.json_templates = json.load(Blank, object_hook=OrderedDict)
                # self.frame_fields = {}
        except Exception as e:
            messagebox.showwarning("template loading error",
                                   'A issue has occured loading template ' + self.file_template + '.\n'
                                   'Traceback:\n'
                                   '{0}'.format(str(e)), parent=self)
            exit()
        for field in self.json_templates:
            if 'options' in self.json_templates[field]:
                if 'addition' in self.json_templates[field]['options']:
                    self.addition_field_list.append(field)

    def prepItemGui(self, mode=0):
        # self.setup_frames_fields(mode)
        # element_name = 'Items'
        # functional_field_flag = [0, '']
        functional_field_repeat = None

        #     frame_singleline_fields = tk.Frame(self.frame_gui)
        #     frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #
        #     frame_advance_fields = tk.Frame(self.frame_gui)
        #     # frame_advance_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #     # frame_singleline_fields = tk.Frame(master=self.frame_gui, bg='red')
        #     # frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH)
        # frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')
        #
        #     frame_ref_a = frame_singleline_fields
        #     frame_ref_b = frame_advance_fields

        row_max_size=15
        currect_size = 0
        col_place = 1
        # for testing rowss in templates
        # visibility_frame = tk.Frame(self.frame_gui)
        # visibility_frame.grid(row=0, column=0)
        # for idx in range(25):
        #     templabel = tk.Label(visibility_frame, text='row ' + str(idx))
        #     templabel.grid(row=idx)
        """mode is for display or create. if creating, then 1, if just display then ="""
        # if mode:
        #     self.frame_gui = self.frame_create_data
        #     self.frame_fields = self.fields_for_create_frame
        # else:
        #     self.frame_gui = self.frame_display_data
        #     self.frame_fields = self.fields_for_display_frame
        element_frame = tk.Frame(master=self.frame_gui)
        element_frame.grid(row=0, column=col_place)
        # frame_filename = tk.Frame(frame_ref_a)
        # frame_filename.pack(fill=tk.BOTH)
        if mode:
            self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
                                                                           ' name without spaces will become file name.', 'L')
        else:
            self.input_filename = SimpleEntryDisplay(element_frame, 'File name', 'Provide name for file. If empty,'
                                                                          ' name without spaces will become file name.',
                                              'L', None, None, self.element_type)
        if self.element_type != 'Fetishes':
            self.input_filename.pack(fill='both')


        flag_switch = 1
        for field in self.json_templates:
            # GuiFieldName = element_name + field
            # try:
            #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
            #         element_frame = temp_frame
            #     else:
            #         element_frame = temp_frame
                # field_value = createField(element_frame, field, self.json_templates[field])
                field_value = createField(element_frame, field, self.json_templates[field], mode, template_name=self.element_type)
                # if field_value == '':
                #     continue
                # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
                if self.json_templates[field]["type"] in 'functionfield':
                    functionflag = ''
                    if self.element_type == 'Events':
                        functionflag = self.json_templates['CardType']
                    """similar to perk double list, there are dummy objects of function field. They have reference
                     to main fields and their task to to set and get vals, by calling first function field"""
                    if functional_field_repeat:
                        # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                        #                                       field)
                        field_value.main_field = functional_field_repeat
                        self.frame_fields[field] = field_value
                        # label_field.destroy()
                    else:
                        functional_field_repeat = FunctionField(functionflag, master=element_frame, view_title=field)
                        # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                        # self.frame_fields[field] = functional_field_repeat
                        field_value = Functional_Dummy(functional_field_repeat, field)
                        self.frame_fields[field] = field_value
                    functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                                                          , dummy_field=field_value)
                    field_value = functional_field_repeat
                if field_value == '':
                    # continue
                #     if self.json_templates[field]["type"] in 'skilltype':
                #         continue
                #         # advance_field = SkillsType(frame_advancedFields, self.frame_fields, field)
                #         # self.frame_fields[field] = advance_field
                #         self.frame_fields[field] = SkillsType(element_frame, self.frame_fields, field)
                #         field_value = self.frame_fields[field].skill_type_field
                #
                    # if self.json_templates[field]["type"] in 'optional':
                        # field_value = OptionalFields(self.frame_gui, self.json_templates[field])
                        # self.optional_class_worker = field_value
                    if self.json_templates[field]["type"] in 'optional' and mode == 1:
                        field_value = OptionalFields(self.frame_gui, self.json_templates[field])
                    else:
                        field_value = OptionalFields(self.frame_gui)
                    self.optional_class_worker = field_value
                    """"""
                # elif self.json_templates[field]["type"] in 'functionfield':
                #         functionflag = ''
                #         if self.element_type == 'Events':
                #             functionflag = self.json_templates['CardType']
                #         #     TODO somehow i need to know if this advance field in this element type was created already
                #         #             if yes, then just add another branch with name of new field
                #         #           answer - list with number of field name. add new field should add proper branch
                #         """similar to perk double list, there are dummy objects of function field. They have reference
                #          to main fields and their task to to set and get vals, by calling first function field"""
                #         if functional_field_repeat:
                #         # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                #         #                                       field)
                #             advance_field = Functional_Dummy(functional_field_repeat, field)
                #             self.frame_fields[field] = advance_field
                #             label_field.destroy()
                #         else:
                #             functional_field_repeat = FunctionField(functionflag, frame_advancedFields
                #                                                     , view_title=field, label_field=label_field)
                #             # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                #             self.frame_fields[field] = functional_field_repeat
                #             advance_field = Functional_Dummy(functional_field_repeat, field)
                #         functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                #                                                   , dummy_field = advance_field)

                # else:
                if isinstance(field_value, list):
                    self.frame_fields[field] = field_value[0]
                    self.frame_fields[field_value[1].title] = field_value[1]
                    field_value = field_value[0]
                else:
                    if not self.json_templates[field]["type"] == 'optional':
                        self.frame_fields[field] = field_value
                # print(field_value.title + ' ' + str(field_value.row_size))
                # print(field)
                field_value.pack(fill=tk.BOTH)
                currect_size += field_value.row_size
                if currect_size > 15:
                    currect_size = 0
                    col_place += 1
                    element_frame = tk.Frame(master=self.frame_gui)
                    element_frame.grid(row=0, column=col_place)
                # self.frame_fields[field] = field_value
            # except:
            #     error_log('error in TemplatesPreparation starting in line 82')
            #     error_log('something wrong with ' + field + ' in file of ' + self.element_type)
            #     error_log(sys.exc_info()[1])


            #     field_value = createField(frame_singleline_fields.scrollable_frame, field, self.json_templates[field])
            #     self.frame_fields[field] = field_value
            # else:
            #     field_value = createField(frame_advance_fields.scrollable_frame, field, self.json_templates[field])
            #     if field_value == '':
            #         frame_advancedFields = tk.Frame(master=frame_advance_fields.scrollable_frame, bg='blue')
            #         frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
            #         label_field = tk.Label(master=frame_advancedFields, text=field)
            #         label_field.grid(row=0, column=0, columnspan=3)
            #         if self.json_templates[field]["type"] in 'PairFields':
            #             advance_field = PerkDoubleList(self.json_templates[field], frame_advancedFields)
            #             self.frame_fields[field] = advance_field
            #             for field in self.json_templates[field]['fields'][1:]:
            #                 connected_field = RestOfPerks(field)
            #                 self.frame_fields[field['name']] = connected_field
            #                 advance_field.add_other_fields(connected_field)
            #         elif self.json_templates[field]["type"] in 'functionfield':
            #             functionflag = ''
            #             if self.element_type == 'Events':
            #                 functionflag = self.json_templates['CardType']
            #             #      somehow i need to know if this advance field in this element type was created already
            #             #             if yes, then just add another branch with name of new field
            #             #           answer - list with number of field name. add new field should add proper branch
            #             """similar to perk double list, there are dummy objects of function field. They have reference
            #              to main fields and their task to to set and get vals, by calling first function field"""
            #             if functional_field_repeat:
            #                 # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
            #                 #                                       field)
            #                 advance_field = Functional_Dummy(functional_field_repeat, field)
            #                 self.frame_fields[field] = advance_field
            #                 label_field.destroy()
            #             else:
            #                 functional_field_repeat = FunctionField(functionflag, frame_advancedFields
            #                                                         , view_title=field, label_field=label_field)
            #                 # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
            #                 self.frame_fields[field] = functional_field_repeat
            #                 advance_field = Functional_Dummy(functional_field_repeat, field)
            #             functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
            #                                                   , dummy_field=advance_field)
            #
            #         elif self.json_templates[field]["type"] in 'skilltype':
            #             advance_field = SkillsType(self.json_templates[field], frame_advancedFields, self.frame_fields, field)
            #             self.frame_fields[field] = advance_field
            #         elif self.json_templates[field]["type"] in 'optional':
            #             advance_field = OptionalFields(self.json_templates[field], frame_advancedFields, self.frame_fields, frame_optional_fields)
            #     else:
            #         self.frame_fields[field] = field_value
    # def prepItemGui(self, master_name, element_type):
    #     # print(self.itemTemplate)
    #     # element_name = 'Items'
    #     # functional_field_flag = [0, '']
    #     functional_field_repeat = None
    #     frame_singleline_fields = tk.Frame(master=master_name, bg='red')
    #     frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH)
    #     frame_listsboxes_fields = tk.Frame(master=master_name, bg='green')
    #     frame_listsboxes_fields.pack(side=tk.LEFT, fill=tk.BOTH)
    #     frame_optional_fields = tk.Frame(master=master_name, bg='purple')
    #     for field in self.json_templates[element_type]:
    #         # GuiFieldName = element_name + field
    #         if self.json_templates[element_type][field]["type"] in "text singlelist int filePath":
    #             field_value = createField(frame_singleline_fields, field, self.json_templates[element_type][field])
    #             self.frame_fields[element_type][field] = field_value
    #         elif self.json_templates[element_type][field]["type"] in "multilist area requirement":
    #             field_value = createField(frame_singleline_fields, field, self.json_templates[element_type][field])
    #             self.frame_fields[element_type][field] = field_value
    #         else:
    #             field_value = createField(master_name, field, self.json_templates[element_type][field])
    #             if field_value == '':
    #                 frame_advancedFields = tk.Frame(master=master_name, bg='blue')
    #                 frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #                 label_field = tk.Label(master=frame_advancedFields, text=field)
    #                 label_field.grid(row=0, column=0, columnspan=3)
    #                 if self.json_templates[element_type][field]["type"] in 'PairFields':
    #                     advance_field = PerkDoubleList(self.json_templates[element_type][field], frame_advancedFields)
    #                     self.frame_fields[element_type][field] = advance_field
    #                     for field in self.json_templates[element_type][field]['fields'][1:]:
    #                         connected_field = RestOfPerks(field)
    #                         self.frame_fields[element_type][field['name']] = connected_field
    #                         advance_field.add_other_fields(connected_field)
    #                 elif self.json_templates[element_type][field]["type"] in 'functionfield':
    #                     functionflag = ''
    #                     if element_type == 'Events':
    #                         functionflag = self.json_templates[element_type]['CardType']
    #                     #      somehow i need to know if this advance field in this element type was created already
    #                     #             if yes, then just add another branch with name of new field
    #                     #           answer - list with number of field name. add new field should add proper branch
    #                     """similar to perk double list, there are dummy objects of function field. They have reference
    #                      to main fields and their task to to set and get vals, by calling first function field"""
    #                     if functional_field_repeat:
    #                         # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
    #                         #                                       field)
    #                         advance_field = Functional_Dummy(functional_field_repeat, field)
    #                         self.frame_fields[element_type][field] = advance_field
    #                     else:
    #                         functional_field_repeat = FunctionField(functionflag, frame_advancedFields
    #                                                                 , view_title=field, label_field=label_field)
    #                         # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
    #                         self.frame_fields[element_type][field] = functional_field_repeat
    #                         advance_field = Functional_Dummy(functional_field_repeat, field)
    #                     functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'], field
    #                                                           , dummy_field=advance_field)
    #                     # if functional_field_flag[0] < 1:
    #                     #     advance_field = FunctionField(functionflag, frame_advancedFields
    #                     #                                   , view_title=field, label_field=label_field)
    #                     #     advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
    #                     #     self.frame_fields[element_type][field] = advance_field
    #                     #     functional_field_flag[0] = 1
    #                     #     functional_field_flag[1] = field
    #                     # else:
    #                     #     self.frame_fields[element_type][functional_field_flag[1]].add_new_field(
    #                     #         self.json_templates[element_type][field]['fields']
    #                     #         , field)
    #
    #                 elif self.json_templates[element_type][field]["type"] in 'skilltype':
    #                     advance_field = SkillsType(self.json_templates[element_type][field], frame_advancedFields, self.frame_fields[element_type], field)
    #                     self.frame_fields[element_type][field] = advance_field
    #                 elif self.json_templates[element_type][field]["type"] in 'optional':
    #                     advance_field = OptionalFields(self.json_templates[element_type][field], frame_advancedFields, self.frame_fields[element_type], frame_optional_fields)
    #             else:
    #                 self.frame_fields[element_type][field] = field_value
    #             # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
    #             # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #             # label_field = tk.Label(master=frame_advancedFields, text=field)
    #             # label_field.grid(row=0, column=0, columnspan=3)
    #         #     if self.json_templates[element_type][field]["tooltip"]:
    #         #         CreateToolTip(label_field, self.json_templates[element_type][field]["tooltip"])
    #         #     rowsC += 1
    #         #     if self.json_templates[element_type][field]["type"] in 'dictionary':
    #         #         # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
    #         #         # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #         #         # self.frame_fields['Items'][field] = {}
    #         #         # label_field = tk.Label(master=frame_advancedFields, text=field)
    #         #         # label_field.grid(row=rowsC, column=0, columnspan=2)
    #         #         # rowsC += 1
    #         #         advance_field = ExpandDictionaryField(self.json_templates[element_type][field], frame_advancedFields, view_title=field)
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         # #     elif self.template[field]["type"] in 'functionfield':
    #         # #         # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
    #         # #         # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #         # #         # self.frame_fields['Items'][field] = {}
    #         # #         # label_field = tk.Label(master=frame_advancedFields, text=field)
    #         # #         # label_field.grid(row=rowsC, column=0, columnspan=2)
    #         # #         # rowsC += 1
    #         # #         functionflag = ''
    #         #     elif self.json_templates[element_type][field]["type"] in 'listDict':
    #         #         advance_field = ListDictionaryField(self.json_templates[element_type][field], frame_advancedFields)
    #         #         self.frame_fields[field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'deck':
    #         #         advance_field = DeckField(frame_advancedFields)
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'monstergroups':
    #         #         advance_field = MonsterGroups(frame_advancedFields, self.json_templates[element_type][field]['options'])
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'speaker':
    #         #         advance_field = Speaker(self.json_templates[element_type][field], frame_advancedFields)
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'FetisheApply':
    #         #         advance_field = FetishApply(frame_advancedFields, self.json_templates[element_type][field])
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'PairFields':
    #         #         advance_field = PerkDoubleList(self.json_templates[element_type][field], frame_advancedFields)
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         for field in self.json_templates[element_type][field]['fields'][1:]:
    #         #             connected_field = RestOfPerks(field)
    #         #             self.frame_fields[element_type][field['name']] = connected_field
    #         #             advance_field.add_other_fields(connected_field)
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'skilltype':
    #         #         advance_field = SkillsType(self.json_templates[element_type][field], frame_advancedFields, self.frame_fields[element_type])
    #         #         self.frame_fields[element_type][field] = advance_field
    #         #         columnC += 2
    #         #         rowsC = 0
    #         #     elif self.json_templates[element_type][field]["type"] in 'optional':
    #         #         advance_field = OptionalFields(self.json_templates[element_type][field], frame_advancedFields, self.frame_fields[element_type], frame_optional_fields)
    #         #     else:
    #         #         print("unknown type")
    def save_data_in_current_mod(self, current_mod, flag_addition=False):
        # save element data into the current mod dictionary and add it into the lists.
        item_temp = OrderedDict()
        error_flag = False
        if 'name' in self.frame_fields:
            unique_field = 'name'
        else:
            unique_field = 'Name'
        if self.frame_fields[unique_field].get_val() == '':
            messagebox.showerror('missing name', 'Forgot to name it', parent=self)
            return False

        # element_name = item_temp['name']
        element_name = self.input_filename.get_val()
        if not element_name:
            element_name = self.frame_fields[unique_field].get_val()
            self.input_filename.set_val(element_name)
        # current_mod[elementType] = elementname

        # if 'Addition' in current_mod[self.element_type][element_name]:
        if element_name in current_mod[self.element_type]:
            if 'Addition' in current_mod[self.element_type][element_name]:
            # if flag_addition:
                item_temp['Addition'] = 'Yes'
                # for field, value in self.frame_fields.items():
                #     if field in self.addition_field_list:
                for field in self.addition_field_list:
                    self.frame_fields[field].get_val(temp_dict_container=item_temp)
            else:
                for field, value in self.frame_fields.items():
                    value.get_val(temp_dict_container=item_temp)
        else:
            for field, value in self.frame_fields.items():
                # print(self.templates[elementType][field].get())
                # print(self.templates[elementType][field].get_val())
                # i dont know what that optional was here for. maybe for optional fields.
                # if value.get_val() == 'OPTIONAL' or value.get_val() == 'optional':
                #     continue
                """IMPORTAN CHANGE!!!"""
                # itemTemp[field] = value.get_val()
                value.get_val(temp_dict_container=item_temp)
        optional_fields_dictionary_values = self.optional_class_worker.get_val()
        for field in optional_fields_dictionary_values:
            item_temp[field] = optional_fields_dictionary_values[field]
            # print(field + ' = ' + value.get())
        # if self.dict_optional_fields:
        #     for field, value in self.dict_optional_fields.items():
        #         value.get_val(temp_dict_container=item_temp)
        # print(itemTemp)
        current_mod[self.element_type][element_name] = item_temp
        # if self.element_type in 'Item Perks Skills Monsters':
        #     update_multilists('add', element_name, self.element_type)
        return True
        # elementPath = app.getEntry('ModName') + '/' + elementType + '/'
        # if "itemType" in itemTemp:
        #     elementPath = elementPath + 'Consumable' + '/'
        #     if itemTemp['itemType'] == 'Healing':
        #         elementPath = elementPath + 'Healing' + '/'
        # if not access(elementPath, F_OK):
        #     makedirs(elementPath)
        # with open(elementPath + itemTemp['name'] + '.json', 'w') as objectF:
        #     objectF.write(json.dumps(itemTemp, indent='\t'))

    def save_element_details_in_current_mod_old(self, elementType, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        itemTemp = OrderedDict()
        errorflag = False
        if self.frame_fields[elementType]['name'].get_val() == '':
            messagebox.showerror('missing name', 'Forgot to name it', parent=self)
            return False
        if elementType == 'Items':
            if self.frame_fields[elementType]['itemType'].get_val() == '':
                messagebox.showerror('missing type', 'Forgot type', parent=self)
                return False
        if elementType == 'Fetishes':
            if self.frame_fields[elementType]['Type'].get_val() == '' or \
                    self.frame_fields[elementType]['Type'].get_val() == 'options':
                messagebox.showerror('missing type', 'Forgot type', parent=self)
                return False
        for field, value in self.frame_fields[elementType].items():
            # print(self.templates[elementType][field].get())
            # print(self.templates[elementType][field].get_val())
            if value.get_val() == 'OPTIONAL' or value.get_val() == 'optional':
                continue
            """IMPORTAN CHANGE!!!"""
            # itemTemp[field] = value.get_val()
            value.get_val(temp_dict_container=itemTemp)
            # print(field + ' = ' + value.get())
        # print(itemTemp)
        elementname = itemTemp['name']
        # current_mod[elementType] = elementname
        current_mod[elementType][elementname] = itemTemp
        return True
        # elementPath = app.getEntry('ModName') + '/' + elementType + '/'
        # if "itemType" in itemTemp:
        #     elementPath = elementPath + 'Consumable' + '/'
        #     if itemTemp['itemType'] == 'Healing':
        #         elementPath = elementPath + 'Healing' + '/'
        # if not access(elementPath, F_OK):
        #     makedirs(elementPath)
        # with open(elementPath + itemTemp['name'] + '.json', 'w') as objectF:
        #     objectF.write(json.dumps(itemTemp, indent='\t'))

    def clear_all_vals(self):
        for fields in self.frame_fields:
            self.frame_fields[fields].clear_val()
        if self.optional_class_worker:
            self.optional_class_worker.clear_val()
            if self.dict_optional_fields:
                for field, value in self.dict_optional_fields.items():
                    value.clear_val()
            self.input_filename.clear_val()
    """
        def prepItemGui_old2(self, master_name, element_type):
            # print(self.itemTemplate)
            # element_name = 'Items'
            index = 1
            functional_field_flag = [0, '']
            rowsA = rowsB = columnC = rowsC =0
            template = self.json_templates[element_type]
            frame_singlelineFields = tk.Frame(master=master_name, bg='red')
            frame_singlelineFields.pack(side=tk.LEFT, fill=tk.BOTH)
            frame_listsboxesFields = tk.Frame(master=master_name, bg='green')
            frame_listsboxesFields.pack(side=tk.LEFT, fill=tk.BOTH)
            # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
            # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
            # for fields in template:
            #     test_label = tk.Label(master=frame_singlelineFields, text='placeholder' + fields)
            #     test_label.pack()
            #     self.templates['Items'][fields] = test_label
            for field in template:
                # GuiFieldName = element_name + field
                if template[field]["type"] in "text singlelist int multilist area":
                    temp_frame = tk.Frame(master=frame_singlelineFields, bg='firebrick4')
                    temp_frame.pack(side=tk.TOP, fill=tk.Y)
                    fieldValue = createField(temp_frame, field, rowsA, template[field])
                    self.templates[element_type][field] = fieldValue
                    rowsA += 1
                # elif template[field]["type"] in "multilist area":
                #     temp_frame = tk.Frame(master=frame_listsboxesFields, bg='firebrick3')
                #     temp_frame.pack(side=tk.TOP, fill=tk.BOTH)
                #     fieldValue = createField(temp_frame, field, rowsB, template[field])
                #     self.templates[element_type][field] = fieldValue
                #     # print(GuiFieldName)
                #     rowsB += 3
                elif template[field]["type"] == 'TBD':
                    frame_advancedFields = tk.Frame(master=master_name, bg='purple' + str(index))
                    label_field = tk.Label(master=frame_advancedFields, text="need to find out how this works")
                    label_field.grid(row=rowsC, column=0, columnspan=7)
                    label_field2 = tk.Label(master=frame_advancedFields, text=field)
                    label_field2.grid(row=rowsC+1, column=0, columnspan=7)
                    frame_advancedFields.pack(side=tk.LEFT, fill=tk.Y)
                else:
                    frame_advancedFields = tk.Frame(master=master_name, bg='purple' + str(index))
                    index += 1
                    if index == 5:
                        index = 1
                    # print(str(index))
                    frame_advancedFields.pack(side=tk.LEFT, fill=tk.Y)
                    label_field = tk.Label(master=frame_advancedFields, text=field)
                    label_field.grid(row=rowsC, column=0, columnspan=7)
                    if 'tooltip' in template[field]:
                        CreateToolTip(label_field, template[field]['tooltip'])
                    # rowsC += 1    # it set up label on same row as first field when looping again, so it might not be usefull here
                    if template[field]["type"] in 'dictionary':
                        # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                        # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                        # self.templates['Items'][field] = {}
                        # label_field = tk.Label(master=frame_advancedFields, text=field)
                        # label_field.grid(row=rowsC, column=0, columnspan=2)
                        # rowsC += 1
                        advance_field = ExpandDictionaryField(template[field], frame_advancedFields, view_title=field)
                        self.templates[element_type][field] = advance_field
                        columnC += 2
                        rowsC = 0
                    elif template[field]["type"] in 'functionfield':
                        # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                        # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                        # self.templates['Items'][field] = {}
                        # label_field = tk.Label(master=frame_advancedFields, text=field)
                        # label_field.grid(row=rowsC, column=0, columnspan=2)
                        # rowsC += 1
                        functionflag = ''
                        if element_type == 'Events':
                            functionflag = self.templates[element_type]['CardType']
                        #     TODO somehow i need to know if this advance field in this element type was created already
                        #             if yes, then just add another branch with name of new field
                        #           answer - list with number of field name. add new field should add proper branch
                    # try:
                        if functional_field_flag[0] < 1:
                            advance_field = FunctionField(functionflag, frame_advancedFields
                                                          , view_title=field, label_to_change=label_field)
                            advance_field.add_new_field(template[field]['fields'], field)
                            self.templates[element_type][field] = advance_field
                            functional_field_flag[0] = 1
                            functional_field_flag[1] = field
                        else:
                            self.templates[element_type][functional_field_flag[1]].add_new_field(template[field]['fields']
                                                                                                 , field,
                                                                                                 label_to_hide=label_field)

                    # except:
                    #     print("error occured for Advance fields creation. here is some data:")
                    #     print('var element_type = ' + element_type)
                    #     print('var field = ' + field)
                    #     print('var functionflag = ' + str(functionflag))
                    #     print('var template[field] = ' + str(template[field]))

                        columnC += 2
                        rowsC = 0
                    elif template[field]["type"] in 'listDict':
                        # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                        # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                        # self.templates['Items'][field] = {}
                        # label_field = tk.Label(master=frame_advancedFields, text=field)
                        # label_field.grid(row=rowsC, column=0, columnspan=2)
                        # rowsC += 1
                        advance_field = ListDictionaryField(template[field], frame_advancedFields)
                        self.templates[element_type][field] = advance_field
                        columnC += 2
                        rowsC = 0
                    elif template[field]["type"] in 'monstergroups':
                        advance_field = MonsterGroups(frame_advancedFields, template[field]['options'])
                        self.templates[element_type][field] = advance_field
                        columnC += 2
                        rowsC = 0
                    elif template[field]["type"] in 'deck':
                        advance_field = DeckField(frame_advancedFields)
                        self.templates[element_type][field] = advance_field
                        columnC += 2
                        rowsC = 0
                    elif template[field]["type"] in 'picturedisplay':
                        advance_field = Picturedisplay(frame_advancedFields)
                        self.templates[element_type][field] = advance_field
                        columnC += 2
                        rowsC = 0
    """
    #   TODO add try catch - not an item
    def load_element_data(self, element_name, element_data):
        # print("function display element")
        # print('elementtype-  '+ elementType + ', element name - ' + elementName)
        if isinstance(element_data, str):
            with open(GlobalVariables.startPath + '/' + element_data, encoding='utf-8-sig') as file:
                element_data = json.load(file, object_hook=OrderedDict)
                # element_data = {self.element_type: {element_name: file_data}}
        if element_name == '':
            messagebox.showerror("Nothing", "No details to display", parent=self)
        else:
                self.input_filename.set_val(element_name)
            # elementType == 'Items':
            # try:
                # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
                # for field, value in current_mod[self.element_type][element_name].items():
                #     if field in self.frame_fields:
                #         # try:
                #         self.frame_fields[field].clear_val()
                #         self.frame_fields[field].set_val(value)
                """clearing is separate, because there are some double fields. like, appear twice,
                 but are controlled by 1 element. so if first time it puts data, it will delete it afterwards"""
                for field in self.frame_fields:
                    self.frame_fields[field].clear_val()
                for field in self.frame_fields:
                    # try:
                    if field in element_data:
                        self.frame_fields[field].set_val(element_data[field])
                        # TODO change labels colour back, but also include if displayed addition or not.
                        # self.frame_fields[field].label_change_colour('reset')
                        # except:
                        #     error_log('error in TemplatesPreparation in line 554')
                        #     error_log('problem with template data load for - ' + self.element_type)
                        #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))

                    """optional off, as optional fields not fixed"""
                    # else:
                    #     GlobalVariables.optional_field.set_val(field, value)

        if (GlobalVariables.flag_addition or 'Addition' in element_data) and not self.flag_fields_marked_for_addition:
            for field in self.addition_field_list:
                self.frame_fields[field].label_change_colour('red')
                self.flag_fields_marked_for_addition = True
                GlobalVariables.flag_modify_addition = True
        elif (not GlobalVariables.flag_addition and 'Addition' not in element_data) and self.flag_fields_marked_for_addition:
            for field in self.addition_field_list:
                self.frame_fields[field].label_change_colour(reset=True)
                self.flag_fields_marked_for_addition = False
                GlobalVariables.flag_modify_addition = False

        # flag_prep_addition = False
        # if 'Addition' in element_data or GlobalVariables.flag_addition:
        #     flag_prep_addition = True
        #     # TODO problem here. if loaded modded addition, it sets red labels, then if load normal mod item, it still seems addition
        # if flag_prep_addition:
        #     if not self.flag_fields_marked_for_addition:
        #         for field in self.addition_field_list:
        #             self.frame_fields[field].label_change_colour('red')
        #         self.flag_fields_marked_for_addition = True
        # else:
        #     if self.flag_fields_marked_for_addition:
        #         for field in self.addition_field_list:
        #             self.frame_fields[field].label_change_colour(reset=True)
        #         self.flag_fields_marked_for_addition = False
            # except:
            #     print("could fix this some day. should not try to load details of a branch")
            #     print('Templates preparation  >!load element data def!')
    # def load_element_data_backup(self, element_name, current_mod):
    #     # print("function display element")
    #     # print('elementtype-  '+ elementType + ', element name - ' + elementName)
    #     if isinstance(current_mod, str):
    #         with open(GlobalVariables.startPath + '/' + current_mod, encoding='utf-8-sig') as file:
    #             file_data = json.load(file, object_hook=OrderedDict)
    #         current_mod = {self.element_type: {element_name: file_data}}
    #     if element_name == '':
    #         messagebox.showerror("Nothing", "No details to display", parent=self)
    #     else:
    #             self.input_filename.set_val(element_name)
    #         # elementType == 'Items':
    #         # try:
    #             # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
    #             # for field, value in current_mod[self.element_type][element_name].items():
    #             #     if field in self.frame_fields:
    #             #         # try:
    #             #         self.frame_fields[field].clear_val()
    #             #         self.frame_fields[field].set_val(value)
    #             """clearing is separate, because there are some double fields. like, appear twice,
    #              but are controlled by 1 element. so if first time it puts data, it will delete it afterwards"""
    #             for field in self.frame_fields:
    #                 self.frame_fields[field].clear_val()
    #             for field in self.frame_fields:
    #                 # try:
    #                 if field in GlobalVariables.current_mod[self.element_type][element_name]:
    #                     self.frame_fields[field].set_val(GlobalVariables.current_mod[self.element_type][element_name][field])
    #                     # TODO change labels colour back, but also include if displayed addition or not.
    #                     # self.frame_fields[field].label_change_colour('reset')
    #                     # except:
    #                     #     error_log('error in TemplatesPreparation in line 554')
    #                     #     error_log('problem with template data load for - ' + self.element_type)
    #                     #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))
    #
    #                 """optional off, as optional fields not fixed"""
    #                 # else:
    #                 #     GlobalVariables.optional_field.set_val(field, value)
    #     if 'Addition' in current_mod[self.element_type][element_name]:
    #         GlobalVariables.flag_addition = True
    #     if GlobalVariables.flag_addition:
    #         if not self.flag_fields_marked_for_addition:
    #             for field in self.addition_field_list:
    #                 self.frame_fields[field].label_change_colour('red')
    #             GlobalVariables.flag_fields_marked_for_addition = True
    #     else:
    #         if self.flag_fields_marked_for_addition:
    #             # TODO change reset - its not gray colour
    #             for field in self.addition_field_list:
    #                 self.frame_fields[field].label_change_colour(reset=True)
    #         GlobalVariables.flag_fields_marked_for_addition = False
    #         # except:
    #         #     print("could fix this some day. should not try to load details of a branch")
    #         #     print('Templates preparation  >!load element data def!')


    def load_element_data_old(self, elementType, elementName, current_mod):
        # print("function display element")
        # print('elementtype-  '+ elementType + ', element name - ' + elementName)
        if elementName == '':
            messagebox.showerror("Nothing", "No details to display", parent=self)
        else:
            # elementType == 'Items':
            try:
                # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
                #       for now try to avoid stuff not in template
                for field, value in current_mod[elementType][elementName].items():
                    if field in self.frame_fields[elementType]:
                        # print("field - " + str(field))
                        # print("value - " + str(value))
                        # value = re.sub('[^A-Za-z0-9]+', '', value)
                        # if isinstance(value, dict):
                        #     for field_A, value_A in value.items():
                        #         self.frame_fields[elementType][field][field_A].set_val(value_A)
                        #         print(field + ' ' + field_A + ' = ' + value_A.get())
                        # else:
                            # print(field + ' = ' + str(value))
                            self.frame_fields[elementType][field].set_val(value)
            except:
                print("could fix this some day. should not try to load details of a branch")
                print('Templates preparation  >!load element data def!')

    # TODO - verify later - if still needed
    def prepare_addition_fields(self, element_name, element_path):
        """disable edition of fields that do not have addiction tag in options and colour labels in....green?"""
        with open(GlobalVariables.startPath + '/'+element_path, encoding='utf-8-sig') as file:
            file_data = json.load(file, object_hook=OrderedDict)
        prepare_data = {self.element_type: {element_name: file_data}}
        self.load_element_data(element_name, prepare_data)
        for field in self.addition_field_list:
            self.frame_fields[field].label_change_colour('red')
        return
        # for field in self.frame_fields:


"""
    def prepItemGui_backup(self, master_name, element_type):
        # print(self.itemTemplate)
        # element_name = 'Items'
        rowsA = rowsB = columnC = rowsC = 0
        frame_singleline_fields = tk.Frame(master=master_name, bg='red')
        frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH)
        frame_listsboxes_fields = tk.Frame(master=master_name, bg='green')
        frame_listsboxes_fields.pack(side=tk.LEFT, fill=tk.BOTH)
        frame_optional_fields = tk.Frame(master=master_name, bg='purple')
        for field in self.json_templates[element_type]:
            # GuiFieldName = element_name + field
            if self.json_templates[element_type][field]["type"] in "text singlelist int filePath":
                field_value = createField(frame_singleline_fields, field, self.json_templates[element_type][field])
                self.frame_fields[element_type][field] = field_value
                rowsA += 1
            elif self.json_templates[element_type][field]["type"] in "multilist area":
                field_value = createField(frame_singleline_fields, field, self.json_templates[element_type][field])
                self.frame_fields[element_type][field] = field_value
                # print(GuiFieldName)
                rowsB += 3
            else:
                frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                label_field = tk.Label(master=frame_advancedFields, text=field)
                label_field.grid(row=0, column=0, columnspan=3)
                if self.json_templates[element_type][field]["tooltip"]:
                    CreateToolTip(label_field, self.json_templates[element_type][field]["tooltip"])
                rowsC += 1
                if self.json_templates[element_type][field]["type"] in 'dictionary':
                    # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                    # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                    # self.frame_fields['Items'][field] = {}
                    # label_field = tk.Label(master=frame_advancedFields, text=field)
                    # label_field.grid(row=rowsC, column=0, columnspan=2)
                    # rowsC += 1
                    advance_field = ExpandDictionaryField(self.json_templates[element_type][field],
                                                          frame_advancedFields, view_title=field)
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                #     elif self.template[field]["type"] in 'functionfield':
                #         # frame_advancedFields = tk.Frame(master=master_name, bg='blue')
                #         # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                #         # self.frame_fields['Items'][field] = {}
                #         # label_field = tk.Label(master=frame_advancedFields, text=field)
                #         # label_field.grid(row=rowsC, column=0, columnspan=2)
                #         # rowsC += 1
                #         functionflag = ''
                elif self.json_templates[element_type][field]["type"] in 'listDict':
                    advance_field = ListDictionaryField(self.json_templates[element_type][field], frame_advancedFields)
                    self.frame_fields[field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'deck':
                    advance_field = DeckField(frame_advancedFields)
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'monstergroups':
                    advance_field = MonsterGroups(frame_advancedFields,
                                                  self.json_templates[element_type][field]['options'])
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'speaker':
                    advance_field = Speaker(self.json_templates[element_type][field], frame_advancedFields)
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'FetisheApply':
                    advance_field = FetishApply(frame_advancedFields, self.json_templates[element_type][field])
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'PairFields':
                    advance_field = PerkDoubleList(self.json_templates[element_type][field], frame_advancedFields)
                    self.frame_fields[element_type][field] = advance_field
                    for field in self.json_templates[element_type][field]['fields'][1:]:
                        connected_field = RestOfPerks(field)
                        self.frame_fields[element_type][field['name']] = connected_field
                        advance_field.add_other_fields(connected_field)
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'skilltype':
                    advance_field = SkillsType(self.json_templates[element_type][field], frame_advancedFields,
                                               self.frame_fields[element_type])
                    self.frame_fields[element_type][field] = advance_field
                    columnC += 2
                    rowsC = 0
                elif self.json_templates[element_type][field]["type"] in 'optional':
                    advance_field = OptionalFields(self.json_templates[element_type][field], frame_advancedFields,
                                                   self.frame_fields[element_type], frame_optional_fields)
                else:
                    print("unknown type")
"""

class FetishesTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankFetish_modtemplate.json', 'Fetishes', master=master)

        self.size = [500, 620]

    def prep_template(self):
        self.input_filename.setEnabled(False)

    def save_element_details_in_current_mod(self, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True

    def save_element_in_file(self, file_name, file_path):
        """filename for fetishes is a list of all fetishes"""
        # file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][file_name]
        """fetish list is a one item dictionary of  list of dictionaries of fetishes
            create a template for fetish and saving in list, but as mod saving all to one file
            file data is dictionary of ordered dictionaries, so"""
        if file_name:
            temp_dictionary1 = {'FetishList': []}
            temp_dictionary2 = {'FetishList': []}
            elementPath = file_path
            if not access(elementPath, F_OK):
                makedirs(elementPath)
                # print(elementPath)
            for fetish in file_name:
                file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][fetish]
                if file_data['Type'] == 'Fetish':
                    temp_dictionary1["FetishList"].append(file_data)
                elif file_data['Type'] == 'Addiction':
                    temp_dictionary2["FetishList"].append(file_data)
            if temp_dictionary1['FetishList']:
                with open(elementPath + '0fetishList.json', 'w') as Fetishes_file:
                    Fetishes_file.write(json.dumps(temp_dictionary1, indent='\t'))
            if temp_dictionary2['FetishList']:
                with open(elementPath + 'addictionList.json', 'w') as Fetishes_file:
                    Fetishes_file.write(json.dumps(temp_dictionary2, indent='\t'))


class ItemTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankItem_modtemplate.json', 'Items', master=master)

        self.size = [1000, 620]
        # itemfileblank = 'files/_BlankItem_modtemplate.json'
        # with open(itemfileblank) as ItemBlank:
        #     self.template = json.load(ItemBlank, object_hook=OrderedDict)
        #     self.frame_gui_fields = {}

    def save_element_details_in_current_mod(self, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        if self.frame_fields['itemType'].get_val() == '':
            messagebox.showerror('missing type', 'Forgot type', parent=self)
            # messagebox.showinfo('missing type', 'Forgot type', master=self.frame_gui)
            return False
        self.save_data_in_current_mod(current_mod)
        return True
    def prepItemGui2(self):
        # element_name = 'Items'
        # functional_field_flag = [0, '']
        functional_field_repeat = None
        frame_singleline_fields = tk.Frame(self.frame_gui)
        frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        frame_advance_fields = tk.Frame(self.frame_gui)
        frame_advance_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')

        frame_ref_a = frame_singleline_fields
        frame_ref_b = frame_advance_fields


        frame_filename = tk.Frame(frame_ref_a)
        frame_filename.pack(fill=tk.BOTH)
        self.input_filename = SimpleEntry(frame_filename, 'File name', 'Provide name for file. If empty,'
                                                                       ' name without spaces will become file name.', 'L')
        self.input_filename.pack(fill='both')
        flag_switch = 1
        for field in self.json_templates:
            # GuiFieldName = element_name + field
            # try:
                if self.json_templates[field]["type"] in "text singlelist int filePath area requirement":
                    element_frame = frame_ref_a
                else:
                    element_frame = frame_ref_b
                # field_value = createField(element_frame, field, self.json_templates[field])
                field_value = createField(element_frame, field, self.json_templates[field])
                if field_value == '':
                    frame_advancedFields = tk.Frame(master=frame_ref_b, bg='blue')
                    frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
                    label_field = tk.Label(master=frame_advancedFields, text=field)
                    label_field.grid(row=0, column=0, columnspan=3)
                    # if 'tooltip' in self.json_templates[field]:
                    #     CreateToolTip(label_field, self.json_templates[field]['tooltip'])
                    # if self.json_templates[field]["type"] in 'PairFields':
                    #     advance_field = PerkDoubleList(self.json_templates[field], frame_advancedFields)
                    #     self.frame_fields[field] = advance_field
                    #     for field in self.json_templates[field]['fields'][1:]:
                    #         connected_field = RestOfPerks(field)
                    #         self.frame_fields[field['name']] = connected_field
                    #         advance_field.add_other_fields(connected_field)
                    # elif self.json_templates[field]["type"] in 'functionfield':
                    #     functionflag = ''
                    #     if self.element_type == 'Events':
                    #         functionflag = self.json_templates['CardType']
                    #     #     TODO somehow i need to know if this advance field in this element type was created already
                    #     #             if yes, then just add another branch with name of new field
                    #     #           answer - list with number of field name. add new field should add proper branch
                    #     """similar to perk double list, there are dummy objects of function field. They have reference
                    #      to main fields and their task to to set and get vals, by calling first function field"""
                    #     if functional_field_repeat:
                    #     # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                    #     #                                       field)
                    #         advance_field = Functional_Dummy(functional_field_repeat, field)
                    #         self.frame_fields[field] = advance_field
                    #         label_field.destroy()
                    #     else:
                    #         functional_field_repeat = FunctionField(functionflag, frame_advancedFields
                    #                                                 , view_title=field, label_field=label_field)
                    #         # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                    #         self.frame_fields[field] = functional_field_repeat
                    #         advance_field = Functional_Dummy(functional_field_repeat, field)
                    #     functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                    #                                               , dummy_field = advance_field)
                    # elif self.json_templates[field]["type"] in 'skilltype':
                    #     advance_field = SkillsType(frame_advancedFields, self.frame_fields, field)
                    #     self.frame_fields[field] = advance_field
                    # if self.json_templates[field]["type"] in 'optional':
                    #     advance_field = OptionalFields(self.json_templates[field], frame_advancedFields, self.dict_optional_fields,
                    #                                    frame_optional_fields)
                    #     self.optional_work = advance_field
                    continue
                self.frame_fields[field] = field_value


class LocationsTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankLocation_modtemplate.json', 'Locations', master=master)
        self.size = [800, 620]

    def save_element_details_in_current_mod(self, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True


class MonsterTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankMonster_modtemplate.json', 'Monsters', master=master)
        self.size = [800, 620]

    def save_element_details_in_current_mod(self, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True

    def prepItemGui_old_separate_tabs(self, mode=1):
        # if mode:
        #     self.frame_gui = self.frame_create_data
        #     self.frame_fields = self.fields_for_create_frame
        # else:
        #     self.frame_gui = self.frame_display_data
        #     self.frame_fields = self.fields_for_display_frame
        functional_field_repeat = None
        frame_advance_fields_1 = tk.Frame(self.frame_gui)
        frame_advance_fields_1.grid(row=1, column=1, columnspan=2)
        frame_advance_fields_2 = tk.Frame(self.frame_gui)
        frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')
        button_frame1 = tk.Button(self.frame_gui, text='Part 1', command=lambda:self.switch_frames(frame_advance_fields_1, frame_advance_fields_2))
        button_frame2 = tk.Button(self.frame_gui, text='Part 2',
                                  command=lambda: self.switch_frames(frame_advance_fields_2, frame_advance_fields_1))
        button_frame1.grid(row=0, column=1)
        button_frame2.grid(row=0, column=2)


        ref_frame = frame_advance_fields_1
        row_max_size=15
        currect_size = 0
        column_max = 3
        col_place = 1
        # visibility_frame = tk.Frame(frame_advance_fields_1)
        # visibility_frame.grid(row=0, column=0)
        # for idx in range(25):
        #     templabel = tk.Label(visibility_frame, text='row ' + str(idx))
        #     templabel.grid(row=idx)
        element_frame = tk.Frame(master=frame_advance_fields_1)
        element_frame.grid(row=0, column=col_place)
        # if mode:
        self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
                                                                       ' name without spaces will become file name.', 'L')
        # else:
        #     self.input_filename = SimpleEntryDisplay(element_frame, 'File name', 'Provide name for file. If empty,'
        #                                                                   ' name without spaces will become file name.',
        #                                       'L', None, None, self.element_type)
        # self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
        #                                                                ' name without spaces will become file name.', 'L')
        self.input_filename.pack(fill='both')
        flag_switch = 1
        for field in self.json_templates:
            # GuiFieldName = element_name + field
            # try:
            #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
            #         element_frame = temp_frame
            #     else:
            #         element_frame = temp_frame
                # field_value = createField(element_frame, field, self.json_templates[field])
                field_value = createField(element_frame, field, self.json_templates[field], template_name=self.element_type, mode=mode)
                # if field_value == '':
                #     continue
                # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
                if self.json_templates[field]["type"] in 'functionfield':
                    functionflag = ''
                    """similar to perk double list, there are dummy objects of function field. They have reference
                     to main fields and their task to to set and get vals, by calling first function field"""
                    if functional_field_repeat:
                        # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
                        #                                       field)
                        field_value.main_field = functional_field_repeat
                        self.frame_fields[field] = field_value
                        # label_field.destroy()
                    else:
                        functional_field_repeat = FunctionField(functionflag, master=element_frame, view_title=field)
                        # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
                        # self.frame_fields[field] = functional_field_repeat
                        field_value = Functional_Dummy(functional_field_repeat, field)
                        self.frame_fields[field] = field_value
                    functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                                              , dummy_field=field_value)
                    field_value = functional_field_repeat
                if field_value == '':
                    if self.json_templates[field]["type"] in 'optional' and mode == 1:
                        field_value = OptionalFields(self.frame_gui, self.json_templates[field])
                    else:
                        field_value = OptionalFields(self.frame_gui)
                    self.optional_class_worker = field_value
                    # continue

                #     if self.json_templates[field]["type"] == 'optional':
                #         field_value = OptionalFields(self.json_templates[field], element_frame, self.dict_optional_fields,
                #                                        frame_optional_fields)
                #         self.optional_work = field_value
                #         # advance_field.optional_fields_interface.pack()
                #     # print(advance_field.title + ' ' + str(advance_field.row_size))

                if isinstance(field_value, list):
                    self.frame_fields[field] = field_value[0]
                    self.frame_fields[field_value[1].title] = field_value[1]
                    field_value = field_value[0]
                else:
                    # if not self.json_templates[field]["type"] == 'optional' or self.json_templates[field]["type"] in 'functionfield':
                    if not self.json_templates[field]["type"] in 'functionfield optional':
                        self.frame_fields[field] = field_value
                # print(field_value.title + ' ' + str(field_value.row_size))
                field_value.pack(fill=tk.BOTH)
                currect_size += field_value.row_size
                if currect_size > 15:
                    currect_size = 0
                    col_place += 1
                    if col_place > column_max:
                        col_place = 0
                        ref_frame = frame_advance_fields_2
                    element_frame = tk.Frame(master=ref_frame)
                    element_frame.grid(row=0, column=col_place)
            # self.frame_fields[field] = field_value

    # def prepItemGui_backup_new(self):
    #     functional_field_repeat = None
    #     frame_advance_fields_1 = tk.Frame(self.frame_gui)
    #     frame_advance_fields_1.grid(row=1, column=1, columnspan=2)
    #     frame_advance_fields_2 = tk.Frame(self.frame_gui)
    #     frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')
    #     button_frame1 = tk.Button(self.frame_gui, text='Part 1', command=lambda:self.switch_frames(frame_advance_fields_1, frame_advance_fields_2))
    #     button_frame2 = tk.Button(self.frame_gui, text='Part 2',
    #                               command=lambda: self.switch_frames(frame_advance_fields_2, frame_advance_fields_1))
    #     button_frame1.grid(row=0, column=1)
    #     button_frame2.grid(row=0, column=2)
    #
    #
    #     ref_frame = frame_advance_fields_1
    #     row_max_size=15
    #     currect_size = 0
    #     column_max = 3
    #     col_place = 1
    #     visibility_frame = tk.Frame(frame_advance_fields_1)
    #     visibility_frame.grid(row=0, column=0)
    #     for idx in range(25):
    #         templabel = tk.Label(visibility_frame, text='row ' + str(idx))
    #         templabel.grid(row=idx)
    #     element_frame = tk.Frame(master=frame_advance_fields_1)
    #     element_frame.grid(row=0, column=col_place)
    #     self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
    #                                                                    ' name without spaces will become file name.', 'L')
    #     self.input_filename.pack(fill='both')
    #     flag_switch = 1
    #     for field in self.json_templates:
    #         # GuiFieldName = element_name + field
    #         # try:
    #         #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
    #         #         element_frame = temp_frame
    #         #     else:
    #         #         element_frame = temp_frame
    #             # field_value = createField(element_frame, field, self.json_templates[field])
    #             field_value = createField(element_frame, field, self.json_templates[field])
    #             # if field_value == '':
    #             #     continue
    #             # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
    #             if field_value == '':
    #                 frame_advancedFields = tk.Frame(master=element_frame, bg='blue')
    #                 frame_advancedFields.pack()
    #                 # frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #                 label_field = tk.Label(master=frame_advancedFields, text=field)
    #                 label_field.grid(row=0, column=0, columnspan=3)
    #                 if 'tooltip' in self.json_templates[field]:
    #                     CreateToolTip(label_field, self.json_templates[field]['tooltip'])
    #                 # if self.json_templates[field]["type"] in 'PairFields':
    #                 #     advance_field = PerkDoubleList(self.json_templates[field], element_frame)
    #                 #     self.frame_fields[field] = advance_field
    #                 #     for field in self.json_templates[field]['fields'][1:]:
    #                 #         connected_field = RestOfPerks(field)
    #                 #         self.frame_fields[field['name']] = connected_field
    #                 #         advance_field.add_other_fields(connected_field)
    #                 if self.json_templates[field]["type"] in 'functionfield':
    #                     functionflag = ''
    #                     """similar to perk double list, there are dummy objects of function field. They have reference
    #                      to main fields and their task to to set and get vals, by calling first function field"""
    #                     if functional_field_repeat:
    #                     # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
    #                     #                                       field)
    #                         advance_field = Functional_Dummy(functional_field_repeat, field)
    #                         self.frame_fields[field] = advance_field
    #                         label_field.destroy()
    #                     else:
    #                         functional_field_repeat = FunctionField(functionflag, frame_advancedFields
    #                                                                 , view_title=field, label_field=label_field)
    #                         # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
    #                         self.frame_fields[field] = functional_field_repeat
    #                         advance_field = Functional_Dummy(functional_field_repeat, field)
    #                     functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
    #                                                               , dummy_field = advance_field)
    #                     currect_size += functional_field_repeat.row_size
    #                 elif self.json_templates[field]["type"] in 'skilltype':
    #                     advance_field = SkillsType(frame_advancedFields, self.frame_fields, field)
    #                     self.frame_fields[field] = advance_field
    #                 elif self.json_templates[field]["type"] in 'optional':
    #                     advance_field = OptionalFields(self.json_templates[field], frame_advancedFields, self.dict_optional_fields,
    #                                                    frame_optional_fields)
    #                     self.optional_work = advance_field
    #                 print(advance_field.title + ' ' + str(advance_field.row_size))
    #                 continue
    #             else:
    #                 if isinstance(field_value, list):
    #                     self.frame_fields[field] = field_value[0]
    #                     self.frame_fields[field_value[1].title] = field_value[1]
    #                     field_value = field_value[0]
    #                 else:
    #                     self.frame_fields[field] = field_value
    #                 print(field_value.title + ' ' + str(field_value.row_size))
    #                 field_value.pack()
    #                 currect_size += field_value.row_size
    #                 if currect_size > 15:
    #                     currect_size = 0
    #                     col_place += 1
    #                     if col_place > column_max:
    #                         col_place = 0
    #                         ref_frame = frame_advance_fields_2
    #                     element_frame = tk.Frame(master=ref_frame)
    #                     element_frame.grid(row=0, column=col_place)
    #             # self.frame_fields[field] = field_value


    # def prepItemGui_backup(self):
    #     functional_field_repeat = None
    #     frame_singleline_fields = tk.Frame(self.frame_gui)
    #     frame_singleline_fields.grid(row=0, rowspan=5, column=0, sticky=tk.N)
    #     # frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    #     frame_advance_fields_1 = tk.Frame(self.frame_gui)
    #     frame_advance_fields_1.grid(row=1, column=1, columnspan=2)
    #     # frame_advance_fields_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #     frame_advance_fields_2 = tk.Frame(self.frame_gui)
    #     # frame_advance_fields_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #     # frame_singleline_fields = tk.Frame(master=self.frame_gui, bg='red')
    #     # frame_singleline_fields.pack(side=tk.LEFT, fill=tk.BOTH)
    #     frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')
    #     button_frame1 = tk.Button(self.frame_gui, text='Part 1', command=lambda:self.switch_frames(frame_advance_fields_1, frame_advance_fields_2))
    #     button_frame2 = tk.Button(self.frame_gui, text='Part 2',
    #                               command=lambda: self.switch_frames(frame_advance_fields_2, frame_advance_fields_1))
    #     button_frame1.grid(row=0, column=1)
    #     button_frame2.grid(row=0, column=2)
    #     frame_ref_a = frame_singleline_fields
    #     frame_ref_b = frame_advance_fields_1
    #     frame_ref_c = frame_advance_fields_2
    #
    #     frame_filename = tk.Frame(frame_ref_a)
    #     frame_filename.pack(fill=tk.BOTH)
    #     # self.input_filename = SimpleEntry(frame_filename, 'File name', 'Provide name for file. If empty,'
    #     #                                                                ' name without spaces will become file name.')
    #     self.input_filename = SimpleEntry(frame_filename, 'File name', 'Provide name for file. If empty,'
    #                                                                    ' name without spaces will become file name.',
    #                                       'L')
    #     self.input_filename.pack(fill='both')
    #     flag_switch = 1
    #     for field in self.json_templates:
    #         # GuiFieldName = element_name + field
    #         # try:
    #         if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
    #             element_frame = frame_ref_a
    #         elif self.json_templates[field]["type"] == 'dictionary':
    #             element_frame = frame_ref_c
    #         else:
    #             element_frame = frame_ref_b
    #         # field_value = createField(element_frame, field, self.json_templates[field])
    #         field_value = createField(element_frame, field, self.json_templates[field])
    #         if field_value == '':
    #             frame_advancedFields = tk.Frame(master=frame_ref_b, bg='blue')
    #             frame_advancedFields.pack(side=tk.LEFT, fill=tk.BOTH)
    #             label_field = tk.Label(master=frame_advancedFields, text=field)
    #             label_field.grid(row=0, column=0, columnspan=3)
    #             if 'tooltip' in self.json_templates[field]:
    #                 CreateToolTip(label_field, self.json_templates[field]['tooltip'])
    #             if self.json_templates[field]["type"] in 'PairFields':
    #                 advance_field = PerkDoubleList(self.json_templates[field], frame_advancedFields)
    #                 self.frame_fields[field] = advance_field
    #                 for field in self.json_templates[field]['fields'][1:]:
    #                     connected_field = RestOfPerks(field)
    #                     self.frame_fields[field['name']] = connected_field
    #                     advance_field.add_other_fields(connected_field)
    #             elif self.json_templates[field]["type"] in 'functionfield':
    #                 functionflag = ''
    #                 if self.element_type == 'Events':
    #                     functionflag = self.json_templates['CardType']
    #                 #     TODO somehow i need to know if this advance field in this element type was created already
    #                 #             if yes, then just add another branch with name of new field
    #                 #           answer - list with number of field name. add new field should add proper branch
    #                 """similar to perk double list, there are dummy objects of function field. They have reference
    #                  to main fields and their task to to set and get vals, by calling first function field"""
    #                 if functional_field_repeat:
    #                     # functional_field_repeat.add_new_field(self.json_templates[element_type][field]['fields'],
    #                     #                                       field)
    #                     advance_field = Functional_Dummy(functional_field_repeat, field)
    #                     self.frame_fields[field] = advance_field
    #                     label_field.destroy()
    #                 else:
    #                     functional_field_repeat = FunctionField(functionflag, frame_advancedFields
    #                                                             , view_title=field, label_field=label_field)
    #                     # advance_field.add_new_field(self.json_templates[element_type][field]['fields'], field)
    #                     self.frame_fields[field] = functional_field_repeat
    #                     advance_field = Functional_Dummy(functional_field_repeat, field)
    #                 functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
    #                                                       , dummy_field=advance_field)
    #             elif self.json_templates[field]["type"] in 'skilltype':
    #                 advance_field = SkillsType(frame_advancedFields, self.frame_fields, field)
    #                 self.frame_fields[field] = advance_field
    #             elif self.json_templates[field]["type"] in 'optional':
    #                 advance_field = OptionalFields(self.json_templates[field], frame_advancedFields,
    #                                                self.dict_optional_fields,
    #                                                frame_optional_fields)
    #                 self.optional_work = advance_field
    #             continue
    #         self.frame_fields[field] = field_value
    def switch_frames(self, frame_on, frame_off):
        frame_off.grid_forget()
        frame_on.grid(row=1, column=1, columnspan=2)
class PerkTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankPerk_modtemplate.json', 'Perks', master=master)
        self.size = [800, 620]

    def save_element_details_in_current_mod(self, current_mod):
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True

    def load_element_data(self, element_name, element_data=None):
        # print("function display element")
        # print('elementtype-  '+ elementType + ', element name - ' + elementName)
        if isinstance(element_data, str):
            temp = element_data.split('/')
            element_file_name = temp[-1][:-5]
            with open(GlobalVariables.Glob_Var.start_path + '/' + element_data, encoding='utf-8-sig') as file:
                element_data = json.load(file, object_hook=OrderedDict)
        if element_name == '':
            show_message("Nothing", "No details to display", 'Warning')
        else:
                if element_data is None:
                    element_data = GlobalVariables.Mod_Var.mod_data[self.element_type][element_name]
                    element_file_name = GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name]
                for field in self.frame_fields:
                        # try:
                    self.frame_fields[field].clear_val()
                    # try:
                    # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
                for field, value in element_data.items():
                    if field in self.frame_fields:
                        # try:
                        if field == 'StatReq':
                            self.frame_fields[field].set_val(element_data[field],
                                                             element_data['StatReqAmount'])
                        elif field == 'PerkType':
                            self.frame_fields[field].set_val(element_data[field],
                                                             element_data['EffectPower'])
                        else:
                            self.frame_fields[field].set_val(value)
                        # except:
                        #     error_log('error in TemplatesPreparation in line 554')
                        #     error_log('problem with template data load for - ' + self.element_type)
                        #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))

                    """temoporary off, as optional fields not fixed"""
                    # else:
                    #     GlobalVariables.optional_field.set_val(field, value)
            # except:
            #     print("could fix this some day. should not try to load details of a branch")
            #     print('Templates preparation  >!load element data def!')
    # def load_element_data(self, element_name, current_mod):
    #     # print("function display element")
    #     # print('elementtype-  '+ elementType + ', element name - ' + elementName)
    #     if element_name == '':
    #         messagebox.showerror("Nothing", "No details to display", parent=self)
    #     else:
    #             self.input_filename.set_val(element_name)
    #             for field in self.frame_fields:
    #                     # try:
    #                 self.frame_fields[field].clear_val()
    #                 # try:
    #                 # elementName = re.sub('[^A-Za-z0-9]+', '', elementName)
    #             for field, value in current_mod[self.element_type][element_name].items():
    #                 if field in self.frame_fields:
    #                     # try:
    #                     if field == 'StatReq':
    #                         self.frame_fields[field].set_val(current_mod[self.element_type][element_name][field],
    #                                                          current_mod[self.element_type][element_name]['StatReqAmount'])
    #                     elif field == 'PerkType':
    #                         self.frame_fields[field].set_val(current_mod[self.element_type][element_name][field],
    #                                                          current_mod[self.element_type][element_name]['EffectPower'])
    #                     else:
    #                         self.frame_fields[field].set_val(value)
    #                     # except:
    #                     #     error_log('error in TemplatesPreparation in line 554')
    #                     #     error_log('problem with template data load for - ' + self.element_type)
    #                     #     error_log('failed to load element data - ' + str(value) + ' to field = ' + str(field))
    #
    #                 """temoporary off, as optional fields not fixed"""
    #                 # else:
    #                 #     GlobalVariables.optional_field.set_val(field, value)
    #         # except:
    #         #     print("could fix this some day. should not try to load details of a branch")
    #         #     print('Templates preparation  >!load element data def!')


class SkillsTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankSkill_modtemplate.json', 'Skills', master=master)
        self.size = [800, 620]
        self.frame_list = []
        # self.mandatory_marked = '0'
        # self.mandatory_marked_prev = '0'
        self.attack_status_flag = 0
        self.status_flag = 0
        self.restrain_flag = 0
        # self.mandatory_sets = {
        #     '13':['power', 'minRange', 'maxRange', 'recoil', 'outcome', 'miss'],
        #     '23':['statusEffect', 'statusChance', 'statusDuration', 'statusPotency', 'statusResistedBy', 'statusText', 'statusOutcome', 'statusMiss'],
        #     '4':['restraintStruggle', 'restraintStruggleCharmed', 'retraintEscaped', 'retraintEscapedFail']
        # }
        self.attack_heal_mand = ['power', 'minRange', 'maxRange', 'recoil', 'outcome', 'miss']
        self.status_afflict_mand = ['statusEffect', 'statusChance', 'statusDuration', 'statusPotency', 'statusResistedBy', 'statusText', 'statusOutcome', 'statusMiss']
        self.status_restrain_mand = ['restraintStruggle', 'restraintStruggleCharmed', 'retraintEscaped', 'retraintEscapedFail']
    def save_data_in_current_mod(self, current_mod, flag_addition=False):
        # save element data into the current mod dictionary and add it into the lists.
        missing_data = ''
        for field in self.frame_fields:
            if self.frame_fields[field].label_custom.palette().color(QPalette.Background).name() == '#ff0000':
                if not self.frame_fields[field].get_val():
                    missing_data += '\n' + 'missing ' + field
        if missing_data:
            show_message('Missing mandatory',"You missed a few spots, didn't you?" + missing_data,'Mandatory error')
            return
        # self.save_data_in_current_mod(current_mod, flag_addition)
        return super().save_data_in_current_mod(current_mod, flag_addition)
        # return True

    def prepItemGui_old_separated_for_frames(self, mode=0):
        # if mode:
        #     self.frame_gui = self.frame_create_data
        #     self.frame_fields = self.fields_for_create_frame
        # else:
        #     self.frame_gui = self.frame_display_data
        #     self.frame_fields = self.fields_for_display_frame
        frame_fields_1 = tk.Frame(self.frame_gui)
        frame_fields_1.grid(row=1, column=1, columnspan=3)
        frame_fields_2 = tk.Frame(self.frame_gui)
        frame_fields_stance_control_keys = tk.Frame(self.frame_gui)
        self.frame_list = [frame_fields_1, frame_fields_2, frame_fields_stance_control_keys]
        frame_optional_fields = tk.Frame(master=self.frame_gui, bg='purple')
        button_frame1 = tk.Button(self.frame_gui, text='Part 1', command=lambda: self.switch_frames(0))
        button_frame2 = tk.Button(self.frame_gui, text='Part 2',
                                  command=lambda: self.switch_frames(1))
        button_frame3 = tk.Button(self.frame_gui, text='Stance and Control',
                                  command=lambda: self.switch_frames(2))
        button_frame1.grid(row=0, column=1)
        button_frame2.grid(row=0, column=2)
        button_frame3.grid(row=0, column=3)


        ref_frame = frame_fields_1
        row_max_size = 10
        currect_size = 0
        column_max = 3
        col_place = 0
        # visibility_frame = tk.Frame(frame_fields_1)
        # visibility_frame.grid(row=0, column=0)
        # for idx in range(25):
        #     templabel = tk.Label(visibility_frame, text='row ' + str(idx))
        #     templabel.grid(row=idx)
        element_frame = tk.Frame(master=frame_fields_1)
        element_frame.grid(row=0, column=col_place)
        if mode:
            self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
                                                                           ' name without spaces will become file name.', 'L')
        else:
            self.input_filename = SimpleEntryDisplay(element_frame, 'File name', 'Provide name for file. If empty,'
                                                                          ' name without spaces will become file name.',
                                              'L', None, None, self.element_type)
        # self.input_filename = SimpleEntry(element_frame, 'File name', 'Provide name for file. If empty,'
        #                                                                ' name without spaces will become file name.', 'L')
        self.input_filename.pack(fill='both')
        for field in self.json_templates:
            # GuiFieldName = element_name + field
            # try:
            #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
            #         element_frame = temp_frame
            #     else:
            #         element_frame = temp_frame
                # field_value = createField(element_frame, field, self.json_templates[field])
                field_value = createField(element_frame, field, self.json_templates[field], template_name=self.element_type, mode=mode)
                if field in 'skillType statusEffect':
                    field_value.var.trace('w', lambda *args, arg1=field, arg2=field_value: self.mark_mandatories(field_name=arg1, field_data=arg2))
                # if field_value == '':
                #     continue
                # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
                if field_value == '':
                    continue
                #     if self.json_templates[field]["type"] == 'optional':
                #         field_value = OptionalFields(self.json_templates[field], element_frame, self.dict_optional_fields,
                #                                        frame_optional_fields)
                #         self.optional_work = field_value
                #         # advance_field.optional_fields_interface.pack()
                #     # print(advance_field.title + ' ' + str(advance_field.row_size))
                if isinstance(field_value, list):
                    self.frame_fields[field] = field_value[0]
                    self.frame_fields[field_value[1].title] = field_value[1]
                    field_value = field_value[0]
                else:
                    if not self.json_templates[field]["type"] == 'optional':
                        self.frame_fields[field] = field_value
                # print(field_value.title + ' ' + str(field_value.row_size))
                field_value.pack(fill=tk.BOTH)
                currect_size += field_value.row_size
                if currect_size > row_max_size:
                    currect_size = 0
                    col_place += 1
                    if col_place > column_max:
                        col_place = 0
                        ref_frame = frame_fields_2
                    element_frame = tk.Frame(master=ref_frame)
                    element_frame.grid(row=0, column=col_place)
            # self.frame_fields[field] = field_value
        # self.frame_fields['skillType'].var.trace('w', lambda arg1='skillType', arg2 = )
        # self.frame_fields['statusEffect']
        currect_size = 0
        column_max = 4
        col_place = 0
        element_frame = tk.Frame(master=frame_fields_stance_control_keys)
        for field in GlobalVariables.optional_fields['skills']:
            field_value = createField(element_frame, field, GlobalVariables.optional_fields['skills'][field], template_name=self.element_type, mode=mode)
            # if field_value == '':
            #     continue
            # field_value.update_label('gird r-' + str(row_place) + ',col-'+str(col_place) + 'span-'+str(field_value.row_size))
            if field_value == '':
                continue
            field_value.pack(fill=tk.BOTH)
            self.frame_fields[field] = field_value
            currect_size += field_value.row_size
            if currect_size > 15:
                currect_size = 0
                col_place += 1
                element_frame = tk.Frame(master=frame_fields_stance_control_keys)
                element_frame.grid(row=0, column=col_place)

    def custom_fields_functionality(self):
        # return
        for field in self.frame_fields:
            # GuiFieldName = element_name + field
            # try:
            #     if self.json_templates[field]["type"] in "text singlelist int filePath multilist area requirement":
            #         element_frame = temp_frame
            #     else:
            #         element_frame = temp_frame
                # field_value = createField(element_frame, field, self.json_templates[field])
                if field in 'skillType statusEffect':
                    self.frame_fields[field].currentTextChanged.connect(lambda *args, arg1=field, arg2=self.frame_fields[field]: self.mark_mandatories(field_name=arg1, field_data=arg2))
                    self.frame_fields[field].set_val('Healing')
                    # field_value.var.trace('w', lambda *args, arg1=field, arg2=field_value: self.mark_mandatories(field_name=arg1, field_data=arg2))

    def switch_frames(self, frame_no):
        for frame in self.frame_list:
            frame.grid_forget()
        self.frame_list[frame_no].grid(row=1, column=1, columnspan=3)

    def mark_mandatories(self, field_name, field_data):
        if field_name == 'skillType':
            field_value = field_data.get_val()
            if field_value:
                if (field_value in 'attack Healing HealingEP HealingSP' and self.attack_status_flag == 1) or \
                   ('ff' in field_value and self.attack_status_flag == 2):
                    return
                else:
                    if field_value in 'attack Healing HealingEP HealingSP':
                        self.attack_status_flag = 1
                        for field in self.attack_heal_mand:
                            # self.frame_fields[field].field_label['text'] += '*'
                            # self.frame_fields[field].field_label.configure(bg='tomato')
                            self.frame_fields[field].label_custom.change_background_color()
                        if not self.status_flag:
                            for field in self.status_afflict_mand:
                                # self.frame_fields[field].field_label.configure(bg='snow')
                                self.frame_fields[field].label_custom.clear_color()

                    elif 'ff' in field_value:
                        self.attack_status_flag = 2
                        for field in self.attack_heal_mand:
                            # self.frame_fields[field].field_label.configure(bg='snow')
                            self.frame_fields[field].label_custom.clear_color()
                        for field in self.status_afflict_mand:
                            if '*' not in self.frame_fields[field].label_custom.text():
                                # self.frame_fields[field].field_label.configure(bg='tomato')
                                self.frame_fields[field].label_custom.change_background_color()
        if field_name == 'statusEffect':
            value = field_data.get_val()
            if value and value != 'None':
                self.status_flag = 1
                if self.attack_status_flag != 2:
                    for field in self.status_afflict_mand:
                        if '*' not in self.frame_fields[field].label_custom.text():
                                # self.frame_fields[field].field_label.configure(bg='tomato')
                                self.frame_fields[field].label_custom.change_background_color()
                    if 'Restrain' in value:
                        for field in self.status_restrain_mand:
                            if '*' not in self.frame_fields[field].label_custom.text():
                                # self.frame_fields[field].field_label.configure(bg='tomato')
                                self.frame_fields[field].label_custom.change_background_color()
                    else:
                        for field in self.status_restrain_mand:
                            # self.frame_fields[field].field_label.configure(bg='snow')
                            self.frame_fields[field].label_custom.clear_color()
            elif value == '' or value == 'None':
                self.status_flag = 0
                if self.attack_status_flag != 2:
                    for field in self.status_afflict_mand:
                        print('not all fields are fields: ' + str(field))
                        # self.frame_fields[field].field_label.configure(bg='snow')
                        self.frame_fields[field].label_custom.clear_color()





        # if self.mandatory_marked_prev != self.mandatory_marked:
        #     self.mandatory_marked_prev = self.mandatory_marked
        #     for fields in self.mandatory_sets:
        #         if fields == self.mandatory_marked:
        #             for field in self.mandatory_sets[fields]:
        #                 self.frame_fields[field].field_label['text'] += '*'

            # for field in self.mandatory_sets[fields]:
            #     self.frame_fields[field].field_label['text'].replace('*', '')
            # # for field in self.frame_fields:
            # #     if field in 'power minRange maxRange recoil outcome miss':
            #         self.frame_fields[field].field_label['text'] += '*'

    # def mark_mandatories(self, field_name, field_data, *args):
    #     # if self.mandatory_marked == 0:
    #     #     self.mandatory_marked =
    #     if field_name == 'skillType':
    #         field_value = field_data.get_val()
    #         if (field_value in 'attack Healing HealingEP HealingSP' and self.mandatory_marked == 1) or \
    #            ('ff' in field_value and self.mandatory_marked == 2):
    #             return
    #         else:
    #             if field_value in 'attack Healing HealingEP HealingSP':
    #                 self.mandatory_marked = '0'
    #             elif 'ff' in field_value:
    #                 self.mandatory_marked = '1'
    #
    #
    #     if field_name == 'statusEffect':
    #         value = field_data.get_val()
    #         if value:
    #
    #
    #
    #     if self.mandatory_marked_prev != self.mandatory_marked:
    #         self.mandatory_marked_prev = self.mandatory_marked
    #         for fields in self.mandatory_sets:
    #             if fields == self.mandatory_marked:
    #                 for field in self.mandatory_sets[fields]:
    #                     self.frame_fields[field].field_label['text'] += '*'
    #
    #         # for field in self.mandatory_sets[fields]:
    #         #     self.frame_fields[field].field_label['text'].replace('*', '')
    #         # # for field in self.frame_fields:
    #         # #     if field in 'power minRange maxRange recoil outcome miss':
    #         #         self.frame_fields[field].field_label['text'] += '*'


