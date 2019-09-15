# SPDX-License-Identifier: BSD-2-Clause

# Audio streaming example using PyAudio + opuslib
# Change self._sendingPeer_ip, self._sendingPeer_port, self._receivingPeer_ip and self._receivingPeer_port accordingly
# Note: setting these ip to 'localhost' will prevent socket to bind to your external/LAN IP
# Use self._mode = "loop" to stream audio to own host. In loop mode it will work if you set the ip's to 'localhost'
# When streaming in "sender" or "receiver" mode set the same port for self._sendingPeer_port and self._receivingPeer_port
# Run this script with self._mode = "sender" in the computer that will stream the audio and with self._mode = "receiver" on computer that will receive the stream. Set IP's accordingly
# Sound card input and output devices are set by "self._input_device" and "self._output_device"

# This script uses version 3.0.1 of opuslib python binds of https://github.com/OnBeep/opuslib
# https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&mobileaction=toggle_view_desktop

import pyaudio
import time
import threading
import socket
import sys
import opuslib
import atexit

class opusStream():

    def __init__(self):
        # working mode
        self._mode = "loop"
        # self._mode = "sender"
        # self._mode = "receiver"

        # network config
        self._sendingPeer_ip = 'localhost'
        self._sendingPeer_port = 49005
        self._receivingPeer_ip = 'localhost'
        self._receivingPeer_port = 49006
        # sound config
        self.RATE = 48000
        self.CHANNELS = 1
        self.chunk = 3840
        self._input_device = 0 # pyaudio set device. See https://people.csail.mit.edu/hubert/pyaudio/docs/#class-stream
        self._output_device = 0
        self.FORMAT = pyaudio.paInt16

        # codec config
        self._opusbitrate = 128000
        self._opuscomplexity = 10 # This is the default

        # general
        self._loopthread = False
        self._socketout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self._socketin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self._enc = None
        self._dec = None
        self._streamin = None
        self._streamout = None
        self._timer = 0
        self._pyaudio = pyaudio.PyAudio()

    def startout(self):
        self._loopthread = True
        self._enc = opuslib.Encoder(self.RATE, self.CHANNELS, opuslib.APPLICATION_AUDIO)
        self._dec = opuslib.Decoder(self.RATE, self.CHANNELS)
        self._enc.complexity = self._opuscomplexity
        self._enc.bitrate = self._opusbitrate
        self.__runstreamin()
        self.__runstreamout()

        if self._mode == "sender":
            self._socketout.bind((self._sendingPeer_ip, self._sendingPeer_port))
            d = threading.Thread(target=self.__sendpacks, args=())
            d.setDaemon(True)
            d.start()
        if self._mode == "receiver":
            self._socketin.bind((self._receivingPeer_ip, self._receivingPeer_port))
            r = threading.Thread(target=self.__getpacks, args=())
            r.setDaemon(True)
            r.start()
        if self._mode == "loop":
            self._socketout.bind((self._sendingPeer_ip, self._sendingPeer_port))
            self._socketin.bind((self._receivingPeer_ip, self._receivingPeer_port))
            d = threading.Thread(target=self.__sendpacks, args=())
            d.setDaemon(True)
            d.start()
            r = threading.Thread(target=self.__getpacks, args=())
            r.setDaemon(True)
            r.start()

        atexit.register(self.__close)

    def __sendpacks(self):
        while self._loopthread == True:
            hh = self._streamin.read(self.chunk)
            enc = self._enc.encode(hh, self.chunk)
            self._socketout.sendto(enc, (self._receivingPeer_ip, self._receivingPeer_port))

    def __getpacks(self):
        while self._loopthread == True:
            data, addr = self._socketin.recvfrom(4096)
            deco = self._dec.decode(data, self.chunk)
            self._streamout.write(deco)
            self.__timer(len(deco), len(data))

    def __runstreamin(self):
        self._streamin = self._pyaudio.open(format=self.FORMAT,
                                            channels=self.CHANNELS,
                                            rate=self.RATE,
                                            input=True,
                                            input_device_index=self._input_device,
                                            frames_per_buffer=self.chunk)

    def __runstreamout(self):
        self._streamout = self._pyaudio.open(format=self.FORMAT,
                                             channels=self.CHANNELS,
                                             rate=self.RATE,
                                             output=True,
                                             output_device_index=self._output_device,
                                             frames_per_buffer=self.chunk)

    def __timer(self,PCMpacketSize,OPUSpacketSize):
        tt = int(time.time())
        if tt - self._timer > 2:
            rate = PCMpacketSize/OPUSpacketSize
            print("PCM packet size: " + str(PCMpacketSize))
            print("OPUS packet size: " + str(OPUSpacketSize))
            print("Compression: "+str(rate))
            print("=============================================")
            self._timer = tt

    def __close(self):
        print("EXIT")
        self._loopthread == False
        self._streamin.stop_stream()
        self._streamin.close()
        self._streamout.stop_stream()
        self._streamout.close()
        self._pyaudio.terminate()

A = opusStream()
A.startout()

while True:
    time.sleep(0.01)