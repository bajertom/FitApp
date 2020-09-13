import csv
import os
import ast
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

database_path = "C:\\Study\\Environments\\FitApp\\database.csv"
if not os.path.exists(database_path):
    with open(database_path, "w",newline="") as database:
        fieldnames = ["Date", "Chin-up", "Bench press", "Squat",
                     "Deadlift", "Row", "Farmer"]
        writer = csv.DictWriter(database,fieldnames=fieldnames)
        writer.writeheader()


class StartExitPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        self.start_button = Button(text="Start Training")
        self.start_button.bind(on_press=self.start_training)
        self.add_widget(self.start_button)

        self.quit_button = Button(text="Quit app")
        self.quit_button.bind(on_press=self.quit_app)
        self.add_widget(self.quit_button)


    def start_training(self,_):
        app.screen_manager.current = "Date"


    def quit_app(self,_):
        app.stop()


class DatePage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"

        self.date_label = Label(text="Insert today's date in DD.MM.YYYY format")
        self.add_widget(self.date_label)

        self.entered_date = TextInput(multiline=False,readonly=True,halign="center",
            font_size=55)
        self.add_widget(self.entered_date)

        buttons = [["1", "2", "3", "4", "5", "6", "Back"], ["7", "8", "9", "0", ".", "C","Enter"]]
        main_layout = BoxLayout(orientation="vertical")
        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number)
                button.bind(on_press=self.on_button_press_date)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        self.add_widget(main_layout)


    def on_button_press_date(self,instance):
        button_pressed = instance.text
        if button_pressed == "Enter":
            app.todays_date = self.entered_date.text
            app.overall_training["Date"] = app.todays_date
            # print(app.overall_training)
            # print(app.previous_training)
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

class Exercises(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        exercises = ["Chin-up", "Bench press", "Squat",
                     "Deadlift", "Row", "Farmer"]
        for exercise in exercises:
            previous_set_rep = ast.literal_eval(app.previous_training[exercise])[1]
            # print(slovnik)
            # print(type(slovnik))
            exercise_button = Button(text=f"{exercise}\n\nWeight: {previous_set_rep[0]}\nReps: {previous_set_rep[1]}",
                halign="center")
            self.add_widget(exercise_button)
            exercise_button.bind(on_press=self.on_exercise_press)


    def on_exercise_press(self, instance):
        # print(instance.text.split("\n")[0])
        app.current_exercise = instance.text.split("\n")[0]
        dicted_previous_training = ast.literal_eval(app.previous_training[instance.text.split("\n")[0]])
        dicted_previous_training_stringed = (
        f"{dicted_previous_training[1][0]}: {dicted_previous_training[1][1]}    "
        f"{dicted_previous_training[2][0]}: {dicted_previous_training[2][1]}    "
        f"{dicted_previous_training[3][0]}: {dicted_previous_training[3][1]}    ")
        # print(dicted_previous_training_stringed)
        app.buttons_page.last_training_displayed.text = f"Last training weights and reps:\n{dicted_previous_training_stringed}"
        # print(type(app.buttons_page.last_training_displayed.text))
        
        app.screen_manager.current = "Weight"



class WeightPage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"


        self.weight_label = Label(text="Insert weight")
        self.add_widget(self.weight_label)

        self.entered_weight = TextInput(multiline=False,readonly=True,halign="center",
            font_size=55)
        self.add_widget(self.entered_weight)

        buttons = [["1", "2", "3", "4", "5", "6","Exercises"], ["7", "8", "9", "0", ".","C","Enter"]]
        main_layout = BoxLayout(orientation="vertical")
        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number)
                button.bind(on_press=self.on_button_press_weight)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        self.add_widget(main_layout)


    def on_button_press_weight(self, instance):
        button_pressed = instance.text
        if button_pressed == "Enter":
            app.weight = self.entered_weight.text
            # print(app.overall_training)
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

        self.last_training_displayed = Label(font_size=30,halign="center")
        self.add_widget(self.last_training_displayed)

        self.entered_reps = TextInput(multiline=False,readonly=True,halign="right",font_size=55)
        self.add_widget(self.entered_reps)

        buttons = [
            ["1", "2", "3", "Weight"],
            ["4", "5", "6", "Exercises"],
            ["7", "8", "9", "."],
            ["C", "0", "ENTER", "Timer"]
            ]

        for row in buttons:
            h_layout = BoxLayout()
            for number in row:
                button = Button(text=number)
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
        elif button_pressed == "ENTER":
            app.current_exercise_dict[app.set_counter] = (app.weight, self.entered_reps.text)
            # print(f"Current set: {app.set_counter}, number of reps: {self.entered_reps.text}")
            self.entered_reps.text = ""
            app.set_counter += 1
            if app.set_counter == 4:
                app.set_counter = 1
                app.overall_training[app.current_exercise] = app.current_exercise_dict
                app.current_exercise_dict = {}
                app.screen_manager.current = "Exercises"
                # print(app.overall_training)
                # print(len(app.overall_training))

            if len(app.overall_training) == 7:
                with open(database_path, "a",newline="") as database:
                    fieldnames = ["Date", "Chin-up", "Bench press", "Squat",
                                 "Deadlift", "Row", "Farmer"]
                    writer = csv.DictWriter(database,fieldnames=fieldnames)
                    writer.writerow(app.overall_training)
                app.stop()
        else:
            self.entered_reps.text += button_pressed


class MainApp(App):
    set_counter = 1
    current_exercise = ""
    todays_date = ""
    weight = ""
    overall_training = {}
    current_exercise_dict = {}
    previous_training = {}
    # print(type(previous_training))




    def build(self):
        with open(database_path, "r",newline="") as database:
            reader = csv.DictReader(database)
            for row in reader:
                self.previous_training = row
                # print(type(self.previous_training))

        self.screen_manager = ScreenManager()

        self.start_exit_page = StartExitPage()
        screen = Screen(name="StartExit")
        screen.add_widget(self.start_exit_page)
        self.screen_manager.add_widget(screen)

        self.date_page = DatePage()
        screen = Screen(name="Date")
        screen.add_widget(self.date_page)
        self.screen_manager.add_widget(screen)
        
        self.exercises = Exercises()
        screen = Screen(name='Exercises')
        screen.add_widget(self.exercises)
        self.screen_manager.add_widget(screen)
        
        self.buttons_page = ButtonsPage()
        screen = Screen(name="Buttons")
        screen.add_widget(self.buttons_page)
        self.screen_manager.add_widget(screen)

        self.weight_page = WeightPage()
        screen = Screen(name="Weight")
        screen.add_widget(self.weight_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    app = MainApp()
    app.run()
