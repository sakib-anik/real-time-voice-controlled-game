from vosk import Model,KaldiRecognizer
import pyaudio

model = Model("C:/Users/SAGOR155/PycharmProjects/game1/Vosk/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
stream.start_stream()
i=1
while True:
    data = stream.read(4096)
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        speech_as_text = recognizer.Result()[14:-3]
        x = speech_as_text.strip()
        print(i,".",x)
        i+=1
        if x == 'close':
            print(x)
            break