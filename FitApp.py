import csv
import os
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
    with open(database_path, "w") as database:
        fieldnames = ["Date", "Chin-up", "Bench press", "Squat",
                     "Deadlift", "Row", "Farmer"]
        writer = csv.DictWriter(database,fieldnames=fieldnames)
        writer.writeheader()


class ButtonsPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.entered_reps = TextInput(multiline=False,readonly=True,halign="right",font_size=55)
        self.add_widget(self.entered_reps)

        buttons = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["C", "0", "ENTER"]
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
        elif button_pressed == "ENTER":
            if app.current_exercise == "Chin-up":
                app.chinup_stats[app.set_counter] = self.entered_reps.text
                self.entered_reps.text = ""
                print(f"Current set: {app.set_counter}")
                app.set_counter += 1
                print(f"Counter increased to {app.set_counter}")
                if app.set_counter == 4:
                    app.set_counter = 1    
                    app.screen_manager.current = "Exercises"
            print(app.chinup_stats)
        else:
            self.entered_reps.text += button_pressed




class Exercises(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        exercises = ["Chin-up", "Bench press", "Squat",
                     "Deadlift", "Row", "Farmer"]
        for exercise in exercises:
            exercise_button = Button(text=exercise)
            self.add_widget(exercise_button)
            exercise_button.bind(on_press=self.on_exercise_press)


    def on_exercise_press(self, instance):
        print(instance.text)
        app.current_exercise = instance.text
        app.screen_manager.current = "Buttons"


class DatePage(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = "vertical"

        self.date_label = Label(text="Insert today's date")
        self.add_widget(self.date_label)

        self.entered_date = TextInput(multiline=False,readonly=True,halign="center",
            font_size=55)
        self.add_widget(self.entered_date)

        buttons = [["1", "2", "3", "4", "5", "6"], ["7", "8", "9", "0", ".", "Enter"]]
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
            # tady dodelat datum
            app.todays_date = self.entered_date.text
            print(app.todays_date)
            app.screen_manager.current = "Exercises"
        else:
            self.entered_date.text += button_pressed 


    # def date_inserted(self, instance):
    #     # with open(database_path, "a") as database:
    #     MainApp().date = instance
    #     # print(MainApp().date)
    #     app.screen_manager.current = "Exercises"

class MainApp(App):
    set_counter = 1
    current_exercise = ""
    todays_date = ""
    overall_training = {}
    chinup_stats = {}
    deadlift_stats = {}
    bench_stats = {}
    squat_stats = {}
    row_stats = {}
    farmer_stats = {}
    def build(self):

        self.screen_manager = ScreenManager()

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

        return self.screen_manager


if __name__ == "__main__":
    app = MainApp()
    app.run()
