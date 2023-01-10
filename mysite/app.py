from flask import Flask, render_template
import random
from datetime import datetime, timedelta
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()

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


def get_all_wods():
    wods = []

    with open(THIS_FOLDER / 'static/bbdd/BBDD_Gymnastics_WODs.csv', 'r') as file:
        lines =  file.readlines()

        for i in range(1, len(lines)):
            args = lines[i].split(',')
            args = list(filter(None, args))

            wods.append(Wod(*args))

    return wods


def get_wods_done():
    wods_done = []

    with open(THIS_FOLDER / 'static/bbdd/WODs_done.csv', 'r') as file:
        for line in file:
            wods_done.append(int(line))

    return wods_done


def get_wod_number_not_done(num_wods, wods_done):
    """obtaining a WOD that has not
    yet been done (is not in the list of events)"""

    if len(wods_done) == num_wods:
        """If all WODs are done, reset
        the WODs_done file"""
        open(THIS_FOLDER / 'static/bbdd/WODs_done.csv','w').close()

    wod_number_not_done = random.randrange(num_wods)

    while wod_number_not_done in wods_done:
        wod_number_not_done = random.randrange(num_wods)

    print('WOD number not done: -' + str(wod_number_not_done) + '-')
    print(wods_done)

    return wod_number_not_done


def set_wod_done_in_file(wod_number_done):
    with open(THIS_FOLDER / 'static/bbdd/WODs_done.csv', 'a') as file:
        file.write(str(wod_number_done)+'\n')

print(THIS_FOLDER)
wods = get_all_wods()
wods_done = get_wods_done()
wod_number = get_wod_number_not_done(int(len(wods)), wods_done)
set_wod_done_in_file(wod_number)
wod = wods[wod_number]


@app.route('/')
def index():
    today = datetime.today().strftime("%B %d, %Y")
    today_day = datetime.today().strftime("%a")
    today_number = datetime.now().day
    current_week = get_current_week()
    days_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return render_template("main_page.html", wod=wod, today = today, current_week = current_week, today_number = today_number, today_day = today_day, days_name = days_name)


if __name__ == '__main__':
    app.run(debug=True)
