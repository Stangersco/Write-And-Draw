import configparser as cp
from os import listdir, getcwd
from os.path import join as j

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

TYPE_ENCODING = ('utf-8', 'utf-16', 'utf-32', 'ascii',
                 'iso-8859-1', 'Windows-1252', 'Windows-1251',
                 'KOI8-R', 'EUC-JP', 'ISO-2022-JP', 'ISO-8859-7')


files_in_direct = ''


def file_directory():
    global files_in_direct
    direct = j(getcwd(), 'file')
    files_in_direct = sorted(listdir(direct))


class Config:
    def __init__(self):
        self._config = cp.ConfigParser()
        self._config.read('config.ini')

        self.encoding = self._config.get('Settings', 'encoding')
        self.font_size = self._config.getint('Settings', 'font_size')
        self.auto_save = self._config.getboolean('Settings', 'auto_save')
        self.cured_proportions = self._config.getfloat('Settings', 'cured_proportions')

    def set(self, section, option, value=None):
        self._config.set(section, option, value)

        self.save_config()

    def save_config(self):
        with open("config.ini", 'w') as settings:
            self._config.write(settings)


class ActiveButton(Button):
    def __init__(self, bg=(1, 1, 1, 1), **kwargs):
        super(ActiveButton, self).__init__(**kwargs)
        self.bg = bg[0:3]
        Window.bind(mouse_pos=self.pos_check)

    def pos_check(self, ints, pos):
        if self.collide_point(*pos):
            self.background_color = (*self.bg, 0.7)
        else:
            self.background_color = (*self.bg, 1)

    def on_release(self):
        self.background_color = (*self.bg, 0.7)

    def on_press(self):
        self.background_color = (0, 0.6, 0, 0.9)


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)
        self.history_canvas = list()
        self.size_cursor = 1.5

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(1, 1, 0, 1)
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=self.size_cursor)

    def on_touch_move(self, touch):
        if "line" in touch.ud and self.collide_point(*touch.pos):
            touch.ud["line"].points += [touch.x, touch.y]

    def go_to_back(self):
        if self.canvas.children:
            self.history_canvas.append(self.canvas.children[-2])
            self.history_canvas.append(self.canvas.children[-1])
            del self.canvas.children[-2]
            del self.canvas.children[-1]

    def go_to_next(self):
        if self.history_canvas:
            self.canvas.children.append(self.history_canvas[-2])
            self.canvas.children.append(self.history_canvas[-1])
            self.history_canvas.pop()
            self.history_canvas.pop()

    def clear_holst(self):
        # temp = self.canvas.children[0:3]
        self.canvas.children.clear()
        # self.canvas.children.extend(temp)


class NoteBook(App):
    settings = Config()
    # encoding_button = font_size_text = autosave = catalogs = selected_file = None

    def build(self):

        root = FloatLayout()

        core = BoxLayout(orientation='vertical')
        tool = BoxLayout(size=(0, 20), size_hint=(1, None), padding=(0, 0, 3, 0), spacing=3)

        self.encoding_button = ActiveButton(text=self.settings.encoding,
                                            on_release=self.show_encoding,
                                            size_hint=(.2, 1))

        self.font_size_text = ActiveButton(text=str(self.settings.font_size),
                                           on_release=self.show_font_sizes,
                                           size_hint=(.2, 1))

        autosave_label = Label(text='autosave:', size=(70, 20),
                               size_hint=(None, None))

        self.autosave = CheckBox(size_hint=(None, None), size=(30, 20),
                                 active=self.settings.auto_save)

        self.autosave.bind(active=lambda _, value: self._change_auto_save(value))

        slider = Slider(min=0, max=1, value=self.settings.cured_proportions, step=0.001, cursor_size=(20, 20))
        slider.bind(value=self.on_slider_value_change)

        tool.add_widget(self.encoding_button)
        tool.add_widget(self.font_size_text)
        tool.add_widget(Button(on_release=lambda x: self.drawing_screen.clear_holst()))
        tool.add_widget(slider)
        tool.add_widget(autosave_label)
        tool.add_widget(self.autosave)

        panel = BoxLayout(size_hint=(1, None), size=(0, 40))
        text_field = BoxLayout(size_hint=(1, .9), spacing=0)
        file_selected = BoxLayout(orientation='vertical', size_hint=(None, 1), size=(100, 0))
        self.catalogs = GridLayout(cols=1, size_hint=(None, 1), size=(100, 0))

        self.selected_file = Label(text='None', color='grey', size_hint=(None, 1), size=(100, 0))
        file_selected.add_widget(Label(text='Cured file:', size_hint=(None, 1), size=(100, 0)))
        file_selected.add_widget(self.selected_file)

        panel.add_widget(file_selected)

        self.name_file = TextInput(hint_text='Name File', text='', size_hint=(1, 1))
        panel.add_widget(self.name_file)

        panel.add_widget(ActiveButton(text='Reload', on_press=lambda _: self.update_catalog(), size_hint=(.1, 1)))
        panel.add_widget(ActiveButton(text='Create', on_press=lambda _: self.save_file(), size_hint=(.1, 1)))
        panel.add_widget(ActiveButton(text='Save', on_press=self.save_text, size_hint=(.1, 1)))

        self.text_ = TextInput(hint_text='None', padding=(15, 1, 1, 1),
                               background_color=(11.8, 11, 12.2, 0.3),
                               background_normal='white',
                               foreground_color='white',
                               cursor_color=(1, 1, 1, 1),
                               selection_color=(0, 120, 0, 0.2),
                               font_size=self.settings.font_size,
                               _cursor_blink=True,
                               size_hint_y=1,
                               size_hint_x=.5
                               )

        self.drawing_screen = PaintWidget(
                                        size_hint_y=1,
                                        size_hint_x=.5
                                        )

        self.text_and_graphics = BoxLayout()
        self.text_and_graphics.add_widget(self.text_)
        self.text_and_graphics.add_widget(self.drawing_screen)

        # update catalog files
        self.update_catalog()
        self.on_slider_value_change(None, self.settings.cured_proportions)

        text_field.add_widget(self.catalogs)
        text_field.add_widget(self.text_and_graphics)

        core.add_widget(tool)
        core.add_widget(panel)
        core.add_widget(text_field)

        root.add_widget(core)

        # root.add_widget(PaintWidget())

        return root

    def update_catalog(self):
        file_directory()
        self.catalogs.clear_widgets()
        for i in files_in_direct:
            self.catalogs.add_widget(ActiveButton(text=i, on_press=self.select_file))

    def save_file(self):
        if self.name_file.text and f'{self.name_file.text}.txt' not in files_in_direct:
            file_directory()
            resolution = '' if '.' in self.name_file.text else '.txt'
            print('file was created: ', end='')
            with open(f'file/{self.name_file.text}{resolution}', 'w+', encoding=self.settings.encoding) as f:
                pass
        else:
            print('Fatal name')
        print(self.name_file.text)
        self.update_catalog()

    def save_text(self):
        with open(f'file/{self.selected_file.text}', 'w', encoding=self.settings.encoding) as f:
            f.write(self.text_.text)

    def select_file(self, instance):
        if self.selected_file.text != 'None' and self.settings.auto_save:
            self.save_text()
        try:
            with open(f'file/{instance.text}', 'r', encoding=self.settings.encoding) as f:
                self.text_.text = f.read()
            self.selected_file.text = instance.text
        except UnicodeDecodeError:
            print('error encoding')

    def on_slider_value_change(self, instance, value: float):
        self.text_.size_hint_x = value
        self.drawing_screen.size_hint_x = 1 - value
        if round(self.settings.cured_proportions, 1) != round(value, 1):
            self.settings.set("Settings", 'cured_proportions', str(value))
            self.settings.cured_proportions = value

    def show_encoding(self, instance):
        dropdown = DropDown()

        for option in TYPE_ENCODING:
            if option != self.settings.encoding:
                btn = Button(text=option, size_hint_y=None, height=25, background_color=(.2, 0.5, 0, 1),
                             background_normal='white', padding=(1, 1, 1, 1))
                btn.bind(on_release=lambda x: self._change_encoding(x.text))
                dropdown.add_widget(btn)

        dropdown.open(instance)

    def show_font_sizes(self, instance):
        dropdown = DropDown()

        for option in range(9, 30):
            if option != self.settings.font_size:
                btn = Button(text=str(option), size_hint_y=None, height=25, background_color=(.2, 0.5, 0, 1),
                             background_normal='white', padding=(1, 1, 1, 1))
                btn.bind(on_release=lambda x: self._change_font_size(x.text))
                dropdown.add_widget(btn)

        dropdown.open(instance)

    def _change_auto_save(self, value: bool):
        self.settings.set("Settings", "auto_save", str(value))
        self.settings.auto_save = value

    def _change_encoding(self, encoding: str):
        """
        # use settings
        :param encoding: encoding type
        """
        self.encoding_button.text = encoding
        self.settings.set("Settings", "encoding", encoding)
        self.settings.encoding = encoding

    def _change_font_size(self, size: str):
        self.text_.font_size = self.settings.font_size = int(size)
        self.font_size_text.text = size
        self.settings.set("Settings", "font_size", size)
        self.settings.font_size = size


if __name__ == '__main__':
    NoteBook().run()
