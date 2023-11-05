from os import listdir, getcwd
from os.path import join as j
import configparser as cp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.slider import Slider

TYPE_ENCODING = ('utf-8', 'utf-16', 'utf-32', 'iso-8859-1')

config = cp.ConfigParser()
config.read('config.ini')

files_in_direct = ''
encoding_file = config.get('Settings', 'encoding')
auto_save = config.get('Settings', 'auto_save')
auto_save = bool(auto_save)


def file_directory():
    global files_in_direct
    direct = j(getcwd(), 'file')
    files_in_direct = sorted(listdir(direct))


def save_config():
    with open("config.ini", 'w') as settings:
        config.write(settings)


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


class NoteBook(App):
    def build(self):
        self.file = None

        core = BoxLayout(orientation='vertical')
        tool = BoxLayout(size=(0, 20), size_hint=(1, None), padding=(0, 0, 3, 0), spacing=3)

        slider = Slider(min=0, max=1, value=0.5)
        slider.bind(value=self.on_slider_value_change)

        self.encoding_button = ActiveButton(text=encoding_file,
                                            on_release=self.show_encoding,
                                            size_hint=(.2, 1))

        tool.add_widget(self.encoding_button)
        tool.add_widget(slider)

        panel = BoxLayout(size_hint=(1, .07))
        text_field = BoxLayout(size_hint=(1, .9), spacing=0)
        file_selected = BoxLayout(orientation='vertical', size_hint=(.26, 1))
        self.catalogs = GridLayout(cols=1, size_hint=(.2, 1))

        self.selected_file = Label(text='empy', color='grey')
        file_selected.add_widget(Label(text='Cured file:'))
        file_selected.add_widget(self.selected_file)

        panel.add_widget(file_selected)

        self.name_file = TextInput(hint_text='Name File', text='')
        panel.add_widget(self.name_file)

        panel.add_widget(ActiveButton(text='Reload', on_press=self.update_catalog, size_hint=(.1, 1)))
        panel.add_widget(ActiveButton(text='Create', on_press=self.save_file, size_hint=(.1, 1)))
        panel.add_widget(ActiveButton(text='Save', on_press=self.save_text, size_hint=(.1, 1)))

        self.text_ = TextInput(hint_text='None', padding=(15, 1, 1, 1),
                               background_color=(11.8, 11, 12.2, 0.3),
                               background_normal='white',
                               foreground_color='white',
                               cursor_color=(1, 1, 1, 1),
                               selection_color=(0, 120, 0, 0.2),
                               font_size=20,
                               _cursor_blink=True,
                               size_hint_y=1,
                               size_hint_x=.5
                               )

        self.drawing_screen = TextInput(background_color=(1, 1, 1, 1),
                                        size_hint_y=1,
                                        size_hint_x=.5
                                        )

        self.text_and_graphics = BoxLayout()  # !!!!!!!!!!!!!!!!!!!!!
        self.text_and_graphics.add_widget(self.text_)
        self.text_and_graphics.add_widget(self.drawing_screen)

        # update catalog files
        self.update_catalog()

        text_field.add_widget(self.catalogs)
        text_field.add_widget(self.text_and_graphics)

        core.add_widget(tool)
        core.add_widget(panel)
        core.add_widget(text_field)

        return core

    def update_catalog(self, instance=None):
        file_directory()
        self.catalogs.clear_widgets()
        for i in files_in_direct:
            self.catalogs.add_widget(ActiveButton(text=i, on_press=self.select_file))

    def open_file(self, file_name):
        pass

    def save_file(self, instance):
        if self.name_file.text and f'{self.name_file.text}.txt' not in files_in_direct:
            file_directory()
            print('file was created')
            with open(f'file/{self.name_file.text}.txt', 'w+', encoding=encoding_file) as f:
                # f.write(self.text_.text)
                pass
        else:
            print('Fatal name')
        print(self.name_file.text)
        self.update_catalog()

    def save_text(self, instance=None):
        with open(f'file/{self.file}', 'w') as f:
            f.write(self.text_.text)

    def select_file(self, instance):
        if self.file and auto_save:
            self.save_text()
        self.file = instance.text
        self.selected_file.text = instance.text
        with open(f'file/{self.file}', 'r') as f:
            self.text_.text = f.read()

    def on_slider_value_change(self, instance, value):
        self.text_.size_hint_x = value
        self.drawing_screen.size_hint_x = 1-value

    def show_encoding(self, instance):
        dropdown = DropDown()

        for option in TYPE_ENCODING:
            if option != encoding_file:
                btn = Button(text=option, size_hint_y=None, height=25, background_color=(.2, 0.5, 0, 1),
                             background_normal='white', padding=(1, 1, 1, 1))
                btn.bind(on_release=lambda x: self.change_encoding(x.text))
                dropdown.add_widget(btn)

        dropdown.open(instance)

    def change_encoding(self, encoding: str):
        """
        :param encoding: encoding type
        """
        global encoding_file
        encoding_file = encoding
        self.encoding_button.text = encoding
        config.set("Settings", "encoding", encoding)
        save_config()


if __name__ == '__main__':
    try:
        NoteBook().run()
    except:
        print('error')
