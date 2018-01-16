import re, time
import urllib.request
from bs4 import BeautifulSoup
import train, get_lyrics

"""
The DeepSong interface.
"""

def get_all_lyrics(artists, filename):
    lyrics = ''
    for artist in artists:
        print('>>> Collecting lyrics of: ' + artist + '...')
        lyrics += get_lyrics.get_lyrics(artist)

    file = open(filename, 'w+', encoding='utf-8')
    lyrics = lyrics.replace(' \n ', '\n')
    file.write(lyrics)
    file.close()

    print('>>> Done collecting lyrics.')


if __name__ == "__main__":
    artists = []
    print()
    print('#########################')
    print('## Welcome to DeepSong ##')
    print('#########################')
    print()
    print('>>> Please write the name of the first artist that you choose.')
    artist = input()
    while(True):
        artists.append(artist)
        print('>>> One more? [y/n]')
        artist = input()
        if artist == 'n':
            break
        print('>>> Please write the name of the artist')
        artist = input()

    print('>>> please write the name of the lyrics file you want (output file)')
    filename = input() + '.txt'

    print('>>> Start collecting lyrics...')
    get_all_lyrics(artists, filename)
    print('>>> Done collecting lyrics.')

    train.Trainer(filename)