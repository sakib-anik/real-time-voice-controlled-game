import pygame
import random
from vosk import Model,KaldiRecognizer
import pyaudio
from threading import Thread
model = Model("C:/Users/SAGOR155/PycharmProjects/game1/Vosk/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
stream.start_stream()

done = False

pressing_down = False

colors = [
    (255, 182, 204),
    (0, 51, 204),
    (0, 204, 0),
    (255, 102, 0),
    (204, 51, 255),
    (153, 0, 51),
    (0, 204, 255)
]

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
                    print('close listened')
                    global done
                    done = True
                    #window.protocol("WM_DELETE_WINDOW", on_closing)
                    #print(x)
                    #break
                elif x == 'left' or x == 'let' or x == 'lived' or x == 'it':
                    print("left listened")
                    x = 'left'
                    game.go_side(-1)
                elif x == 'right' or x == 'plug' or x == 'pride':
                    print("right listened")
                    x = 'right'
                    game.go_side(1)
                elif x == 'start' or x == 'that' or x == 'stat' or x == 'touch' or x == 'up' or x == 'oh':
                    print("up listened")
                    x = 'up'
                    game.rotate()

                elif x == 'down' or x == 'damn' or x == 'doubt' or x == 'town':
                    print("down listened")
                    x = 'down'
                    global pressing_down
                    pressing_down = True

                elif x == 'space' or x == 'stairs':
                    print('space listened')
                    game.go_space()

class Figures:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation +1) % len(self.figures[self.type])

class Tetris:
    level = 0.1#measures speed of falling
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figures(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width -1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines +=1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

pygame.init()

GREEN = (0, 51, 0)
NAVY = (0, 0, 102)
GREYBLUE = (102, 153, 153)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('BEST Tetris Game')



clock = pygame.time.Clock()
fps = 25
game = Tetris(20,10)
counter = 0



while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    print(counter)
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    #myClassA()
    data = stream.read(4096)
        #if len(data) == 0:
        #    break

    if recognizer.AcceptWaveform(data):
        speech_as_text = recognizer.Result()[14:-3]
        x = speech_as_text.strip()  # removes white spaces from beginning and end
        # logging.debug(x)
        print(x)
        if x == 'close' or x == 'plus' or x == 'clark' or x == 'those' or x == 'cool' or x == 'lol':
            print('close listened')
            done = True
            # window.protocol("WM_DELETE_WINDOW", on_closing)
            # print(x)
            # break
        elif x == 'left' or x == 'let' or x == 'lived' or x == 'it':
            print("left listened")
            x = 'left'
            game.go_side(-1)
        elif x == 'right' or x == 'plug' or x == 'pride':
            print("right listened")
            x = 'right'
            game.go_side(1)
        elif x == 'start' or x == 'that' or x == 'stat' or x == 'touch' or x == 'up' or x == 'oh':
            print("up listened")
            x = 'up'
            game.rotate()

        elif x == 'down' or x == 'damn' or x == 'doubt' or x == 'town':
            print("down listened")
            x = 'down'
            pressing_down = True

        elif x == 'space' or x == 'stairs' or x == 'stage' or x == 'step' or x == 'tess':
            print('space listened')
            game.go_space()

    screen.fill(GREYBLUE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, NAVY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, GREEN)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("say close", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()



