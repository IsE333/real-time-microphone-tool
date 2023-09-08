import pyaudio
import numpy as np
import threading
import gui


CHUNK = 2**2
RATE = 44100
LEN = 10
MULTIPLIER = 20

active = True


def play(stream, player, windowGui):
    while active:
        data = np.frombuffer(
            stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16
        )
        data = data * MULTIPLIER
        windowGui.updateData(data)
        player.write(data, CHUNK)


def consoleT(windowGui):
    while input() != "q":
        pass
    windowGui.running = False


if __name__ == "__main__":
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)["maxInputChannels"] == 0:
            print(p.get_device_info_by_index(i))
            print()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=RATE,
        input=True,
        input_device_index=1,
        frames_per_buffer=CHUNK,
    )

    player = p.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=RATE,
        output=True,
        output_device_index=26,
        frames_per_buffer=CHUNK,
    )

    windowGui = gui.GUI()
    print("gui start")

    playThread = threading.Thread(
        target=play, args=(stream, player, windowGui), daemon=True
    )
    playThread.start()

    consoleThread = threading.Thread(target=consoleT, args=(windowGui,), daemon=True)
    consoleThread.start()
    print("q to quit")

    windowGui.run()

    active = False

    stream.stop_stream()
    stream.close()
    p.terminate()
