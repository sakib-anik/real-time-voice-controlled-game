from vosk import Model,KaldiRecognizer
import pyaudio

model = Model("C:/Users/SAGOR155/PycharmProjects/game1/Vosk/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        x = recognizer.Result()[14:-3]
        print(x)
        if x == 'close':
            print(x)
            break