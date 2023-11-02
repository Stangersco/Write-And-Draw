from os import listdir, getcwd
from os.path import join as j
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window

files_in_direct = ''


def file_directory():
    global files_in_direct
    direct = j(getcwd(), 'file')
    files_in_direct = sorted(listdir(direct))


class ActiveButton(Button):
    def __init__(self, **kwargs):
        super(ActiveButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.pos_check)

    def pos_check(self, ints, pos):
        if self.collide_point(*pos):
            self.background_color = (1, 1, 1, 0.7)
        else:
            self.background_color = (1, 1, 1, 1)

    def on_release(self):
        self.background_color = (1, 1, 1, 0.7)

    def on_press(self):
        self.background_color = (0, 0.6, 0, 0.9)


class NoteBook(App):
    def build(self):
        self.file = None

        core = BoxLayout(orientation='vertical')
        tool = BoxLayout(size_hint=(1, .03), padding=(0, 1, 2, 1), spacing=3)

        tool.add_widget(ActiveButton(text='file', font_size=12))
        tool.add_widget(ActiveButton(text='font', font_size=12))
        tool.add_widget(ActiveButton(text='do', font_size=12))
        tool.add_widget(ActiveButton(text='settings', font_size=12))
        tool.add_widget(ActiveButton(text='text', font_size=12))

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
                               size_hint_x=1
                               )

        self.update_catalog()

        text_field.add_widget(self.catalogs)
        text_field.add_widget(self.text_)

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
            with open(f'file/{self.name_file.text}.txt', 'w+') as f:
                # f.write(self.text_.text)
                pass
        else:
            print('Fatal name')
        print(self.name_file.text)
        self.update_catalog()

    def save_text(self, instance):
        with open(f'file/{self.file}', 'w') as f:
            f.write(self.text_.text)

    def select_file(self, instance):
        self.file = instance.text
        self.selected_file.text = instance.text
        with open(f'file/{self.file}', 'r') as f:
            self.text_.text = f.read()


if __name__ == '__main__':
    NoteBook().run()
