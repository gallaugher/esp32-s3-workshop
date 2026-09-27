# mp3_play.py
import board, audiobusio
from audiomp3 import MP3Decoder

# I2S DAC wiring: WSEL -> GPIO16, DIN -> GPIO17, BCK -> GPIO18
audio = audiobusio.I2SOut(bit_clock=board.GPIO18, word_select=board.GPIO16, data=board.GPIO17)

# Folder on CIRCUITPY where the sound files live
path = "sounds/"

# Create the decoder ONCE (it needs a lot of RAM) and pass it a file on your board
decoder = MP3Decoder(path + "encouragement1.mp3")

# Pass in the file name, including the .mp3 extension
def play_mp3(filename):
   decoder.open(path + filename)   # closes the previous file, opens the new one
   audio.play(decoder)
   while audio.playing:
       pass   # add code here that you want to run while the sound plays

print("mp3 sound playing")
play_mp3("mo-funk.mp3")