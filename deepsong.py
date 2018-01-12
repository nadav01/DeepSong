import re, time
import urllib.request
from bs4 import BeautifulSoup
import train

"""
The DeepSong interface.
"""

def get_lyrics(artists, filename):
    numartists = len(artists)
    allLir = ""
    counter = 1
    for artist in artists:
        artist = artist.lower()
        apagesurl = []
        for i in range(1,3): # number of pages of songs
            # scrapping lyrics from AZ Lyrics
            apagesurl.append("https://search.azlyrics.com/search.php?q=" + artist + "&w=songs&p=" + str(i))
        lir = allLyrics(apagesurl)

        # if the chosen artist not found
        if lir == '':
            print ('>>> unknown artist: ' + artist)
            quit()

        allLir += lir
        print(str((counter/numartists)* 100)  + '%')
        counter += 1

    # cleaning the data
    allLir = re.sub(r'\[[^]]*\]', '', allLir)
    allLir = re.sub('\n\n', '\n', allLir)
    allLir = bytes(allLir, 'utf-8').decode('utf-8', 'ignore') # removes non utf8 chars


    file = open(filename, 'w+', encoding='utf-8')
    file.write(allLir)
    file.close()

def allLyrics(urls):
    songsurl = []
    allLyrics = ""
    for u in urls:
        time.sleep(5) #wait for not being blocked
        content = urllib.request.urlopen(u).read()
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a'):
            l = str(link.get('href'))
            if "/lyrics/" in l:
                songsurl.append(l)

    for u in songsurl:
        allLyrics = allLyrics + get_song_lyrics(u) + "\n"

    return allLyrics


def get_song_lyrics(url):
    try:
        time.sleep(5) #wait for not being blocked
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').replace('<i>','').replace('</i>','').strip()
        lyrics = bytes(lyrics, 'utf-8').decode('utf-8', 'ignore')
        lyrics = lyrics.lower()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" + str(e)

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
    get_lyrics(artists, filename)
    print('>>> Done collecting lyrics.')

    train.Trainer(filename)