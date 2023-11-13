import otherFunctions
import GlobalVariables
import SimpleFields
#TODO function swap line if
from PyQt5 import QtCore, QtWidgets


class SceneSpeaks(SimpleFields.SingleList):
    def __init__(self, title_field):
        super().__init__(label_text='Speakers')
        """in these case, it should be only 1 word, so return empty value and instead update title field
        This is where user select speaker from event template but instead of name, it adds Speaker2, Speaker3"""
        self.title = 'Speakers'
        self.t_field = title_field
        temp_list = PrepareSpeakers()
        f_list = []
        for speaker in temp_list:
            f_list.append(speaker['name'])
        self.set_val(f_list, sort=False)
        self.currentTextChanged.connect(self.update_title)

    def get_val(self):
        return ''

    def update_title(self):
        cur_idx = self.currentIndex()
        if cur_idx == 0:
            cur_idx = ''
        self.t_field.set_val('Speakers' + str(cur_idx))


class StatCheckField(QtWidgets.QWidget):
    def __init__(self, master_frame=None, mod_elements_treeview=None):
        super().__init__(None)
        self.treeview_main_game_items = mod_elements_treeview
        master_frame.addWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        """first, setup basic field - stats, amount, success and fail scene. In order to put them nicely, 
        they'll done here"""
        self.basic_functions = []
        stat_layout = QtWidgets.QHBoxLayout()
        stats = SimpleFields.SingleList(None, 'Stats', {'choices': ["game-core stats-simple"]}, edit=False)
        stats.set_up_widget(stat_layout)
        self.basic_functions.append(stats)
        amount = SimpleFields.NumericEntry(None)
        amount.set_up_widget(stat_layout)
        self.main_layout.addLayout(stat_layout)
        self.basic_functions.append(amount)
        success = SimpleFields.MultiListDisplay(None, 'Success scene',
                                                field_data={'choices': ["Scenes-current"],
                                                            'options': ["single_item", "search"]},
                                                main_data_treeview=self.treeview_main_game_items)
        success.set_up_widget(self.main_layout)
        self.basic_functions.append(success)
        fail_text = SimpleFields.SimpleEntry(None)
        fail_text.set_val('Fail')  # this is hidden to save on space
        self.basic_functions.append(fail_text)
        fail = SimpleFields.MultiListDisplay(None, 'Fail scene',
                                             field_data={'choices': ["Scenes-current"],
                                                         'options': ["single_item", "search"]},
                                             main_data_treeview=self.treeview_main_game_items)
        fail.set_up_widget(self.main_layout)
        self.basic_functions.append(fail)
        """now, for subfunction, which should be very similar to use in menu and swap"""
        #
        #
        # self.menu_main_options = SimpleFields.SingleList(None, 'Options',
        #                                                  {'choices': ['blank', 'MaxMenuSlots', 'ShuffleMenu']}, edit=False)
        # self.menu_main_options.set_val('blank')
        # self.menu_main_options.set_up_widget(self.main_layout)
        # self.maxmenu_amount = SimpleFields.NumericEntry(None)
        # """to add options amount next to Single list"""
        # self.maxmenu_amount.set_up_widget(self.menu_main_options.custom_layout)
        # # self.options_amount.set_up_widget(self.main_layout)
        # self.maxmenu_amount.hide()
        # self.menu_main_options.currentTextChanged.connect(self.menu_slots)
        #
        # """second, text field called 'choices-scenes' its selection are scenes in current event.
        # Press enter to add new choice to menu - new branch to tree called same as scene"""
        #
        # self.choices_text = SimpleFields.MultiListDisplay(None, 'choices-scenes',
        #                               field_data={'choices': ["Scenes-current"], 'options': ["single_item", "search"]},
        #                               main_data_treeview=self.treeview_main_game_items)
        # self.choices_text.final_data.returnPressed.connect(self.new_choice)
        # self.choices_text.set_up_widget(self.main_layout)
        self.menu_conditions = SubFunction('StatCheck', mod_elements_treeview)
        self.main_layout.addWidget(self.menu_conditions)

        self.button_add_condition = SimpleFields.CustomButton(None, 'Add Condition')
        self.button_add_condition.clicked.connect(self.add_condition)
        self.main_layout.addWidget(self.button_add_condition)
        self.final_data = SimpleFields.ElementsList(None, 'Menu choices', all_edit=True)
        self.final_data.set_up_widget(self.main_layout)
        # self.prev_options = ''  # this was to avoid reloading field when selecting similar stuff. Too complicated.
        # self.options_row = 1

    def set_val(self, values_to_set_list):
        """should accept list of values"""
        """first 5 are basic value, next are conditions"""
        basic_vals = values_to_set_list[:5]
        for field, vals in zip(self.basic_functions, basic_vals):
            field.set_val(vals)
        conditions = values_to_set_list[5:]
        vals_to_add = []
        condition = ''
        for val in conditions:
            if val in self.menu_conditions.subfunctions:
                vals_to_add[val] = []
                condition = val
            else:
                vals_to_add[condition].append(val)
        self.final_data.add_data(vals_to_add)
        return

    def get_val(self):
        return_values = []
        """first get main options, then what was added in the data display"""
        for basic in self.basic_functions:
            return_values.append(basic.get_val())
        displayed_data_list = self.final_data.get_data()
        for choice in displayed_data_list:
            for choice_element in choice:
                choice_elements_list = choice[choice_element]
                return_values.append(choice_element)
                return_values += choice_elements_list
        self.final_data.clear_tree()
        return return_values

    def destroy(self):
        self.setParent(None)
        self.deleteLater()

    def add_condition(self):
        """add condition to choice. Choice is branch name in final data."""
        conditions = self.menu_conditions.get_val()  # this will be list, 0 - option, rest are values
        new_branch = self.final_data.add_branch(conditions[0])
        self.final_data.add_data_to_display(conditions[1:], new_branch)


class MenuField(QtWidgets.QWidget):
    def __init__(self, master_frame=None, mod_elements_treeview=None):
        super().__init__(None)
        self.treeview_main_game_items = mod_elements_treeview
        master_frame.addWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        """first, menu options - MaxMenuSlots and ShuffleMenu"""
        self.menu_main_options = SimpleFields.SingleList(None, 'Options',
                                                         {'choices': ['blank', 'MaxMenuSlots', 'ShuffleMenu']},
                                                         edit=False)
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
                                                          field_data={'choices': ["Scenes-current"],
                                                                      'options': ["single_item", "search"]},
                                                          main_data_treeview=self.treeview_main_game_items)
        self.choices_text.final_data.setToolTip('Click here, then double click on scene from list above.\n'
                                                'Then press enter here to add scene to list below.')
        self.choices_text.final_data.returnPressed.connect(self.new_choice)
        self.choices_text.set_up_widget(self.main_layout)

        """now make creator of choices conditions. This has lots of options"""
        # conditions_list = ['', 'FinalOption', 'EventJump', 'HideOptionOnRequirementFail', 'InverseRequirement',
        #                 'RequiresStat','RequiresItem', 'RequiresSkill', 'RequiresPerk', 'RequiresEnergy',
        #                 'RequiresVirility', 'RequiresItemEquipped', 'RequiresTime', 'RequiresFetishLevelEqualOrGreater',
        #                 'RequiresFetishLevelEqualOrLess', 'RequiresMinimumProgress', 'RequiresMinimumProgressFromEvent',
        #                 'RequiresLessProgress', 'RequiresLessProgressFromEvent', 'RequiresChoice',
        #                 'RequiresChoiceFromEvent']
        # conditions_list.sort()
        # since I created subfunction, above should be obsolete now.
        self.menu_conditions = SubFunction('Menu', mod_elements_treeview)
        self.main_layout.addWidget(self.menu_conditions)
        """here is where all is displayed"""
        self.button_add_condition = SimpleFields.CustomButton(None, 'Add Condition')
        self.button_add_condition.clicked.connect(self.add_condition)
        self.main_layout.addWidget(self.button_add_condition)
        self.final_data = SimpleFields.ElementsList(None, 'Menu choices', all_edit=True)
        self.final_data.set_up_widget(self.main_layout)
        # self.prev_options = ''
        # self.options_row = 1

    def set_val(self, values_to_set_list):
        """should accept list of values"""
        """first check for main menu options"""
        length_of_list = len(values_to_set_list)
        start_checking = 0
        if values_to_set_list[start_checking] in 'MaxMenuSlots ShuffleMenu':
            value = values_to_set_list[start_checking]
            if value == 'MaxMenuSlots':
                start_checking = 2
                self.menu_main_options.set_val('MaxMenuSlots')
                self.maxmenu_amount.set_val(int(values_to_set_list[1]))
            elif value == 'ShuffleMenu':
                self.menu_main_options.set_val('ShuffleMenu')
                start_checking = 1
        # choices_no = 1
        temp_list = []
        skip_no = 0
        for index in range(start_checking, length_of_list):
            if skip_no > 0:
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
                parent = self.final_data.add_branch(selected_option)
                temp_list.pop(-1)
                self.final_data.add_data_to_display(temp_list, parent)
                temp_list.clear()
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
                """for MENU, scene title goes last, after conditions"""
                choice_elements_list = choice[choice_element]
                return_values += choice_elements_list
                return_values.append(choice_element)
        self.final_data.clear_tree()
        return_values.append('EndLoop')
        return return_values

    def clear_val(self):
        return

    def destroy(self):
        self.setParent(None)
        self.deleteLater()

    def new_choice(self):
        new_choice = self.choices_text.get_val()
        if new_choice:
            self.final_data.add_data(new_choice)

    def add_condition(self):
        """add condition to choice. Choice is branch name in final data."""
        selected_choice_name = self.final_data.selected_element()
        if selected_choice_name:
            conditions = self.menu_conditions.get_val() # this will be list, 0 - option, rest are values
            if conditions[0] not in ['', 'FinalOption', 'EventJump', 'HideOptionOnRequirementFail', 'InverseRequirement']:
                conditions[0] = 'Requires' + conditions[0]
            self.final_data.add_data_to_display(conditions, selected_choice_name)
        else:
            otherFunctions.show_message('Condition placement', 'Press "enter" on selected scene to add new condition.\n'
      
                                                               'Then select added scene to add condition to it', '')
    def menu_slots(self, slots_val):
        if slots_val == 'MaxMenuSlots':
            self.maxmenu_amount.show()
        else:
            self.maxmenu_amount.hide()
    # def menu_choice_options(self, selected_option):
    #     # selected_option = self.menu_choice_list.get_val()
    #     if selected_option not in self.prev_options:
    #         self.clear_fields()
    #         self.prev_options = selected_option
    #         if selected_option in 'FinalOption HideOptionOnRequirementFail InverseRequirement':
    #             self.prev_options = 'FinalOption HideOptionOnRequirementFail InverseRequirement'
    #             self.selected_filter_fields = []
    #         elif selected_option in 'RequiresMinimumProgress RequiresLessProgress RequiresEnergy RequiresVirility':
    #             self.prev_options = 'RequiresMinimumProgress RequiresLessProgress RequiresEnergy RequiresVirility'
    #             self.setup_int()
    #         elif selected_option in 'RequiresFetishLevelEqualOrGreater RequiresFetishLevelEqualOrLess RequiresStat':
    #             self.setup_list_int()
    #         elif selected_option in 'RequiresItem RequiresItemEquipped RequiresPerk RequiresSkill':
    #             self.setup_multi()
    #         elif selected_option in 'RequiresMinimumProgressFromEvent RequiresLessProgressFromEvent':
    #             self.prev_options = 'RequiresMinimumProgressFromEvent RequiresLessProgressFromEvent'
    #             self.setup_int_multi()
    #         elif selected_option in 'RequiresTime':
    #             self.setup_list()
    #         elif selected_option == 'RequiresChoice':
    #             self.set_up_choice('current')
    #         elif selected_option == 'RequiresChoiceFromEvent':
    #             self.set_up_choice('event')
    #         else:
    #             # self.prev_options = 'EventJump ThenJumpToScene' - thise should be together, not separate
    #             self.prev_options = 'EventJump'
    #             self.setup_scene()
    # def clear_fields(self):
    #     for field in self.fields_list:
    #         self.fields_list[field].hide()
    #         self.fields_list[field].clear_val()
    # def setup_int(self):
    #     self.fields_list['int'].show()
    #     # self.fields_list['int'].grid(row=self.options_row, column=2)
    #     self.selected_filter_fields = ['int']
    # def setup_list_int(self):
    #     self.fields_list['list1'].show()
    #     # self.fields_list['list1'].grid(row=self.options_row, column=2)
    #     data_to_load = self.menu_conditions.get_val()
    #     if 'Stat' in data_to_load:
    #         # values = GlobalVariables.Glob_Var.game_hard_data
    #         values = otherFunctions.getListOptions(['game-core stats-simple'], 'single')
    #     else:
    #         values = otherFunctions.getListOptions(['Fetishes'], 'single')
    #         # values = otherFunctions.getListOptions(['Fetishes'], 'single')
    #     self.fields_list['list1'].reload_options(values)
    #     self.fields_list['int'].show()
    #     # self.fields_list['int'].grid(row=self.options_row, column=3)
    #     self.selected_filter_fields = ['list1', 'int']
    # def setup_list(self):
    #     self.fields_list['list1'].show()
    #     # self.fields_list['list1'].grid(row=self.options_row, column=2)
    #     self.fields_list['list1'].reload_options(["Day", "Night", "DayFaked", "DayTrue", "NightFaked", "NightTrue", "Morning", "Noon", "Afternoon", "Dusk", "Evening", "Midnight"])
    #     self.selected_filter_fields = ['list1']
    # def setup_multi(self):
    #     self.fields_list['multi'].show()
    #     data_to_load = self.menu_conditions.get_val()
    #     if 'Item' in data_to_load:
    #         data_to_load = 'Items'
    #     elif 'Perk' in data_to_load:
    #         data_to_load = 'Perks'
    #     elif 'Skill' in data_to_load:
    #         data_to_load = 'Skills'
    #     self.fields_list['multi'].selection_type = data_to_load
    #     self.treeview_main_game_items.disconnect_multilist()
    #     self.selected_filter_fields = ['multi']
    # def setup_int_multi(self):
    #     self.fields_list['multi'].show()
    #     self.fields_list['int'].show()
    #     self.fields_list['multi'].selection_type = 'Events'
    #     self.fields_list['multi'].label_custom.setText('Events')
    #     self.selected_filter_fields = ['multi', 'int']
    # def setup_scene(self):
    #     data_to_load = self.menu_conditions.get_val()
    #     if data_to_load == 'EventJump':
    #         # if eventjump, need to set first multilist display for events.
    #         # second multi could display scenes. either from current event - "choice" options, or from selected event from eventjump - first multi
    #         values = ['Events']
    #
    #         self.fields_list['multi'].label_custom.setText('Events')
    #         self.fields_list['multi'].selection_type = 'Events'
    #         self.fields_list['multi'].show()
    #         # self.fields_list['multi'].var.trace_id = self.fields_list['multi'].var.trace('w', lambda *args: self.special_event_jumping_load_scenes_to_list(''))
    #         self.fields_list['multi'].final_data.function_on_modify(self.special_event_jumping_load_scenes_to_list)
    #         self.fields_list['check'].show()
    #         self.selected_filter_fields = ['multi', 'check']
    #     #     Else below never happens, since this reacts to option value, which is only EventText. Scene is a checkbox
    #     # else:
    #     #     self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
    #     #     # values = ['Scenes']
    #     #     # self.fields_list['multi2'].update_list(values)
    #     #     self.fields_list['multi2'].show()
    #     #     # self.fields_list['multi2'].grid(row=self.options_row, column=2)
    #     #     self.selected_filter_fields = ['multi2']
    #     # # values = otherFunctions.getListOptions(['currentmod-Events'], 'multi')
    #     # # self.fields_list['multi'].update_list(values)
    #
    #     # self.fields_list['multi'].grid(row=self.options_row, column=3)
    # def set_up_scene_field(self):
    #     flag_trigger = self.fields_list['check'].get_val()
    #     if flag_trigger:
    #         self.fields_list['multi2'].show()
    #         # self.fields_list['multi2'].grid(row=1, column=5)
    #         self.selected_filter_fields.append('multi2')
    #     else:
    #         self.fields_list['multi2'].hide()
    #         if len(self.selected_filter_fields) == 5:
    #             self.selected_filter_fields.pop()
    # def set_up_choice(self, with_event):
    #     self.selected_filter_fields = ['list1', 'list2']
    #     choice_startup = 'current'
    #     if with_event == 'event':
    #         self.fields_list['multi'].selection_type = 'Events'
    #         self.fields_list['multi'].label_custom.setText('Events')
    #         self.fields_list['multi'].show()
    #         self.selected_filter_fields.insert(0, 'multi')
    #         choice_startup = 'Event'
    #
    #     self.fields_list['list1'].show()
    #     self.fields_list['list2'].show()
    #     self.Special_Set_Up_Choices_Fields(choice_startup)
    #
    # def Special_Set_Up_Choices_Fields(self, function_name):
    #     if 'Event' in function_name:
    #         """if event, link first multi field with function to find choices based on event"""
    #         # self.fields_list['list1'].clear_val()
    #         # otherFunctions.duplicate_treeview(GlobalVariables.list_elementlists[1].treeview,
    #         #                                   self.function_fields_list[0].tree_options_choose.treeview,
    #         #                                   destination_leaf='mod-Events')
    #         # self.fields_list['multi'].var.trace_id =\
    #         #     self.fields_list['multi'].var.trace("w", lambda *args, arg1='true': self.special_set_up_choices_1(arg1))
    #         self.fields_list['multi'].final_data.function_on_modify(self.special_set_up_choices_1)
    #     else:
    #         """if not event, then return choices from current scene"""
    #
    #         event_name = SimpleFields.mod_temp_data.current_editing_event
    #         self.prev_options = event_name
    #         self.special_set_up_choices_1()
    #     """first field should be choice number, second field should be choice text"""
    #     # # self.function_fields_list[field_order].var.trace_add("write", lambda order: self.Special_Set_Up_Choices_2(field_order))
    #     self.fields_list['list1'].currentTextChanged.connect(self.Special_Set_Up_Choices_2)
    #     # self.fields_list['list1'].var.trace_id =\
    #     #     self.fields_list['list1'].var.trace("w", lambda *args: self.Special_Set_Up_Choices_2())
    #     # self.fields_list['list1'].delete_place = 'gate'
    #     # self.fields_list['list2'].delete_place = 'choice'
    #     # self.fields_list['list2'].choice_no_field = self.fields_list['list1']
    #     # self.fields_list['list2'].currentTextChanged.connect(self.Special_Set_Up_Choices_2_1)
    #     # self.fields_list['list2'].var.trace_id = self.fields_list[
    #     #     'list2'].var.trace("w", lambda *args: self.Special_Set_Up_Choices_2_1())
    #
    #     # old version, when it searched on the spot
    #     # choices_list = []
    #     # if 'Event' in function_name:
    #     #     return
    #     # else:
    #     #     if self.event == 'EventText':
    #     #         element = 'Events'
    #     #     else:
    #     #         element = 'Monsters'
    #     #     list_of__dictionary_scenes = GlobalVariables.templates[element].frame_fields[self.event].get_val()
    #     #     for dictionary_scene in list_of__dictionary_scenes:
    #     #         theText = dictionary_scene['theScene']
    #     #         index = 0
    #     #         for texts in theText:
    #     #             if len(texts) == 9:
    #     #                 if texts == 'SetChoice':
    #     #                     choices_list.append(theText[index+1])
    #     #             index += 1
    #     #     self.function_fields_list[1].reload_options(choices_list)
    #
    # def special_set_up_choices_1(self):
    #     if 'multi' in self.selected_filter_fields:
    #         """this means choices should be set by event name in first field"""
    #         event_name = self.fields_list['multi'].get_val()
    #         self.prev_options = event_name
    #     """first field should be choice number, second field should be choice text"""
    #     choice_list = SimpleFields.mod_temp_data.get_choices(get_val='gate', event_name=self.prev_options)
    #     self.fields_list['list1'].reload_options(choice_list)
    #     # self.fields_list['list1'].event_name = event_name
    #     choice_list = SimpleFields.mod_temp_data.get_all_choices_text(event_name=self.prev_options)
    #     self.fields_list['list2'].reload_options(choice_list)
    #     # self.fields_list['list2'].event_name = event_name
    #
    # def Special_Set_Up_Choices_2(self, choice_gate):
    #     """get choice number and load choices text"""
    #     # choice_text = self.fields_list['list2'].get_val()
    #     # if not choice_text:
    #     # choice_gate = choice_no
    #     # choice_gate = self.fields_list['list1'].get_val()
    #     if choice_gate:
    #         choices_list = SimpleFields.mod_temp_data.get_choices(get_val=choice_gate, event_name=self.prev_options)
    #         self.fields_list['list2'].reload_options(choices_list)
    #
    # # def Special_Set_Up_Choices_2_1(self):
    # #     """get choice text and load its number"""
    # #     choice_no = self.fields_list['list1'].get_val()
    # #     if not choice_no:
    # #         choice_text = self.fields_list['list2'].get_val()
    # #         if choice_text:
    # #             choices_no = SimpleFields.mod_temp_data.get_gates(choice=choice_text, event_name=self.prev_options)
    # #             self.fields_list['list1'].set_val(choices_no)
    #
    #     return
    # def special_event_jumping_load_scenes_to_list(self, event, flag_current_event=False):
    #     self.fields_list['multi2'].clear_val()
    #     if flag_current_event:
    #         self.treeview_main_game_items.scene_source = 'current'
    #         # event_name = GlobalVariables.templates['Events'].frame_fields['name'].get_val()
    #         # list_of_dictionary_scenes = GlobalVariables.Mod_Var.templates['Events'].frame_fields['EventText'].get_val()
    #         # for scene in list_of_dictionary_scenes:
    #         #     # self.fields_list['multi2'].tree_options_choose.treeview.insert('mod-Scenes', 'end', text=scene['NameOfScene'])
    #         #     self.fields_list['multi2'].tree_options_choose.treeview.insert('', 'end', text=scene['NameOfScene'])
    #         # return
    #     # selected_item = self.fields_list['multi'].tree_options_choose.treeview.selection()
    #     selected_event = self.fields_list['multi'].get_val()
    #     if selected_event:
    #         self.treeview_main_game_items.scene_source = selected_event
    #         # self.fields_list['multi2'].clear_val('all')
    #         # selected_event = self.fields_list['multi'].tree_options_choose.treeview.item(selected_item)['text']
    #         # scenes_list = GlobalVariables.current_mod['Events'][selected_event]['EventText']
    #         # temp_scene_names = []
    #         # for scene in scenes_list:
    #         #     self.fields_list['multi2'].tree_options_choose.treeview.insert('', 'end',
    #         #                                                                      text=scene['NameOfScene'])
    #         # temp_scene_names.append(scene['NameOfScene'])
    #     # self.function_fields_list[2].treeview_optionstochoose.treeview.insert('', 'end',values=temp_scene_names)


# TODO remove later if nothing breaks
class MenuField_backup_working(QtWidgets.QWidget):
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
                return_values.append(choice_element)
                return_values += choice_elements_list
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
        else:
            otherFunctions.show_message('Condition placement', 'Press enter on selected scene to add new condition.\n'
                                                               'Then select added scene to add condition to it', '')
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


class Choices:
    def __init__(self, event_field=None):
        self.field_choice_no = SimpleFields.InputList(field_name='Choice')
        self.field_choice_no.field.setMaximumWidth(60)
        self.field_choice_text = SimpleFields.InputList(field_name='Text')
        self.event_source = ''
        self.event_source_field = None
        # TODO here is not working in case it should take from another event
        if event_field:
            self.event_source_field = event_field
            self.event_source_field.final_data.function_on_modify(self.set_up_event_source)
        else:
            self.event_source = SimpleFields.mod_temp_data.current_editing_event
            self.set_up_event_source()
        self.field_choice_no.field.currentTextChanged.connect(self.set_up_choices_text)
        self.field_choice_no.delete_place = 'gate'
        self.field_choice_text.delete_place = 'choice'
        self.field_choice_text.choice_no_field = self.field_choice_no

    def set_up_event_source(self):
        if self.event_source_field:
            self.event_source = self.event_source_field.get_val()
            # print("updating event source. seems like event source field is not connecting to this function")
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


class CombatEncounter(QtWidgets.QWidget):
    def __init__(self, master_frame=None, mod_elements_treeview=None):
        super().__init__(None)
        self.treeview_main_game_items = mod_elements_treeview
        master_frame.addWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        """first, menu options - MaxMenuSlots and ShuffleMenu"""
        self.menu_main_options = SimpleFields.SingleList(None, 'Options',
                                                         {'choices': ['blank', 'NoRunning', 'RunningWontSkipEvent',
                                                                      'SetBGOnRun', 'DenyInventory']}, edit=False)
        self.menu_main_options.set_val('blank')
        self.menu_main_options.set_up_widget(self.main_layout)
        self.background_file = SimpleFields.FileField(None, 'Background')
        """to add options amount next to Single list"""
        self.background_file.set_up_widget(self.menu_main_options.custom_layout)
        self.background_file.hide()
        self.menu_main_options.currentTextChanged.connect(self.menu_background)
        """second, text field called 'monsters' its selection are monsters.
        Press enter to add new choice to menu - new branch to tree called same as scene"""
        self.choices_text = SimpleFields.MultiListDisplay(None, 'Monsters',
                                                          field_data={'choices': ["Monsters"],
                                                                      'options': ["single_item", "search"]},
                                                          main_data_treeview=self.treeview_main_game_items,
                                                          single_edit=False)
        self.choices_text.final_data.returnPressed.connect(self.new_choice)
        self.choices_text.set_up_widget(self.main_layout)

        """there are only 2 conditions:apply stance and restrainer, where later is just word"""
        """if only 2 options, stance will be similar to first field, also with 'enter' to add.
        Restrainer might as well be a simple button"""
        layout_buttons = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(layout_buttons)
        """first stances"""
        self.stances = SimpleFields.MultiListDisplay(None, 'Stances',
                                                     field_data={'choices': ["Stances"],
                                                                 'options': ["single_item", "search"]},
                                                     main_data_treeview=self.treeview_main_game_items, single_edit=False)
        self.stances.set_up_widget(layout_buttons)
        self.stances.final_data.function_on_modify(self.add_condition)
        self.button_restrainer = SimpleFields.CustomButton(None, "RESTRAINER")
        self.button_restrainer.clicked.connect(self.add_condition)
        layout_buttons.addWidget(self.button_restrainer)
        """here is where all is displayed"""
        self.prev_options = ''
        self.options_row = 1
        self.final_data = SimpleFields.ElementsList(None, 'Encounters', all_edit=True)
        self.final_data.set_up_widget(self.main_layout)

    def set_val(self, values_to_set_list):
        """should accept list of values"""
        """first check for main menu options"""
        length_of_list = len(values_to_set_list)
        if values_to_set_list[0] in 'NoRunning RunningWontSkipEvent SetBGOnRun DenyInventory':
            value = values_to_set_list.pop(0)
            if value == 'SetBGOnRun':
                self.menu_main_options.set_val(value)
                self.background_file.set_val(values_to_set_list.pop(0))
            elif value == 'NoRunning RunningWontSkipEvent DenyInventory':
                self.menu_main_options.set_val(value)
        skip_no = 0
        """now start checking for all conditional choices"""
        for index in range(0, length_of_list):
            if skip_no >= 0:
                skip_no -= 1
                continue
            selected_option = values_to_set_list[index]
            if selected_option in 'Restrainer':
                self.final_data.add_leaf([selected_option], None, current_leaf)
                continue
            elif selected_option in 'ApplyStance':
                self.final_data.add_leaf([selected_option, values_to_set_list[index + 1]], None, current_leaf)
                skip_no = 1
            else:
                current_leaf = self.final_data.add_branch(selected_option)
        return

    def get_val(self):
        return_values = []
        """first get main options, then what was added in the data display"""
        main_options = self.menu_main_options.get_val()
        if main_options != 'blank':
            return_values.append(main_options)
            if main_options == 'SetBGOnRun':
                return_values.append(self.background_file.get_val())
        displayed_data_list = self.final_data.get_data()
        for choice in displayed_data_list:
            for choice_element in choice:
                choice_elements_list = choice[choice_element]
                return_values.append(choice_element)
                return_values += choice_elements_list

        return return_values

    def destroy(self):
        self.setParent(None)
        self.deleteLater()

    def set_up_widget(self, outside_layout, insert_for_options=False, insert_pos=0):
            if insert_for_options:
                if insert_pos == 0:
                    insert_pos = outside_layout.count() - 1
                outside_layout.insertLayout(insert_pos, self.custom_layout)
            else:
                outside_layout.addWidget(self)

    def new_choice(self):
        current_leaves = self.final_data.tree_model.children()
        if len(current_leaves) == 12:
            otherFunctions.show_message("Monster Limit", "Too many enemies. Cannot add more", '')
            return
        new_choice = self.choices_text.get_val()
        self.final_data.add_data(new_choice)

    def add_condition(self, flag=None):
        """little gimmick - change button title to stances"""
        if flag or flag == '':
            """button was clicked"""
            if flag != '':
                self.button_restrainer.setText('Apply stance')
            else:
                self.button_restrainer.setText('Restrainer')
            return
        """add condition to choice. Choice is branch name in final data."""
        selected_choice_name = self.final_data.selected_element()
        # TODO check if below works with IS
        if selected_choice_name and selected_choice_name.parent() is None:
            value = self.stances.get_val()
            """check if stance was selected. if yes, add stance and clear field, if not, add restrainer"""
            if value == '':
                self.final_data.add_data_to_display('Restrainer', selected_choice_name)
            else:
                """here get stance"""
                self.final_data.add_data_to_display('ApplyStance', selected_choice_name)
                self.final_data.add_data_to_display(value, selected_choice_name)
                self.stances.clear_val()
            return

    def menu_background(self, val):
        if val == 'SetBGOnRun':
            self.background_file.show()
        else:
            self.background_file.hide()


# this is just for testing stuff
class FunctionTests(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Events')
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
        # TODO for some reason, when this is created, other function after it are created at the bottom of main layout instead of the top. maybe remake it similar to menu, as a widget
        """main idea:
        first line - dropdown with options
        second line - will create fields according to above. mostly int and text, sometime input with staff from tree
        last line - element tree with columns, all editable"""
        self.main_layout = main_layout
        # options = {'choices': ["","Random", "Stat", "Arousal", "MaxArousal", "Energy", "MaxEnergy", "Virility",
        #                         "HasFetish", "HasFetishLevelEqualOrGreater", "Perk", "EncounterSize", "Item", "Eros",
        #                         "IfTimeIs", "Progress", "OtherEventsProgress", "Choice", "OtherEventsChoice"]
        #            }
        self.list_fields_not_going_to_treeview = ''
        """in case options has additional options, like event for progress, which should not repeat for each text"""
        self.options_fields = SubFunction(function_name='SwapLineIf', main_treeview=main_game_items)
        self.main_layout.addWidget(self.options_fields)
        self.field_text = SimpleFields.SimpleEntry(None, 'Text', label_pos='V')
        self.field_text.label_custom.change_position('C')
        self.field_text.center()
        self.field_text.set_up_widget(self.main_layout)
        self.field_text.returnPressed.connect(self.add_multi_value)
        self.data_tree = SimpleFields.ElementsList(None, folders=True, all_edit=True)
        self.data_tree.set_up_widget(self.main_layout)
        self.data_tree.setWordWrap(True)

    def add_multi_value(self):
        options_data = self.options_fields.get_val()
        self.option = options_data[0]
        if self.option in ['OtherEventsChoice', 'OtherEventsProgress', 'HasFetishLevelEqualOrGreater']:
            start_idx = 2
            self.list_fields_not_going_to_treeview = options_data[1]
        else:
            start_idx = 1
            self.list_fields_not_going_to_treeview = ''
        title = options_data[start_idx]
        self.data_tree.add_data({title: self.field_text.get_val()})
        self.data_tree.change_row_height(40)
        self.data_tree.expandAll()

    def deselect_row(self):
        self.data_tree.treeview.selection_remove(self.data_tree.treeview.selection()[0])

    def prepare_line_fields(self, prepare_options):
        self.options_fields.set_fields(prepare_options)
        self.data_tree.clear_tree()
        # self.treeview_main_game_items.disconnect_multilist()
        # for field in self.fields_list:
        #     field.destroy()
        # self.fields_list = []
        # for field in self.list_fields_not_going_to_treeview:
        #     field.destroy()
        # self.list_fields_not_going_to_treeview = []
        # self.data_tree.clear_tree()
        # if prepare_options == 'Stat':
        #     field_atr1 = SimpleFields.SingleList(label_text='Core Attribute',
        #                                          field_data={'choices': ["Power", "Technique", "Willpower", "Allure",
        #                                                                  "Intelligence", "Luck"]}, label_pos='V')
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     self.fields_list.append(field_atr1)
        #     field_atr2 = SimpleFields.NumericEntry(None)
        #     self.fields_list.append(field_atr2)
        #     field_atr2.set_up_widget(self.created_fields_layout)
        # elif prepare_options in "Arousal MaxArousal Energy MaxEnergy Virility EncounterSize Eros Progress":
        #     field_atr1 = SimpleFields.NumericEntry(None)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     self.fields_list.append(field_atr1)
        #     self.changed_selection = "Arousal MaxArousal Energy MaxEnergy Virility EncounterSize Eros Progress"
        # elif prepare_options == 'HasFetish':
        #     field_atr1 = SimpleFields.SingleList(label_text='Fetishes', label_pos='V',
        #                                          field_data={'choices': ["Fetishes"]})
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     self.fields_list.append(field_atr1)
        # elif prepare_options == 'HasFetishLevelEqualOrGreater':
        #     field_atr1 = SimpleFields.SingleList(label_text='Fetishes', label_pos='V',
        #                                          field_data={'choices': ["Fetishes"]})
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     self.list_fields_not_going_to_treeview.append(field_atr1)
        #     # self.fields_list.append(field_atr1)
        #     field_atr2 = SimpleFields.NumericEntry(None)
        #     self.fields_list.append(field_atr2)
        #     field_atr2.set_up_widget(self.created_fields_layout)
        # elif prepare_options == 'Perk':
        #     field_atr1 = SimpleFields.MultiListDisplay(None, 'Perks',
        #                                                field_data={'choices': ["Perks"], 'options': ["single_item", "search"]},
        #                                                main_data_treeview=self.treeview_main_game_items)
        #     self.fields_list.append(field_atr1)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        # elif prepare_options == 'Item':
        #     field_atr1 = SimpleFields.MultiListDisplay(None, 'Items',
        #                                                field_data={'choices': ["Items"], 'options': ["single_item", "search"]},
        #                                                main_data_treeview=self.treeview_main_game_items)
        #     self.fields_list.append(field_atr1)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        # elif prepare_options == 'IfTimeIs':
        #     field_atr1 = SimpleFields.SingleList(label_text='Time of day', label_pos='V',
        #                                          field_data={'choices': ["Day", "Night"]})
        #     self.fields_list.append(field_atr1)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        # elif prepare_options == 'OtherEventsProgress':
        #
        #     field_atr1 = SimpleFields.MultiListDisplay(None, 'Events',
        #                                                field_data={'choices': ["Events"], 'options': ["single_item", "search"]},
        #                                                main_data_treeview=self.treeview_main_game_items)
        #     # field_atr1 = SceneMultiList(self.fields_master, list_path=["currentmod-Events"], field_options=["single_item", "search"])
        #     # field_atr1.update_label('Events')
        #     # field_atr1 = SimpleFields.MultiList(self.fields_master, field_name='Events', label_position='U',
        #     #                                     list_path=["currentmod-Events"], field_options=["single_item", "search"])
        #     self.list_fields_not_going_to_treeview.append(field_atr1)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     field_atr2 = SimpleFields.NumericEntry(None)
        #     self.fields_list.append(field_atr2)
        #     field_atr2.set_up_widget(self.created_fields_layout)
        # elif prepare_options == 'Choice':
        #     field_list = Choices()
        #     field_list.set_up_widget(self.created_fields_layout)
        #     self.fields_list.append(field_list.field_choice_no)
        #     self.fields_list.append(field_list.field_choice_text)
        # #     TODO this is not working for some reason. when event is selected, choice fields are not updated.
        # elif prepare_options == 'OtherEventsChoice':
        #     field_atr1 = SimpleFields.MultiListDisplay(None, 'Event',
        #                                                field_data={'choices': ["Events"], 'options': ["single_item", "search"]},
        #                                                main_data_treeview=self.treeview_main_game_items)
        #     self.list_fields_not_going_to_treeview.append(field_atr1)
        #     field_atr1.set_up_widget(self.created_fields_layout)
        #     field_list = Choices(field_atr1)
        #     field_list.set_up_widget(self.created_fields_layout)
        #     self.fields_list.append(field_list.field_choice_no)
        #     self.fields_list.append(field_list.field_choice_text)

    def get_val(self):
        templist = [self.option]
        if self.list_fields_not_going_to_treeview:
            templist.append(self.list_fields_not_going_to_treeview)
        swap_attributes = self.data_tree.get_data()
        for dict_in_list in swap_attributes:
            for keyV in dict_in_list:
                templist.append(keyV)
                templist.append(dict_in_list[keyV][0])
        self.data_tree.clear_tree()
        self.options_fields.set_val('')
        self.field_text.clear_val()
        return templist

    def clear_val(self):
        self.data_tree.clear_tree()

    def destroy(self):
        self.main_layout.removeWidget(self.field_text)
        self.field_text.destroy()
        self.main_layout.removeWidget(self.options_fields)
        self.options_fields.destroy()
        # self.main_layout.removeWidget(self.field_widget_for_easy_remove)
        # self.field_widget_for_easy_remove.deleteLater()
        self.main_layout.removeWidget(self.data_tree)
        self.data_tree.deleteLater()


class SubFunction(QtWidgets.QWidget):
    """functions like MENU, SWAPLINE and now i see that STATCHECK, got options with various values to select.
    Some, if not most of those options, seems different but are actually the same. So instead of having
    different code(menu has different way to working for that), I've decided to create seperate class, that should
    work on those options itself."""
    def __init__(self, function_name=None, main_treeview=None):
        super().__init__()
        """in case options has additional options, like event for progress, which should not repeat for each text"""
        self.created_fields_layout = QtWidgets.QVBoxLayout()
        self.created_fields_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.created_fields_layout)
        temp = GlobalVariables.Glob_Var.get_functions(function_name)
        self.sub_functions_structure_data = temp['subfunction']
        list_options_values = list(self.sub_functions_structure_data['structure'].keys())
        list_options_values.insert(0, '')
        self.subfunctions = list_options_values  # might be usefull somewhere
        self.list_options = SimpleFields.SingleList()
        self.list_options.reload_options(list_options_values)
        self.list_options.set_up_widget(self.created_fields_layout)
        self.list_options.currentTextChanged.connect(self.set_fields)
        self.fields_list = []
        self.treeview_main_game_items = main_treeview

    def set_fields(self, sub_function_name):
        for field in self.fields_list:
            field.destroy()
        self.fields_list.clear()
        if sub_function_name:
            structure = self.sub_functions_structure_data['structure'][sub_function_name]
            for field in structure:
                tempfield = ''
                if structure[field]["type"] == "text":
                    tempfield = SimpleFields.SimpleEntry(None)
                elif structure[field]["type"] == "int":
                    tempfield = SimpleFields.NumericEntry(None, field_name=field)
                elif structure[field]["type"] == "singlelist":
                    tempfield = SimpleFields.SingleList(label_text=field, label_pos='H', field_data=structure[field])
                elif structure[field]["type"] == 'multilist':
                    tempfield = SimpleFields.MultiListDisplay(None, field, field_data=structure[field],
                                                              main_data_treeview=self.treeview_main_game_items)
                elif structure[field]["type"] == 'checkbox':
                    tempfield = SimpleFields.CheckBox(None, field, field)
                    tempfield.change_f(self.custom_function)
                elif 'choice' in structure[field]['type']:
                    if 'Events' in structure.keys():
                        tempfield = Choices(self.fields_list[0])
                    else:
                        tempfield = Choices()
                    tempfield.set_up_widget(self.created_fields_layout)
                    self.fields_list.append(tempfield.field_choice_no)
                    self.fields_list.append(tempfield.field_choice_text)
                    continue
                self.fields_list.append(tempfield)
                tempfield.set_up_widget(self.created_fields_layout)

    def get_val(self):
        """return all data from fields
        first value is selected option, rest are remaining values"""
        ret_list = [self.list_options.currentText()]
        for field in self.fields_list:
            ret_list.append(field.get_val())
        return ret_list

    def set_val(self, value):
        if not value:
            self.list_options.setCurrentIndex(0)

    def custom_function(self, state):
        # if state = 2 - checked. if 0 - unchechekd - this is only for checkbox in menu>jumpevent then scene
        if state == 2:
            next_event_field = SimpleFields.MultiListDisplay(None, 'Scene',
                                                                   field_data={"type": "multilist", "options":
                                                                              ["single_item", "search"],"choices":
                                                                              ["Scenes"]},
                                                                   main_data_treeview=self.treeview_main_game_items)

            self.fields_list[-2].final_data.function_on_modify(self.scene_reload)
            self.scene_reload()
            self.fields_list.append(next_event_field)
            next_event_field.set_up_widget(self.created_fields_layout)
        else:
            gone = self.fields_list.pop(-1)
            gone.destroy()
        """checkbox in menu function event jump > should display another multilist for scene for that event"""

    def scene_reload(self):
        self.treeview_main_game_items.scene_source = self.fields_list[0].get_val()


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
        """target area will be when user opens scene editor from simple text field."""
        self.ending_field = ''
        """checkboxes and buttons. check for adding as function or text, button to prepare and add functions"""
        h_lay_checkboxes = QtWidgets.QHBoxLayout()
        self.buttonADD_function = SimpleFields.CustomButton(None, 'Add')
        self.buttonADD_function.setMaximumWidth(40)
        self.buttonADD_function.clicked.connect(self.add_function_fields)
        h_lay_checkboxes.addWidget(self.buttonADD_function)
        self.checkbox_text = SimpleFields.CheckBox(self.parent_widget, 'TEXT', 't')
        # self.checkbox_text.set_val(True)
        self.checkbox_text.set_up_widget(h_lay_checkboxes)
        self.checkbox_event = SimpleFields.CheckBox(self.parent_widget, 'EVENT', 'e')
        self.checkbox_event.set_val(True)
        self.checkbox_event.set_up_widget(h_lay_checkboxes)
        self.buttonPREPARE_function = SimpleFields.CustomButton(None, 'Prep')
        self.buttonPREPARE_function.setMaximumWidth(40)
        self.buttonPREPARE_function.clicked.connect(self.prepare_function_fields)
        h_lay_checkboxes.addWidget(self.buttonPREPARE_function)
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.checkbox_text)
        self.button_group.addButton(self.checkbox_event)
        """flag function will be list. first its a 0/1, second, target field"""
        self.flag_function_target_type = []
        self.adding_config = adding_config
        if not adding_config[0]:
            # if 0, only text, disable event adding
            self.checkbox_text.set_val(1)
            self.checkbox_event.setEnabled(False)
            self.checkbox_text.setEnabled(False)
        self.button_group.buttonToggled.connect(self.on_checkbox_toggled)
        h_lay_checkboxes.setAlignment(QtCore.Qt.AlignCenter)
        self.custom_layout.addLayout(h_lay_checkboxes)

        self.treeview_functions = SimpleFields.ElementsList(None, 'functions', True, False, False, delete_flag=False)
        self.treeview_functions.setMinimumWidth(250)
        self.treeview_functions.set_up_widget(self.custom_layout)
        self.treeview_functions.add_data(data=GlobalVariables.Glob_Var.functions_display)
        self.treeview_functions.clicked.connect(self.display_explanation)
        self.area_instruction = SimpleFields.AreaEntry()
        self.area_instruction.setMaximumSize(300, 200)
        self.area_instruction.set_up_widget(self.custom_layout)
        """here add main_game_treeview with items from main game and mod. Not all functions need them,
        so hide and show when needed and make it work same as in main window"""
        self.treeview_main_game_items = SimpleFields.Main_MultiList(None, "Game items", main_label_flag=False)
        self.treeview_main_game_items.main_data.flag_focus = False
        self.treeview_main_game_items.current_scene_list = scene_list
        self.flag_main_game_items = False
        self.treeview_main_game_items.set_up_widget(self.functions_layout)
        self.treeview_main_game_items.hide()
        self.field_title = SimpleFields.SimpleEntry(None, 'Title')
        self.field_title.setEnabled(False)
        self.field_title.set_up_widget(self.functions_layout)
        self.field_title.setMaximumWidth(300)
        self.flag_error_checkbox = False

    def set_up_widget(self, outside_layout):
        outside_layout.addLayout(self.custom_layout)

    def create_function_field(self, structure):
        # TODO check all specials now
        """this is for creation fields that will be destroyed, instead of premaking them"""
        for field in structure:
            tempfield = None
            if structure[field]["type"] == "text":
                tempfield = SimpleFields.SimpleEntry(None, field_name=field, field_data=structure,
                                                     main_data_treeview=self.treeview_main_game_items)
            elif structure[field]["type"] == "int":
                tempfield = SimpleFields.NumericEntry(None, wid=4, field_name=field, field_data=structure)
                # tempfield.bind("<Tab>", otherFunctions.focus_next_window)
            elif structure[field]["type"] == "singlelist":
                tempfield = SimpleFields.SingleList(None, field, structure)
                # TODO for damage from monster - dropdown is too small. either make it wider or change to multilist
                tempfield.reload_options(structure[field]['choices'])
            elif structure[field]["type"] == 'multilist':
                tempfield = SimpleFields.MultiListDisplay(None, field, structure[field], single_edit=False,
                                                          main_data_treeview=self.treeview_main_game_items)
                self.flag_main_game_items = True
            elif structure[field]["type"] == 'combobox':
                tempfield = SimpleFields.InputList(None, field_name=field, field_data=structure[field])
            elif structure[field]["type"] == 'filePath':
                tempfield = SimpleFields.FileField(None, 'File', field_data=structure[field])
            self.function_fields_list.append(tempfield)
            if tempfield is not None:
                tempfield.set_up_widget(self.functions_layout, True)
        if self.flag_main_game_items:
            self.treeview_main_game_items.show()

    # def close_window(self):
    #     self.flag_if_window_open = False
    #     self.window_function.destroy()
#     # TODO check setchoice if choice is deleted when press X on input least. maybe add confirmation window too.
    def display_explanation(self, *args, function_title=None):
        """function title is for when loading function from scene text instead of function list"""
        self.ending_field = ''
        selected_function_item = self.treeview_functions.selected_element()
        if not selected_function_item.child(0, 0) or function_title:
            """clear current list of prepare fields. should work each time user select different function"""
            if self.function_fields_list:
                for field in self.function_fields_list:
                    """if its just function name, here is simple string"""
                    if isinstance(field, str):
                        continue
                    else:
                        field.destroy()
                self.function_fields_list.clear()
            if not function_title:
                function_title = selected_function_item.text()
            function_data = GlobalVariables.Glob_Var.get_functions(function_title)
            explanation_text = function_data['explanation']
            self.area_instruction.clear_val()
            self.area_instruction.set_val(explanation_text)
            """also, if there is only 1 step it is title, might as well hide prep button and add button will add it"""
            if function_data['steps'] == '1':
                self.buttonPREPARE_function.setDisabled(True)
                self.buttonADD_function.setEnabled(True)
                self.function_fields_list.append(function_data['title'])
            else:
                self.buttonPREPARE_function.setEnabled(True)
                self.buttonADD_function.setDisabled(True)
            self.field_title.set_val(function_data['title'])
            self.field_title.adjustSize()
        else:
            self.buttonADD_function.setDisabled(True)
            self.buttonPREPARE_function.setDisabled(True)
        self.treeview_main_game_items.hide()

    def prepare_function_fields(self, function_values=[]):
        """function_values - in case user wants to edit function from scene, here should be passed list
        where 0 is function title, rest are attributes"""
        if function_values:
            function_name = function_values.pop(0)
        else:
            function_item = self.treeview_functions.selected_element()
            function_name = function_item.text()
        function_data = GlobalVariables.Glob_Var.get_functions(function_name)
        self.buttonADD_function.setEnabled(True)
        """fields data should be a dictionary with all data for specific function."""
        self.flag_main_game_items = False
        """prepare correct fields. read structure in function data and make something like create field.
                    some fields are related to each other so put them in special and code manually"""
        # if "simple" in function_data['options']:
        # self.prepare_title(function_name)
        # self.frame_function_fields.pack()
        # if "TODO" in function_data['options']:
        #     struct_len = len(function_data['structure'].keys())
        #     function_data['structure'] = {}
        #     function_data['options'] = []
        #     for idx in range(1, struct_len + 1):
        #         function_data['structure'][idx] = {"type": "text"}
        if function_data['steps'] != '1':
            """create all fields for function. Later, if special, adjust them"""
            self.create_function_field(function_data['structure'])
            if "special" in function_data['options']:
                self.prepare_special(function_name)
            # print('making fields for function')
        # print('stuff to do after fields are prepared')
        """add separate EndLoop field to the list of fields. if steps is just EndLoop, add at the end, if there is a
         number, it is number of steps before end"""
        if 'EndLoop' in function_data['steps'] or 'EndMusicList' in function_data['steps']:
            """codename should be 'EndLoop-2' first part is string, usually EndLoop, sometime EndMusicList,
             second is position where"""
            self.ending_field = function_data['steps']
        if function_values:
            self.load_function_attributes(function_values, function_data)
        self.buttonPREPARE_function.setDisabled(True)
        # print(final_functions)

    def add_function_fields(self):
        """add prepared data from function fields to target area, scene text or just input text"""
        function_title = self.field_title.get_val()
        if not function_title:
            return
        checked_button = self.button_group.checkedButton()
        """this is to add to either scene or to text field"""
        if checked_button is None:
            for checkbox in self.button_group.buttons():
                checkbox.setStyleSheet("QCheckBox { color: red }")
                self.flag_error_checkbox = True
            return
        """if flag TRUE, should add as data to treeview(scene) 2
        if flag FALSE, add as text to area 1"""
        if checked_button.text() == 'EVENT':
            selected_element = self.adding_config[2].selected_element()
            if isinstance(self.function_fields_list[0], str):
                function_values = self.function_fields_list[0]
            else:
                if function_title == 'DisplayCharacters':
                    # add later updating list of currect characters in window markup text
                    self.displayed_characters = self.function_fields_list[0].get_val()
                elif 'Choice' in function_title:
                    """when choice is typed in fields and user clicked 'add function'"""
                    SimpleFields.mod_temp_data.add_choice(self.function_fields_list[0].get_val(), self.function_fields_list[1].get_val())
                elif 'ChoiceTo' in function_title:
                    self.function_fields_list.pop(-1)
                temp_vals = []
                """here check, if ending place is populated. if yes, then add ENDLOOP in correct place"""
                end_loop_place = -1
                if self.ending_field:
                    temp = self.ending_field.split('-')
                    # ending field might be 1,2 or with different word Endmusic-2
                    if len(temp) > 1:
                        end_loop_place = temp[1]
                    else:
                        end_loop_place = len(self.function_fields_list)-1
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
                    if self.function_fields_list.index(function_field) == int(end_loop_place):
                        temp_vals.append(temp[0])
                function_values = {function_title: temp_vals}
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
            for function_a in self.function_fields_list:
                if isinstance(function_a, str):
                    break
                value = function_a.get_val()
                final_function += value + '|'
            self.adding_config[1].insert_text('|f|' + final_function + 'n|')

    def prepare_special(self, function_name):
        if 'Jump' in function_name or "Call" in function_name:
            """this should cover all jumping to other scenes and events. If event jump, load event data with scenes
            if just scenes, load current event scenes"""
            if "Event" in function_name:
                self.function_fields_list[0].clear_val()
                if 'Scene' in function_name:
                    self.function_fields_list[0].final_data.function_on_modify(self.special_event_jumping_load_scenes_to_list)
            elif 'Scene' in function_name:
                self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
        elif function_name == "SwapLineIf":
            special_field = SwapLine_Field(self.functions_layout, self.treeview_main_game_items)
            self.function_fields_list.append(special_field)
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
            self.function_fields_list[2].currentTextChanged.connect(lambda: self.load_layer_picture_data('Layer'))
        elif 'Choice' in function_name:
            # TODO if below is working, maybe replace class choises with this
            if 'Event' in function_name:
                SimpleFields.mod_temp_data.prepare_fields_for_choice_set_up(self.function_fields_list[1], self.function_fields_list[2], self.function_fields_list[0])
            else:
                SimpleFields.mod_temp_data.prepare_fields_for_choice_set_up(self.function_fields_list[0], self.function_fields_list[1])
            if function_name == 'GetEventAndIfChoiceIs':
                self.special_event_jumping_load_scenes_to_list('', flag_current_event=True)
        elif function_name == 'Speaks':
            temp_field = SceneSpeaks(self.field_title)
            temp_field.set_up_widget(self.functions_layout, True)
            self.function_fields_list.append(temp_field)
        elif function_name == 'StatCheck':
            self.function_fields_list.append(StatCheckField(self.functions_layout, self.treeview_main_game_items))
            self.flag_main_game_items = True
            self.treeview_main_game_items.show()
        elif function_name == 'PlayMotionEffectCustom':
            self.function_fields_list[1].currentTextChanged.connect(self.Set_Up_Motion_Effect)
            self.function_fields_list[1].set_val(' ')
        elif function_name == 'ApplyStance':
            return
            # TODO after stances are working
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
            temp_field = CombatEncounter(self.functions_layout, self.treeview_main_game_items)
            self.function_fields_list.append(temp_field)
            self.flag_main_game_items = True
            self.treeview_main_game_items.show()

    def special_event_jumping_load_scenes_to_list(self, selected_event, flag_current_event=False):
        """for function 'jump to scene'"""
        if flag_current_event:
            self.treeview_main_game_items.scene_source = 'current'
        else:
            self.treeview_main_game_items.scene_source = selected_event

    def SpecialChangeImageLayer_prep_speakers_field(self, field_no):
        """almost done, but its not gonna work. Speaker show not from speaker fields, but from function
         displayCharacters, which are based on speakers list. So first, it need to check displaycharacters in memory
          somewher, if not used, because we loaded the mod, then it need to find that by searching backwards by scene
           names and when found, load data and then load speakers in current displayedcharacters"""
        """first prepare list of speakers used in current event.These come from DisplayCharacters function,
         should be saved in function.displayed_characters var"""

        """for now, load data according to speakers. Stuff above will be fixed some other time."""
        # TODO might be problem when girls name is not equeal to girl id or something like that
        speaker_data = PrepareSpeakers()
        temp_list = ['']
        for speaker in speaker_data:
            if speaker['name'] not in temp_list:
                temp_list.append(speaker['name'])
        self.function_fields_list[field_no].reload_options(temp_list)
        """looks good. now, prepare layers data for first field, based on speakers. All should be in currentmod, if need
         layers from main game it would need to load all mosnters data...so just search for specific monster by its id."""
        # TODO cleaning
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

    def load_layer_picture_data(self, data_level='temp', not_motion=True):
        """datalevel - if layer, set or expression or something.
            not motion - for function with additional options"""
        """find field with speaker name - should be labeled Speaker"""
        girl_id = ''
        for field in self.function_fields_list:
            if field.title == 'Speaker':
                girl_id = field.get_val()
                break
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
                    field.clear_val()
                    for pictures in pictures_list:
                        if 'Set' in pictures:
                            for pict_set in pictures['Set']:
                                results_list.append(pict_set['Name'])
                            break
                        else:
                            results_list.append(pictures['Name'])
                    field.reload_options(results_list)
                    if not_motion:
                        field.add_items_to_skip_sort(['ImageSet', 'ImageSetPersist', 'ImageSetDontCarryOver'])
                    break
        elif data_level == 'Image':
            for field in self.function_fields_list:
                if field.title == 'Layer Type':
                    layer_name = field.get_val()
                    break
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
        skills = otherFunctions.find_monster_skills(target_data)
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
        """first prepare that temp_data.
         since this def is used to 'damage from monster' and should use all girls from game"""
        skills = otherFunctions.find_monster_skills(target_data)
        self.function_fields_list[1].reload_options(skills)

    # TODO if choices are working, remove below(later)
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
        """first clean fields from bodyparts and characters to set it up again properly"""
        if len(self.function_fields_list) == 5:
            field = self.function_fields_list.pop(2)
            field.destroy()
        elif len(self.function_fields_list) == 6:
            field = self.function_fields_list.pop(2)
            field.destroy()
            field = self.function_fields_list.pop(2)
            field.destroy()
        if setup_val in 'Character Bodypart':
            """for these 2 it needs to add fields for speaker and maybe for layers"""
            temp_field = SimpleFields.SingleList(label_text='Speaker', edit=False)
            speakers = PrepareSpeakers()
            temp_list = []
            for speaker in speakers:
                if speaker['name'] not in temp_list:
                    temp_list.append(speaker['name'])
            temp_field.reload_options(temp_list)
            temp_field.set_up_widget(self.functions_layout, True, 3)
            self.function_fields_list.insert(2, temp_field)
            if setup_val == 'Bodypart':
                temp_field.currentTextChanged.connect(lambda *args: self.load_layer_picture_data(data_level='Layer', not_motion=False))
                temp_field = SimpleFields.InputList(field_name='Layer Type')
                self.function_fields_list.insert(3, temp_field)
                temp_field.set_up_widget(self.functions_layout, True, 3)

    def set_attack(self, check_val):
        """probably for apply stance, which is not ready"""
        if check_val.get() == 1:
            # print('it might work')
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
        """to edit function in text"""
        if len(function_data['steps']) == 1:
            for field, values in zip(self.function_fields_list, attributes_list):
                field.set_val(values)
        else:
            steps = function_data['steps']
            structure_fields_no = len(function_data['structure'])
            """now need if for different endloops variations.
            if just endloop, then its for last field. check structure, example = 3 fields, first 2 are single values,
             rest is for last field. unless structure empty, then it's custom and only 1 field
            if endloop-3, then third field should get most data, also check via stucture.
            Easiest would probably be to find where additional list should be. for example, for 3 fields second is loop:
            [val1,[a,b,c,d,e,endloop], val3]"""
            if structure_fields_no < 2:
                """only 1 field, not much to think about"""
                attributes_list.pop(-1)
                self.function_fields_list[0].set_val(attributes_list)
                return
            elif '-' in steps:
                end = steps.split('-')
                step_f = end[1]
                end = end[0]
            else:
                end = steps
                step_f = structure_fields_no-1
            end_loop_list = []
            values_list = []
            for idx in range(len(attributes_list)):
                if idx == step_f:
                    while attributes_list[idx] != end:
                        end_loop_list.append(attributes_list[idx])
                        idx += 1
                    values_list.append(end_loop_list)
                else:
                    values_list.append(attributes_list[idx])
            for field, values in zip(self.function_fields_list, values_list):
                field.set_val(values)

    def on_checkbox_toggled(self, checkbox, checked):
        if self.flag_error_checkbox:
            if checked:
                for button in self.button_group.buttons():
                    button.setStyleSheet("QCheckBox { color: black }")


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
