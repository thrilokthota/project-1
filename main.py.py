from datetime import datetime
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from plyer import notification
import threading

KV = '''
#:import datetime datetime.datetime

BoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    MDBoxLayout:
        size_hint: 1, None
        height: dp(360)
        pos_hint: {'center_x': 0.5}

        canvas:
            Color:
                rgba: app.theme_cls.primary_color  # Set box color to match the button color
            Rectangle:
                size: self.size
                pos: self.pos

    MDBoxLayout:
        size_hint: 1, None
        height: dp(200)
        pos_hint: {'center_x': 0.5}

        canvas:
            Color:
                rgba: 1, 1, 1, 1  # Change to white
            Rectangle:
                size: self.size
                pos: self.pos

        MDLabel:
            text: "Notify your reminders!"
            font_style: 'H5'
            theme_text_color: 'Primary'
            size_hint_y: None
            height: self.texture_size[1] + dp(10)
            pos_hint: {'top': 1, 'left': 1}
            padding: dp(10)

    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: self.minimum_size
        pos_hint: {'center_x': 0.5}
        spacing: dp(10)
        padding: dp(10)

        MDTextField:
            id: reminder_input
            hint_text: "Enter Reminder"
            color: app.theme_cls.primary_color  # Use primary color for text
            size_hint_x: None
            width: root.width * 0.8
            pos_hint: {'center_x': 0.5}
            padding: [dp(10), dp(15), dp(10), dp(15)]

    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: self.minimum_size
        pos_hint: {'center_x': 0.5}
        spacing: dp(10)
        padding: dp(10)

        MDTextField:
            id: moral_input
            hint_text: "Enter Moral"
            color: app.theme_cls.primary_color  # Use primary color for text
            size_hint_x: None
            width: root.width * 0.8
            pos_hint: {'center_x': 0.5}
            padding: [dp(10), dp(15), dp(10), dp(15)]

    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: self.minimum_size
        pos_hint: {'center_x': 0.5}
        spacing: dp(10)
        padding: dp(10)

        Spinner:
            id: hour_spinner
            text: str(datetime.now().strftime('%I'))
            values: [str(i) for i in range(1, 13)]
            size_hint: None, None
            size: 100, 48
            font_size: '18sp'

        Spinner:
            id: minute_spinner
            text: str(datetime.now().strftime('%M'))
            values: [str(i).zfill(2) for i in range(0, 60, 5)]
            size_hint: None, None
            size: 100, 48
            font_size: '18sp'

        Spinner:
            id: ampm_spinner
            text: datetime.now().strftime('%p')
            values: ['AM', 'PM']
            size_hint: None, None
            size: 100, 48
            font_size: '18sp'

    MDRaisedButton:
        text: "Set"
        size_hint: None, None
        size: dp(150), dp(50)
        pos_hint: {'right': 1, 'center_y': 0.5}  # Right-center position
        on_release: app.set_reminder()
        elevation_normal: 2
        elevation_hover: 4
        md_bg_color: app.theme_cls.primary_color
        ripple_behavior: True
'''

class NoteloopApp(MDApp):
    def build(self):
        self.dialog = None
        self.ampm_menu = None
        return Builder.load_string(KV)

    def show_notification(self, message):
        notification.notify(
            title="Reminder",
            message=message,
            timeout=10
        )

    def set_reminder(self):
        reminder_text = self.root.ids.reminder_input.text
        moral_text = self.root.ids.moral_input.text
        hour_text = self.root.ids.hour_spinner.text
        minute_text = self.root.ids.minute_spinner.text
        ampm_text = self.root.ids.ampm_spinner.text

        if not all([reminder_text, hour_text, minute_text, ampm_text]):
            self.show_dialog("Error", "Please enter all fields.")
            return

        try:
            reminder_time = datetime.strptime(f"{hour_text}:{minute_text} {ampm_text}", '%I:%M %p').time()
        except ValueError:
            self.show_dialog("Error", "Invalid time format.")
            return

        current_time = datetime.now().time()
        current_datetime = datetime.now()

        reminder_datetime = datetime.combine(current_datetime.date(), reminder_time)

        if reminder_datetime < current_datetime:
            self.show_dialog("Error", "Please set a future time.")
            return

        time_difference = datetime.combine(datetime.today(), reminder_time) - datetime.combine(datetime.today(), current_time)
        time_seconds = time_difference.total_seconds()

        full_reminder_text = f"{reminder_text}\nMoral: {moral_text}" if moral_text else reminder_text
        threading.Timer(time_seconds, self.show_notification, [full_reminder_text]).start()

        self.show_dialog("Success", f"Reminder set for {hour_text}:{minute_text} {ampm_text}.")

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.7, 0.3),
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=self.dismiss_dialog
                )
            ]
        )
        self.dialog.open()

    def dismiss_dialog(self, obj):
        self.dialog.dismiss()


if __name__ == "__main__":
    NoteloopApp().run()
