from os import listdir, getcwd
from os.path import join as j
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

files_in_direct = ''


def file_directory():
    global files_in_direct
    direct = j(getcwd(), 'file')
    files_in_direct = sorted(listdir(direct))


file_directory()


class NoteBook(App):
    def build(self):
        self.file = None

        core = BoxLayout(orientation='vertical')

        panel = BoxLayout(size_hint=(1, .07))
        text_field = BoxLayout(size_hint=(1, .9), spacing=0)
        self.catalogs = GridLayout(cols=1, size_hint=(.2, 1))

        self.selected_file = Label(text='empy', color='grey', size_hint=(.26, 1))
        self.name_file = TextInput(hint_text='Name File', text='')
        panel.add_widget(self.selected_file)
        panel.add_widget(self.name_file)
        panel.add_widget(Button(text='Reload', on_press=self.update_catalog, size_hint=(.1, 1)))
        panel.add_widget(Button(text='Create', on_press=self.save_file, size_hint=(.1, 1)))
        panel.add_widget(Button(text='Save', on_press=self.save_text, size_hint=(.1, 1)))


        self.text_ = TextInput(hint_text='None', padding=(15, 1, 1, 1),
                               background_color=(11.8, 11, 12.2, 0.3),
                               background_normal='white',
                               foreground_color='white',
                               cursor_color=(1, 1, 1, 1),
                               font_size=(20),
                               _cursor_blink=True
                               )

        for i in files_in_direct:
            self.catalogs.add_widget(Button(text=i, on_press=self.select_file))

        text_field.add_widget(self.catalogs)
        text_field.add_widget(self.text_)

        core.add_widget(panel)
        core.add_widget(text_field)

        return core

    def update_catalog(self, instance=None):
        file_directory()
        self.catalogs.clear_widgets()
        for i in files_in_direct:
            self.catalogs.add_widget(Button(text=i, on_press=self.select_file))

    def open_file(self, file_name):
        pass

    def save_file(self, instance):
        if self.name_file.text and f'{self.name_file.text}.txt' not in files_in_direct:
            file_directory()
            print('file was created')
            with open(f'file/{self.name_file.text}.txt', 'w+') as f:
                f.write(self.text_.text)
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
