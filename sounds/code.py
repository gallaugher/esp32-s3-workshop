# mp3_play.py
import board, neopixel, time, audiobusio, pwmio
from audiocore import WaveFile # only needed for wav
from audiomp3 import MP3Decoder

audio = audiobusio.I2SOut(bit_clock=board.GPIO18, word_select=board.GPIO16, data=board.GPIO17)

# set path to the folder where the sound files can be found on the device, example below is for a folder named alarm
path = "sounds/"
# set up the mp3 decoder
filename = "encouragement1.mp3" # change to valid file in your path
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)

# Call this function passing in a String for the full filename with extension.
def play_mp3(filename):
    decoder.file = open(path + filename, "rb") 
    audio.play(decoder)
    while audio.playing:
        pass # add code here that you want to run while sound plays

def play_sound(filename):
   with open(path + filename, "rb") as wave_file:
       wave = WaveFile(wave_file)
       audio.play(wave)
       while audio.playing:
           pass

print("Rewire 2")
play_mp3("encouragement1.mp3") # call the function to play an mp3 file
# play_sound("wand.wav") # call the function to play a wav file