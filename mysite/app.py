
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True


class Wod:
    def __init__(self, *args):
        self.name = args[0]
        self.wod_type = args[1]
        self.time = args[2]
        self.exercises = [*args[3:]]

    def __str__(self):
        return self.name + ", " + self.wod_type + ", " + self.time + ", " + ", ".join(self.exercises)


def get_random_number(len):
    return random.randrange(len)


def get_current_week():
    """
    -weekday- corresponds to the position of the day of the week in a list,
    Monday = 0, Tuesday = 1 ... Sunday = 6.
    So to fill the -current_week- list with the number of the corresponding day, 
    -weekday- is used as the iterator of the position in the list. 
    """

    today = datetime.today()

    current_week  = []
    iterator = -today.weekday()
    for i in range(7):
        if iterator <= 0 :
            number_day = datetime.now() - timedelta(abs(iterator))
        else:
            number_day = datetime.now() + timedelta(abs(iterator))

        current_week.append(number_day.day)
        iterator += 1

    return current_week   

def get_workout_of_day():
    wods = []
    
    #with open('/home/trojmat201/mysite/bbdd/BBDD_Gymnastics_WODs.csv', 'r') as file:
    with open('./bbdd/BBDD_Gymnastics_WODs.csv', 'r') as file:
        lines =  file.readlines()

        for i in range(1, len(lines)):
            args = lines[i].split(',')
            args = list(filter(None, args))

            wods.append(Wod(*args))

    random_number = random.randrange(len(wods))
    return wods[random_number]


@app.route('/')
def index():
    today = datetime.today().strftime("%B %d, %Y")
    today_day = datetime.today().strftime("%a")
    today_number = datetime.now().day
    current_week = get_current_week()
    days_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    wod = get_workout_of_day()
    return render_template("main_page.html", wod=wod, today = today, current_week = current_week, today_number = today_number, today_day = today_day, days_name = days_name)

