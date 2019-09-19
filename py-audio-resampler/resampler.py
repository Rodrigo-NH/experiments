import subprocess
import shlex
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
p = pyaudio.PyAudio()

streamout = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        output = True,
        output_device_index = 0
        )

#https://stackoverflow.com/questions/48725405/how-to-read-binary-data-over-a-pipe-from-another-process-in-python
def resample(command):
    process = subprocess.Popen(shlex.split(command), shell=False, stdout=subprocess.PIPE, universal_newlines=False)
    while True:
        buffer = bytearray(1920) #10ms of 16bit PCM stereo audio at 48000Hz = 1920 bytes
        numberOfBytesReceived = process.stdout.readinto(buffer)
        data = bytes(buffer)
        streamout.write(data)
        if numberOfBytesReceived <= 0:
            break
    rc = process.poll()

command = 'sox /home/rod/opusdev/rewind44.mp3 -r 48000 -t raw -e signed -b 16 -c 2 -'
resample(command)