from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os

NOTES_FOLDER = "notes"

class NotesApp(App):

    def build(self):
        if not os.path.exists(NOTES_FOLDER):
            os.makedirs(NOTES_FOLDER)

        main_layout = BoxLayout(orientation='horizontal')

        # LEFT SIDE: NOTE LIST
        self.notes_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.notes_list_layout.bind(minimum_height=self.notes_list_layout.setter('height'))

        scroll = ScrollView(size_hint=(0.3, 1))
        scroll.add_widget(self.notes_list_layout)

        main_layout.add_widget(scroll)

        # RIGHT SIDE: EDITOR
        editor_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.note_title = TextInput(hint_text="Note Title", size_hint_y=0.15, font_size=22)
        editor_layout.add_widget(self.note_title)

        self.note_input = TextInput(hint_text="Write your note here...",
                                    size_hint_y=0.7, font_size=18)
        editor_layout.add_widget(self.note_input)

        # BUTTONS
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)

        new_btn = Button(text="New Note", background_color=(0.2, 0.7, 0.2, 1), font_size=20)
        new_btn.bind(on_press=self.new_note)

        save_btn = Button(text="Save", background_color=(0, 0.5, 1, 1), font_size=20)
        save_btn.bind(on_press=self.save_note)

        delete_btn = Button(text="Delete", background_color=(1, 0, 0, 1), font_size=20)
        delete_btn.bind(on_press=self.delete_note)

        btn_layout.add_widget(new_btn)
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(delete_btn)

        editor_layout.add_widget(btn_layout)
        main_layout.add_widget(editor_layout)

        self.load_notes_list()

        return main_layout

    # Load notes list
    def load_notes_list(self):
        self.notes_list_layout.clear_widgets()

        files = os.listdir(NOTES_FOLDER)

        for file in files:
            btn = Button(text=file.replace(".txt", ""), size_hint_y=None, height=50,
                         background_color=(0.2, 0.2, 0.2, 1))
            btn.bind(on_press=self.open_note)
            self.notes_list_layout.add_widget(btn)

    # New Note
    def new_note(self, instance):
        self.note_title.text = ""
        self.note_input.text = ""

    # Open note
    def open_note(self, instance):
        filename = instance.text + ".txt"
        filepath = os.path.join(NOTES_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        self.note_title.text = instance.text
        self.note_input.text = content

    # Save note
    def save_note(self, instance):
        title = self.note_title.text.strip()
        content = self.note_input.text

        if title == "":
            return

        filepath = os.path.join(NOTES_FOLDER, title + ".txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        self.load_notes_list()

    # Delete note
    def delete_note(self, instance):
        title = self.note_title.text.strip()
        if title == "":
            return

        filepath = os.path.join(NOTES_FOLDER, title + ".txt")

        if os.path.exists(filepath):
            os.remove(filepath)

        self.note_title.text = ""
        self.note_input.text = ""

        self.load_notes_list()


NotesApp().run()
