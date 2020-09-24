import csv
import shutil
import os
import ast
import datetime
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from android.permissions import request_permissions, Permission

request_permissions([Permission.WAKE_LOCK])
request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

database_path = "./database.csv"
database_copy_path = "/storage/emulated/0/FitAppDatabase"

if not os.path.exists(database_path):
    with open(database_path, "w", newline="") as database:
        fieldnames = ["Date", "Chin-up", "Bench press", "Squat",
                      "Deadlift", "Row", "Farmer"]
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()


class StartExitPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        self.start_button = Button(text="Start Training", font_size=60)
        self.start_button.bind(on_press=self.start_training)
        self.add_widget(self.start_button)

        self.quit_button = Button(text="Quit app", font_size=60)
        self.quit_button.bind(on_press=self.quit_app)
        self.add_widget(self.quit_button)

    def start_training(self, _):
        app.screen_manager.current = "Date"

    def quit_app(self, _):
        app.stop()


class DatePage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"

        self.date_label = Label(text=f"Insert today's date in \n DD.MM.YYYY format",font_size=45)
        self.add_widget(self.date_label)

        self.entered_date = TextInput(multiline=False,readonly=True,font_size=140,halign="center")
        self.add_widget(self.entered_date)

        buttons = [["1", "2", "3", ""],
                   ["4", "5", "6", ""],
                   ["7", "8", "9", "Back"],
                   ["0", ".", "C", "Enter"]]

        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number, font_size=30)
                button.bind(on_press=self.on_button_press_date)
                h_layout.add_widget(button)
            self.add_widget(h_layout)

    def on_button_press_date(self, instance):
        button_pressed = instance.text
        if button_pressed == "Enter":
            app.todays_date = self.entered_date.text
            app.overall_training["Date"] = app.todays_date
            app.screen_manager.current = "Exercises"
            # if len(self.entered_date.text) != 10:
            #     pass
            # else:
            #     app.todays_date = self.entered_date.text
            #     app.overall_training["Date"] = app.todays_date
            #     print(app.overall_training)
            #     print(app.previous_training)
            #     app.screen_manager.current = "Exercises"
        elif button_pressed == "C":
            self.entered_date.text = ""
        elif button_pressed == "Back":
            app.screen_manager.current = "StartExit"
        else:
            self.entered_date.text += button_pressed


class ExercisesPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.spacing = 1
        exercises = ["Chin-up", "Bench press", "Squat",
                     "Deadlift", "Row", "Farmer"]
        for exercise in exercises:
            previous_set_rep = ast.literal_eval(app.previous_training[exercise])[1]
            self.exercise_button = Button(text=f"{exercise}\n\nWeight: {previous_set_rep[0]}\nReps: {previous_set_rep[1]}",
                                          font_size=45, halign="center")
            self.add_widget(self.exercise_button)
            self.exercise_button.bind(on_press=self.on_exercise_press)

    def on_exercise_press(self, instance):
        app.current_exercise = instance.text.split("\n")[0]
        dicted_previous_training = ast.literal_eval(app.previous_training[instance.text.split("\n")[0]])
        dicted_previous_training_stringed = (
            f"{dicted_previous_training[1][0]}: {dicted_previous_training[1][1]}    "
            f"{dicted_previous_training[2][0]}: {dicted_previous_training[2][1]}    "
            f"{dicted_previous_training[3][0]}: {dicted_previous_training[3][1]}    "
            )
        app.buttons_page.last_training_displayed.text = f"Last training weights and reps:\n{dicted_previous_training_stringed}"
        app.screen_manager.current = "Weight"


class WeightPage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"

        self.weight_label = Label(text="Insert weight", font_size=60)
        self.add_widget(self.weight_label)

        self.entered_weight = TextInput(multiline=False, readonly=True, font_size=140, halign="center")
        self.add_widget(self.entered_weight)

        buttons = [["1", "2", "3", "Exercises"],
                   ["4", "5", "6", ""],
                   ["7", "8", "9", ""],
                   ["0", ".", "C", "Enter"]]
        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number, font_size=40)
                button.bind(on_press=self.on_button_press_weight)
                h_layout.add_widget(button)
            self.add_widget(h_layout)

    def on_button_press_weight(self, instance):
        button_pressed = instance.text
        if button_pressed == "Enter":
            app.weight = self.entered_weight.text
            self.entered_weight.text = ""
            app.screen_manager.current = "Buttons"
        elif button_pressed == "C":
            self.entered_weight.text = ""
        elif button_pressed == "Exercises":
            self.entered_weight.text = ""
            app.screen_manager.current = "Exercises"
        else:
            self.entered_weight.text += button_pressed


class ButtonsPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.last_training_displayed = Label(font_size=45, halign="center")
        self.add_widget(self.last_training_displayed)

        self.entered_reps = TextInput(multiline=False, readonly=True, font_size=140, halign="center")
        self.add_widget(self.entered_reps)

        buttons = [["1", "2", "3", "Weight"],
                   ["4", "5", "6", "Exercises"],
                   ["7", "8", "9", ""],
                   ["0", ".", "C", "Enter"]]

        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number, font_size=40)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)

    def on_button_press(self, instance):
        button_pressed = instance.text

        if button_pressed == "C":
            self.entered_reps.text = ""
        elif button_pressed == "Exercises":
            app.current_exercise_dict = {}
            app.set_counter = 1
            app.screen_manager.current = "Exercises"
        elif button_pressed == "Weight":
            app.screen_manager.current = "Weight"
        elif button_pressed == "Enter":
            app.current_exercise_dict[app.set_counter] = (float(app.weight), int(self.entered_reps.text))
            self.entered_reps.text = ""
            app.set_counter += 1
            app.start_time = datetime.datetime.now()
            app.screen_manager.current = "Timer"
            if app.set_counter == 4:
                for exercise_object in app.exercises_page.children:
                    if exercise_object.text.split("\n")[0] == app.current_exercise:
                        exercise_object.background_normal = ""
                        exercise_object.background_color = (0.31, 0.74, 0.2, 1)
                app.set_counter = 1
                app.overall_training[app.current_exercise] = app.current_exercise_dict
                app.current_exercise_dict = {}
                app.screen_manager.current = "Exercises"
            if len(app.overall_training) == 7:
                app.difference_page.diff_calculation(app.previous_training, app.overall_training)
                app.screen_manager.current = "Difference"
        else:
            self.entered_reps.text += button_pressed


class TimerPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer_button = Button(font_size=120)
        self.timer_button.bind(on_press=self.on_button_press)
        self.add_widget(self.timer_button)
        self.start_time = datetime.datetime.now()
        Clock.schedule_interval(self.timer, 0.1)
    
    def timer(self, dt):
        actual_time = datetime.datetime.now()
        time_difference = actual_time - app.start_time
        self.timer_button.text = str(time_difference)[2:7]

    def on_button_press(self, instance):
        app.screen_manager.current = "Buttons"


class DifferencePage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.description = (
            f"Difference of reps\n from previous training\n"
            f"('-' if diff. weight)\nPress for save&exit\n\n\n\n"
            )
        self.difference = ""

    def diff_calculation(self, stary, novy):
        for exercise_prev_training, data_prev_training in stary.items():
            for exercise_curr_training, data_curr_training in novy.items():
                if exercise_curr_training == exercise_prev_training:
                    if exercise_curr_training == "Date":
                        pass
                    else:
                        exercise_diff = f"{exercise_curr_training+':':<13}"
                        data_prev_training = ast.literal_eval(data_prev_training)
                        for set_nr in data_prev_training.keys():
                            if data_prev_training[set_nr][0] == data_curr_training[set_nr][0]:
                                diff = data_curr_training[set_nr][1] - data_prev_training[set_nr][1]
                                if diff == 0:
                                    exercise_diff += f"{0:>2} "
                                elif diff > 0:
                                    exercise_diff += f"+{diff} "
                                else:
                                    exercise_diff += f"{diff} "
                            else:
                                exercise_diff += f" - "
                        self.difference += f"{exercise_diff}\n"

        self.difference_button = Button(text=f"{self.description}\n{self.difference}",
                                        font_size=45, halign="center", font_name="CourierPrime-Regular")
        self.difference_button.bind(on_press=self.save_quit)
        self.add_widget(self.difference_button)

    def save_quit(self, instance):
        with open(database_path, "a", newline="") as database:
            fieldnames = ["Date", "Chin-up", "Bench press", "Squat",
                          "Deadlift", "Row", "Farmer"]
            writer = csv.DictWriter(database, fieldnames=fieldnames)
            writer.writerow(app.overall_training)
        shutil.copy2(database_path, database_copy_path)
        app.stop()


class MainApp(App):
    start_time = datetime.datetime.now()
    set_counter = 1
    current_exercise = ""
    todays_date = ""
    weight = ""
    overall_training = {}
    current_exercise_dict = {}
    previous_training = {}

    def build(self):
        with open(database_path, "r", newline="") as database:
            reader = csv.DictReader(database)
            for row in reader:
                self.previous_training = row

        self.screen_manager = ScreenManager()

        self.start_exit_page = StartExitPage()
        screen = Screen(name="StartExit")
        screen.add_widget(self.start_exit_page)
        self.screen_manager.add_widget(screen)

        self.date_page = DatePage()
        screen = Screen(name="Date")
        screen.add_widget(self.date_page)
        self.screen_manager.add_widget(screen)
        
        self.exercises_page = ExercisesPage()
        screen = Screen(name='Exercises')
        screen.add_widget(self.exercises_page)
        self.screen_manager.add_widget(screen)
        
        self.buttons_page = ButtonsPage()
        screen = Screen(name="Buttons")
        screen.add_widget(self.buttons_page)
        self.screen_manager.add_widget(screen)

        self.weight_page = WeightPage()
        screen = Screen(name="Weight")
        screen.add_widget(self.weight_page)
        self.screen_manager.add_widget(screen)

        self.timer_page = TimerPage()
        screen = Screen(name="Timer")
        screen.add_widget(self.timer_page)
        self.screen_manager.add_widget(screen)

        self.difference_page = DifferencePage()
        screen = Screen(name="Difference")
        screen.add_widget(self.difference_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    app = MainApp()
    app.run()
