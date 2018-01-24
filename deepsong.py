import re, time
import urllib.request
from bs4 import BeautifulSoup
import train, get_lyrics, generator


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


# create a model from an existing corpus
def train_(corpus_file_name):
    train.Trainer(corpus_file_name + '.txt')


# generate songs from an existing model
def generate_(model_file_name):
    print('>>> Start generating lyrics? [y/n]')
    answer = input()
    gen = generator.Generator(model_file_name)
    while answer != 'exit':
        print('>>> To generate a lyrics, please define:')
        print('>>> a prime text for the lyrics')
        p_str = input()
        print('>>> the length of the lyrics you want')
        len = int(input())
        print('>>> temperature? [higher is more chaotic, the default is 0.8]')
        temp = float(input())
        gen.generate(prime_str=p_str, predict_len=len, temperature=temp, cuda=False)



"""
The DeepSong interface.
"""

if __name__ == "__main__":
    artists = []
    print()
    print()
    print('#########################')
    print('## Welcome to DeepSong ##')
    print('#########################')
    print()
    print()

    print('>>> To create a new artist type n,\n'
          '>>> To train a model on existing corpus [.txt file] type c, \n'
          '>>> To generate songs from an existing model, type g')

    action = input()

    if action == 'c':
        print('>>> Please write the corpus file name')
        name = input()
        train_(name)

    if action == 'g':
        print('>>> Please write the model file name')
        name = input()
        generate_(name)

    if action == 'n':
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