#imports
import turtle
import time
import random
from vosk import Model,KaldiRecognizer
import pyaudio
from threading import Thread

model = Model("C:/Users/sakib/PycharmProjects/pythonProject/Vosk/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
stream.start_stream()


delay = 0.1

#scores
score = 0
high_score = 0

#set up screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor('yellow')
wn.setup(width=600, height=600)
wn.tracer(0)

#snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

#snake food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

#scoreboards
sc = turtle.Turtle()
sc.speed(0)
sc.shape("square")
sc.color("black")
sc.penup()
sc.hideturtle()
sc.goto(0,260)
sc.write("score: 0 High score: 0", align = "center", font=("ds-digital", 24, "normal"))

#Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

class myClassA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            data = stream.read(4096)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                speech_as_text = recognizer.Result()[14:-3]
                x = speech_as_text.strip()#removes white spaces from beginning and end
                #logging.debug(x)
                print(x)
                if x == 'close' or x == 'plus' or x == 'clark' or x == 'those' or x == 'cool' or x == 'lol':
                    wn.bye()
                    #window.protocol("WM_DELETE_WINDOW", on_closing)
                    #print(x)
                    #break
                elif x == 'left' or x == 'let' or x == 'lived' or x == 'it':
                    print("left listened")
                    go_left()
                    #x = 'left'
                    #add = lambda x: change_direction(x)
                    #add(x)
                elif x == 'right' or x == 'plug' or x == 'pride':
                    print("right listened")
                    go_right()
                elif x == 'start' or x == 'that' or x == 'stat' or x == 'touch' or x == 'up' or x == 'oh':
                    print("up listened")
                    go_up()
                elif x == 'down' or x == 'damn' or x == 'doubt' or x == 'town':
                    print("down listened")
                    go_down()

#keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

#Mainloop
while True:
    data = stream.read(4096)
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        speech_as_text = recognizer.Result()[14:-3]
        x = speech_as_text.strip()  # removes white spaces from beginning and end
        # logging.debug(x)
        print(x)
        if x == 'close' or x == 'plus' or x == 'clark' or x == 'those' or x == 'cool' or x == 'lol':
            wn.bye()
        elif x == 'left' or x == 'let' or x == 'lived' or x == 'it':
            print("left listened")
            go_left()
            # x = 'left'
            # add = lambda x: change_direction(x)
            # add(x)
        elif x == 'right' or x == 'plug' or x == 'pride':
            print("right listened")
            go_right()
        elif x == 'start' or x == 'that' or x == 'stat' or x == 'touch' or x == 'up' or x == 'oh':
            print("up listened")
            go_up()
        elif x == 'down' or x == 'damn' or x == 'doubt' or x == 'town':
            print("down listened")
            go_down()

    wn.update()

    #check collision with the border area
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        #hide the segments of body
        for segment in segments:
            segment.goto(1000,1000) #out of range
        #clear the segments
        segments.clear()

        #reset score
        score = 0

        #reset delay
        delay = 0.1

        sc.clear()
        sc.write("score: {} High score: {}".format(score, high_score), align="center", font=("ds-digital", 24, "normal"))

    #check collision with food
    if head.distance(food) <20:
        # move the food to random place
        x = random.randint(-290,290)
        y = random.randint(-290,290)
        food.goto(x,y)

        #add a new segment to the head
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("black")
        new_segment.penup()
        segments.append(new_segment)

        #shorten the delay
        delay -= 0.001
        #increase the score
        score += 10

        if score > high_score:
            high_score = score
        sc.clear()
        sc.write("score: {} High score: {}".format(score,high_score), align="center", font=("ds-digital", 24, "normal"))

    #move the segments in reverse order
    for index in range(len(segments)-1,0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
    #move segment 0 to head
    if len(segments)>0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    #check for collision with body
    for segment in segments:
        if segment.distance(head)<20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

        #hide segments
        for segment in segments:
            segment.goto(1000,1000)
        segments.clear()
        score = 0
        delay = 0.1

        #update the score
        sc.clear()
        sc.write("score: {} High score: {}".format(score,high_score), align="center", font=("ds-digital", 24, "normal"))
    time.sleep(delay)
myClassA()
wn.mainloop()

