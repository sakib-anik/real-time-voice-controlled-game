from tkinter import *
import random
from vosk import Model,KaldiRecognizer
import pyaudio
from threading import Thread
import logging
model = Model("C:/Users/SAGOR155/PycharmProjects/game1/Vosk/vosk-model-small-bn-0.22")
recognizer = KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
stream.start_stream()
GAME_WIDTH = 700
GAME_HEIGHT = 500
SPEED = 1000#the lower the number the faster the game
SPACE_SIZE = 25#FOOD AND BODY PART OF THE SNAKE
BODY_PARTS = 3#BODY PARTS AT THE BEGINNING OF THE GAME
SNAKE_COLOR = "#00FF00"#green_snake
FOOD_COLOR = "#FF0000"#Red_food
BACKGROUND_COLOR = "#000000"#black_background

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        #list of coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])#snake will appear in the top left corner

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collision(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

def on_closing():
    window.destroy()

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score),font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
                #print('')
                if x == 'बोलो' or x == 'बॉन्ड' or x == 'बॉन्ड हो' or x == 'वॉन हो' or x == 'बॉन्डों' or x == 'बूंदों' or x == 'दोनों' or x == 'बंद' or x == 'बंद हुआ' or x == 'बंद हो' or x == 'हुआ' or x == 'बौद्धों' or x == 'दो' or x == 'बांधों' or x == 'पंद्रह' or x == 'हो' or x == 'बोल्ड हो' or x == 'बॉन्ड व':
                    window.destroy()
                    #window.protocol("WM_DELETE_WINDOW", on_closing)
                    #print(x)
                    #break
                elif x == 'में' or x == 'बारह में' or x == 'बम में' or x == 'बावन' or x == 'बाद में' or x == 'हमें' or x == 'भवें' or x == 'बंद हो' or x == 'वह में' or x == 'बा में' or x == 'बानवे' or x == 'भाव में':
                    print("বামে")
                    x = 'left'
                    add = lambda x: change_direction(x)
                    add(x)
                elif x == 'दान है' or x == 'दाने' or x == 'डॉन है' or x == 'है' or x == 'गाने है' or x == 'ने' or x == 'मेनन' or x == 'डॉ ने' or x == 'धन है' or x == 'डॉन' or x == 'ठाणे' or x == 'उन्होंने' or x == 'दान' or x == 'नाना' or x == 'डालें' or x == 'गाने':
                    print("ডানে")
                    x = 'right'
                    add = lambda x: change_direction(x)
                    add(x)
                elif x == 'उप्र' or x =='वो रहे हैं' or x == 'वह' or x == 'उपर उपर' or x == 'ऊपर' or x == 'उपर एक' or x == 'उभरे' or x == 'ऊपर है' or x == 'उपर' or x == 'बड़े' or x == 'उपर है' or x == 'और' or x == 'गुर्दे' or x == 'उधर' or x == 'पढ़ें' or x == 'तो पढ़ें' or x == 'उबर' or x == 'ऊपर एक':
                    print("উপরে")
                    x = 'up'
                    add = lambda x: change_direction(x)
                    add(x)
                elif x == 'नेचर' or x == 'बेचें' or x == 'नीचे' or x == 'निश्चय' or x == 'डीजे':
                    print("নিচে")
                    x = 'down'
                    add = lambda x: change_direction(x)
                    add(x)



#window.bind('<Left>', lambda event: change_direction('left'))
#window.bind('<Right>', lambda event: change_direction('right'))
#window.bind('<Up>', lambda event: change_direction('up'))
#window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)
myClassA()
window.mainloop()