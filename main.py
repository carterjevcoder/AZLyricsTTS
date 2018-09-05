# AUTHOR: Carter Jevens
# PROGRAM: lyrics2mp3
# PURPOSE: Takes a users input of a song, finds the AZlyrics page for it, then gives an mp3 of the text to speech
# of that song. This is probably optimized horribly.
# NOTE: I needed to install AVBin in order for the mp3 creation and play to work.

#imports needed to scrape HTML and convert to mp3
from bs4 import BeautifulSoup
import requests
from gtts import gTTS
import pyglet


#getting user input, loop makes sure the format is correct
bandSong = "Artist - Song"
bandSong = input("Please enter a song in the format of 'Artist - Song': ")
correctForm = bandSong.find(' - ')
while correctForm == -1:
    bandSong = input("Error, enter with the correct format. 'Artist - Song': ")
    correctForm = bandSong.find(' - ')
    if correctForm != -1: break

#drop it into lowercase, split, add necessary things for the URL
bandSong = bandSong.lower()
appendedSong = bandSong.split(' - ')

songTitle = appendedSong[1] + '.mp3'

appendedSong[0] = ''.join(appendedSong[0].split())
appendedSong[1] = ''.join(appendedSong[1].split())

appendedSong[0] = appendedSong[0] + '/'
appendedSong[1] = appendedSong[1] + '.html'

link = "https://www.azlyrics.com/lyrics/" + ''.join(appendedSong)

#shows link to the lyrics
print(link)

#requests for HTTPS
r = requests.get(link)

#scraping HTML using bs4
soup = BeautifulSoup(r.content, 'html.parser')

#makes a list using div tag in html in order to search for the lyrics block (no id on it)
p = soup.prettify()
divided = p.split('div>')

#worst part of the code, trying to get rid of the trash that isnt lyrics.
textBlock = divided[19].replace("<br/>", "").replace("<i>", "").replace("</i>", "").replace("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->", "").replace("<[Hook:]>", "").replace("[Intro:]", "").replace("[Outro:]", "").replace("[Outro x2:]", "").replace("[Hook]", "").replace("</", "").replace("[Verse 1:]", "").replace("[Verse 2:]", "").replace("[Verse 3:]", "").replace("[Verse 4:]", "")

#creation of mp3
tts = gTTS(text=textBlock, lang='en')
tts.save(songTitle)

#playing of mp3
music = pyglet.resource.media(songTitle, streaming=False)
music.play()
pyglet.app.run()

#god please make this script stop someone help pls