import json
import re, copy
from os import makedirs
from os import access, F_OK
from collections import OrderedDict
from SimpleFields import SimpleEntry, mod_temp_data
from CustomFields import createField, OptionalFields, FunctionField, Functional_Dummy
    # , OptionalFields, FunctionField,
from otherFunctions import error_log, show_message
import GlobalVariables
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette


class Templates:
    def __init__(self, file_path_template, element_name, master=None):
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
        # self.widgets_in_template = {}
        # self.dict_optional_fields = {}
        self.file_template = file_path_template
        self.frame_fields = {}
        self.json_templates = {}
        self.element_type = element_name
        self.input_filename = None
        # self.addition_field = addition_field
        self.field_used_in_additions = []
        self.flag_additional_marking = False
        self.optional_class_worker = ''
        # self.size = []
        # self.flag_fields_marked_for_addition = False
        try:
            with open(self.file_template, encoding='utf-8-sig') as Blank:
                self.json_templates = json.load(Blank, object_hook=OrderedDict)
                # self.frame_fields = {}
        except Exception as e:
            show_message("template loading error", 'A issue has occured loading template ' +
                         self.file_template + '.\nTraceback:\n{0}'.format(str(e)), "")
            exit()

    def clear_template(self):
        self.input_filename.clear_val()
        for field in self.frame_fields:
            self.frame_fields[field].clear_val()

    def clear_markings(self):
        for field in self.field_used_in_additions:
            self.frame_fields[field].label_custom.clear_color()

    def custom_fields_functionality(self):
        return

    def load_element_data(self, element_name, element_data=None):
        """below is in case element data is just file name, but i dont see reason for this anymore
           ....oooo, its for addition loading"""
        element_file_name = ''
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
                if not element_file_name:
                    element_file_name = GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name]
                if self.element_type != 'Fetishes':
                    self.input_filename.set_val(element_file_name)
                """clearing is separate, because there are some double fields. like, appear twice,
                 but are controlled by 1 element. so if first time it puts data, it will delete it afterwards"""
                for field in self.frame_fields:
                    self.frame_fields[field].clear_val()
                for field in element_data:
                    # try:
                    if field in self.frame_fields:
                        try:
                            self.frame_fields[field].set_val(element_data[field])
                        except:
                            error_log('error in TemplatesPreparation in line 109')
                            error_log('problem with template data load for - ' + self.element_type)
                            error_log('failed to load element data - ' + str(element_data[field]) + ' to field = ' + str(field))
                    else:
                        self.optional_class_worker.set_val(field, element_data[field])

    def mark_additional_fields(self):
        """go over field in field for additions and mark labels in different colour.
        maybe even lock others?"""
        for field in self.field_used_in_additions:
            self.frame_fields[field].label_custom.change_background_color()

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
                                                            ' name without spaces will become file name.\n'
                                                            'Provide just file name to create folder'})
        self.input_filename.set_up_widget(layout_template)
        for field in self.json_templates:
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
                        field_value.main_field = functional_field_repeat
                        self.frame_fields[field] = field_value
                    else:
                        """if first time, create main field and dummy and assign it"""
                        functional_field_repeat = FunctionField(functionflag, master=None, view_title=field)
                        field_value = Functional_Dummy(functional_field_repeat, field)
                        self.frame_fields[field] = field_value
                    functional_field_repeat.add_new_field(self.json_templates[field]['fields'], field
                                                          , dummy_field=field_value)
                    field_value = functional_field_repeat
                if field_value == '':
                    if self.json_templates[field]["type"] in 'optional':
                        field_value = OptionalFields(self.main_widget, self.json_templates[field], self.main_template_layout)
                        self.optional_class_worker = field_value
                try:
                    field_value.set_up_widget(layout_template)
                except:
                    print('something wrong with set up widget')
                    print(field_value)
                    print(field)
                """set aside info if field is in addition"""
                if 'options' in self.json_templates[field]:
                    if 'addition' in self.json_templates[field]['options']:
                        self.field_used_in_additions.append(field)
                """now check if there are too many fields. each field has some size"""
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
        """save filename separately"""
        GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name] = file_name
        if flag_addition == 2:
            """yeah, instead of true false, i gave it numbers"""
            item_temp['Addition'] = 'Yes'
            """if addition, gather only data from used fields"""
            for field in self.field_used_in_additions:
                self.frame_fields[field].get_val(temp_dict_container=item_temp)
        else:
            for field, value in self.frame_fields.items():
                # print(self.templates[elementType][field].get())
                # print(self.templates[elementType][field].get_val())
                """IMPORTANT CHANGE!!!"""
                # itemTemp[field] = value.get_val()
                value.get_val(temp_dict_container=item_temp)
        current_mod[self.element_type][element_name] = item_temp
        return element_name

    def save_element_in_file(self, element_name, file_path):
        file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][element_name]
        file_name = GlobalVariables.Mod_Var.mod_file_names[self.element_type][element_name]
        elementPath = file_path
        if not access(elementPath, F_OK):
            makedirs(elementPath)
            # print(elementPath)
        # file_name = item_file_name
        file_name = re.sub('[^A-Za-z0-9]+', '', file_name)
        with open(elementPath + file_name + '.json', 'w') as objectF:
            objectF.write(json.dumps(file_data, indent='\t'))


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
        self.size = [800, 620]

    def load_element_data(self, element_name, element_data=None):
        mod_temp_data.current_editing_event = element_name
        super().load_element_data(element_name, element_data)

    def save_element_details_in_current_mod(self, current_mod):
        return
        # save element data into the current mod dictionary and add it into the lists.
        self.save_data_in_current_mod(current_mod)
        return True


class FetishesTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankFetish_modtemplate.json', 'Fetishes', master=master)
        self.size = [500, 620]

    def prep_template(self):
        self.input_filename.setEnabled(False)

    def save_element_in_file(self, fetish_list, file_path):
        """filename for fetishes is a list of all fetishes"""
        # file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][file_name]
        """fetish list is a one item dictionary of  list of dictionaries of fetishes
            create a template for fetish and saving in list, but as mod saving all to one file
            file data is dictionary of ordered dictionaries, so"""
        if fetish_list:
            temp_dictionary1 = {'FetishList': []}
            temp_dictionary2 = {'FetishList': []}
            if not access(file_path, F_OK):
                makedirs(file_path)
                # print(elementPath)
            for fetish in fetish_list:
                file_data = GlobalVariables.Mod_Var.mod_data[self.element_type][fetish]
                if file_data['Type'] == 'Fetish':
                    temp_dictionary1["FetishList"].append(file_data)
                elif file_data['Type'] == 'Addiction':
                    temp_dictionary2["FetishList"].append(file_data)
            if temp_dictionary1['FetishList']:
                with open(file_path + '0fetishList.json', 'w') as Fetishes_file:
                    Fetishes_file.write(json.dumps(temp_dictionary1, indent='\t'))
            if temp_dictionary2['FetishList']:
                with open(file_path + 'addictionList.json', 'w') as Fetishes_file:
                    Fetishes_file.write(json.dumps(temp_dictionary2, indent='\t'))


class ItemTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankItem_modtemplate.json', 'Items', master=master)
        self.size = [1000, 620]


class LocationsTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankLocation_modtemplate.json', 'Locations', master=master)
        self.size = [800, 620]


class MonsterTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankMonster_modtemplate.json', 'Monsters', master=master)
        self.size = [800, 620]

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

    def switch_frames(self, frame_on, frame_off):
        frame_off.grid_forget()
        frame_on.grid(row=1, column=1, columnspan=2)


class PerkTemplate(Templates):
    def __init__(self, master=None):
        super().__init__('files/_BlankPerk_modtemplate.json', 'Perks', master=master)
        self.size = [800, 620]

    def load_element_data(self, element_name, element_data=None):
        """there are 2 specific field - combined. take them out first
        then proceed with flow and after load those 2 fields"""
        if element_data is None:
            element_data = copy.copy(GlobalVariables.Mod_Var.mod_data[self.element_type][element_name])
        if 'StatReq' in list(element_data.keys()):
            f_stat_req = [element_data.pop('StatReq'), element_data.pop('StatReqAmount')]
        else:
            f_stat_req = []
        if 'PerkType' in list(element_data.keys()):
            f_perk_type = [element_data.pop('PerkType'), element_data.pop('EffectPower')]
        else:
            f_perk_type = []
        super().load_element_data(element_name, element_data)
        if f_stat_req:
            self.frame_fields['StatReq'].set_val(f_stat_req[0], f_stat_req[1])
        if f_perk_type:
            self.frame_fields['PerkType'].set_val(f_perk_type[0], f_perk_type[1])


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

    def save_data_in_current_mod(self, current_mod, flag_addition='1'):
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

    def custom_fields_functionality(self):
        for field in self.frame_fields:
                if field in 'skillType statusEffect':
                    self.frame_fields[field].currentTextChanged.connect(lambda *args, arg1=field, arg2=self.frame_fields[field]: self.mark_mandatories(field_name=arg1, field_data=arg2))
                    self.frame_fields[field].set_val('Healing')

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
                            self.frame_fields[field].label_custom.change_background_color()
                        if not self.status_flag:
                            for field in self.status_afflict_mand:
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