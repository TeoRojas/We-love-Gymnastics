
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template
import random
from datetime import date

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

wods = []
with open('/home/trojmat201/mysite/bbdd/BBDD_Gymnastics_WODs.csv', 'r') as file:
    lines =  file.readlines()

    for i in range(1, len(lines)):
        args = lines[i].split(',')
        args = list(filter(None, args))

        wods.append(Wod(*args))

random_number = random.randrange(len(wods))
#print(wods[random_number])
wod = wods[random_number]

today = date.today().strftime("%B %d, %Y")

@app.route('/')
def index():
    return render_template("main_page.html", wod=wod, today=today)

