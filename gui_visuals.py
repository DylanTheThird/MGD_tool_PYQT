import tkinter as tk
# from tkinter.ttk import Label
import SimpleFields
import GlobalVariables
from otherFunctions import update_config
fonts = ['System',
'Terminal',
'Fixedsys',
'Modern',
'Roman',
'Script',
'Courier',
'MS Serif',
'MS Sans Serif',
'Small Fonts',
'Marlett',
'Arial',
'Arabic Transparent',
'Arial Baltic',
'Arial CE',
'Arial CYR',
'Arial Greek',
'Arial TUR',
'Arial Black',
'Bahnschrift Light',
'Bahnschrift SemiLight',
'Bahnschrift',
'Bahnschrift SemiBold',
'Bahnschrift Light SemiCondensed',
'Bahnschrift SemiLight SemiConde',
'Bahnschrift SemiCondensed',
'Bahnschrift SemiBold SemiConden',
'Bahnschrift Light Condensed',
'Bahnschrift SemiLight Condensed',
'Bahnschrift Condensed',
'Bahnschrift SemiBold Condensed',
'Calibri',
'Calibri Light',
'Cambria',
'Cambria Math',
'Candara',
'Candara Light',
'Comic Sans MS',
'Consolas',
'Constantia',
'Corbel',
'Corbel Light',
'Courier New',
'Courier New Baltic',
'Courier New CE',
'Courier New CYR',
'Courier New Greek',
'Courier New TUR',
'Ebrima',
'Franklin Gothic Medium',
'Gabriola',
'Gadugi',
'Georgia',
'Impact',
'Ink Free',
'Javanese Text',
'Leelawadee UI',
'Leelawadee UI Semilight',
'Lucida Console',
'Lucida Sans Unicode',
'Malgun Gothic',
'@Malgun Gothic',
'Malgun Gothic Semilight',
'@Malgun Gothic Semilight',
'Microsoft Himalaya',
'Microsoft JhengHei',
'@Microsoft JhengHei',
'Microsoft JhengHei UI',
'@Microsoft JhengHei UI',
'Microsoft JhengHei Light',
'@Microsoft JhengHei Light',
'Microsoft JhengHei UI Light',
'@Microsoft JhengHei UI Light',
'Microsoft New Tai Lue',
'Microsoft PhagsPa',
'Microsoft Sans Serif',
'Microsoft Tai Le',
'Microsoft YaHei',
'@Microsoft YaHei',
'Microsoft YaHei UI',
'@Microsoft YaHei UI',
'Microsoft YaHei Light',
'@Microsoft YaHei Light',
'Microsoft YaHei UI Light',
'@Microsoft YaHei UI Light',
'Microsoft Yi Baiti',
'MingLiU-ExtB',
'@MingLiU-ExtB',
'PMingLiU-ExtB',
'@PMingLiU-ExtB',
'MingLiU_HKSCS-ExtB',
'@MingLiU_HKSCS-ExtB',
'Mongolian Baiti',
'MS Gothic',
'@MS Gothic',
'MS UI Gothic',
'@MS UI Gothic',
'MS PGothic',
'@MS PGothic',
'MV Boli',
'Myanmar Text',
'Nirmala UI',
'Nirmala UI Semilight',
'Palatino Linotype',
'Segoe MDL2 Assets',
'Segoe Print',
'Segoe Script',
'Segoe UI',
'Segoe UI Black',
'Segoe UI Emoji',
'Segoe UI Historic',
'Segoe UI Light',
'Segoe UI Semibold',
'Segoe UI Semilight',
'Segoe UI Symbol',
'SimSun',
'@SimSun',
'NSimSun',
'@NSimSun',
'SimSun-ExtB',
'@SimSun-ExtB',
'Sitka Small',
'Sitka Text',
'Sitka Subheading',
'Sitka Heading',
'Sitka Display',
'Sitka Banner',
'Sylfaen',
'Symbol',
'Tahoma',
'Times New Roman',
'Times New Roman Baltic',
'Times New Roman CE',
'Times New Roman CYR',
'Times New Roman Greek',
'Times New Roman TUR',
'Trebuchet MS',
'Verdana',
'Webdings',
'Wingdings',
'Yu Gothic',
'@Yu Gothic',
'Yu Gothic UI',
'@Yu Gothic UI',
'Yu Gothic UI Semibold',
'@Yu Gothic UI Semibold',
'Yu Gothic Light',
'@Yu Gothic Light',
'Yu Gothic UI Light',
'@Yu Gothic UI Light',
'Yu Gothic Medium',
'@Yu Gothic Medium',
'Yu Gothic UI Semilight',
'@Yu Gothic UI Semilight',
'HoloLens MDL2 Assets',
'BIZ UDGothic',
'@BIZ UDGothic',
'BIZ UDPGothic',
'@BIZ UDPGothic',
'BIZ UDMincho Medium',
'@BIZ UDMincho Medium',
'BIZ UDPMincho Medium',
'@BIZ UDPMincho Medium',
'Meiryo',
'@Meiryo',
'Meiryo UI',
'@Meiryo UI',
'MS Mincho',
'@MS Mincho',
'MS PMincho',
'@MS PMincho',
'UD Digi Kyokasho N-B',
'@UD Digi Kyokasho N-B',
'UD Digi Kyokasho NP-B',
'@UD Digi Kyokasho NP-B',
'UD Digi Kyokasho NK-B',
'@UD Digi Kyokasho NK-B',
'UD Digi Kyokasho N-R',
'@UD Digi Kyokasho N-R',
'UD Digi Kyokasho NP-R',
'@UD Digi Kyokasho NP-R',
'UD Digi Kyokasho NK-R',
'@UD Digi Kyokasho NK-R',
'Yu Mincho',
'@Yu Mincho',
'Yu Mincho Demibold',
'@Yu Mincho Demibold',
'Yu Mincho Light',
'@Yu Mincho Light',
'DengXian',
'@DengXian',
'DengXian Light',
'@DengXian Light',
'FangSong',
'@FangSong',
'KaiTi',
'@KaiTi',
'SimHei',
'@SimHei',
'Ubuntu',
'Raleway',
'Ubuntu Condensed',
'Ubuntu Light']

# examples_list=[]

class App(tk.Toplevel):
    def __init__(self, master=None, current_style=None, font_type=None, font_size=None):
        super().__init__(master=master)
        # Instantiating master i.e toplevel Widget
        # self.master = master
        # Instantiating Style class
        # self.style = Style(self)
        self.current_style = current_style
        self.def_font = 'Arial'
        self.def_size = 10
        self.font_size = GlobalVariables.current_font_size
        self.title('MGD Visual Options')

        # labels_style = style.configure("TLabel", font=('Arial', self.font_size))
        frame_visual_options = tk.Frame(self, height=100, width=300)
        frame_visual_options.grid_propagate(0)
        # frame_visual_options.grid_columnconfigure(4, weight=1)
        # frame_visual_options.grid_rowconfigure(3, weight=1)
        frame_visual_options.grid(row=0, column=0)
        self.font_options = SimpleFields.SingleList(frame_visual_options, 'Fonts', '', 'U', fonts)
        self.font_options.grid(row=0, column=1, rowspan=3, sticky='NS')
        self.font_options.set_val(GlobalVariables.current_font_type)
        font_prev = tk.Button(frame_visual_options, text='^^', command=self.fontprev)
        font_prev.grid(row=0, column=0, sticky='S')
        font_next = tk.Button(frame_visual_options, text='VV', command=self.fontnext)
        font_next.grid(row=2, column=0, sticky='N')
        font_apply = tk.Button(frame_visual_options, text='Apply', command=self.apply_font)
        font_apply.grid(row=1, column=0, sticky='W')

        size_increase = tk.Button(frame_visual_options, text='^Increase font size^', command=self.size_up)
        size_decrease = tk.Button(frame_visual_options, text='VDecrease font sizeV', command=self.size_down)
        # self.size_current = Label(frame_visual_options, text=str(self.font_size))
        self.size_current = SimpleFields.SimpleField(frame_visual_options, str(self.font_size),'')
        self.size_current.update_label(self.font_size)
        size_increase.grid(row=0, column=2)
        self.size_current.grid(row=1, column=2)
        size_decrease.grid(row=2, column=2)


        button_set_detault = tk.Button(frame_visual_options, text='restore default', command=self.restore_default)
        button_set_detault.grid(row=5, column=0, columnspan=3)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # temp_label1 = tk.Label(frame_visual_options, text='testfffffffffffffffffff ivusla')
        # temp_label1.grid(row=0, column=4)
        # temp_label2 = tk.Label(frame_visual_options, text='test ivusla')
        # temp_label2.grid(row=1, column=4, sticky=tk.EW)
        # temp_label3 = Label(frame_visual_options, text='test new')
        # temp_label3.grid(row=2, column=4, sticky='EW')
        # temp_label3.grid_columnconfigure(0, weight=1)
        # temp_label3.grid_rowconfigure(0, weight=1)
        # # self.style.configure("TLabel", font=('Arial', self.font_size))


        # frame_examples = tk.Frame(self)
        # frame_examples.grid(row=1, column=0)
        #
        # for indx in range(1, 5):
        #     test_field = SimpleFields.SimpleEntry(frame_examples, 'test', '', 'L')
        #     test_field.pack()
        #     test_label = tk.Label(frame_examples, text='test22')
        #     test_label.pack()
        #     examples_list.append(test_field.field_label)
    def apply_font(self):
        font_name = self.font_options.get_val()
        # Changing font-size of all the Label Widget
        # self.style.configure("TLabel", font=(font_name, self.font_size))
        self.current_style.configure("TLabel", font=(font_name, self.font_size))
        # print(self.size_current.field_label['background'])
        # self.size_current.field_label.configure(background='aliceblue')
        # self.size_current.field_label.configure(background='')
        # global current_font_type
        # global current_font_size
        GlobalVariables.current_font_type = font_name
        GlobalVariables.current_font_size = self.font_size

        # for example in examples_list:
        #     example.config(font=(font_name, 14))

    def fontprev(self):
        font_current = self.font_options.get_val()
        font_current_no = fonts.index(font_current)-1
        if font_current_no > 0:
            self.font_options.set_val(fonts[font_current_no])
            self.apply_font()

    def fontnext(self):
        font_current = self.font_options.get_val()
        font_current_no = fonts.index(font_current)+1
        if font_current_no < len(fonts):
            self.font_options.set_val(fonts[font_current_no])
            self.apply_font()

    def size_up(self):
        self.font_size += 1
        # self.size_current.configure(text=str(self.font_size))
        self.size_current.update_label(str(self.font_size))
        self.apply_font()
    def size_down(self):
        self.font_size -= 1
        self.size_current.update_label(str(self.font_size))
        self.apply_font()

    def restore_default(self):
        self.font_options.set_val(self.def_font)
        self.size_current.update_label(self.font_size)
        self.apply_font()
    def on_closing(self):
        update_config()
        self.destroy()

# MainWin = tk.Tk()
#
# app = App(MainWin)
#
# MainWin.mainloop()