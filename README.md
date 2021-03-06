<p align="center"> 
<img src="https://i.imgur.com/wSIr6IY.png">
</p>
DeepSong is a final project in the course Digital Humanities 181 at Ben Gurion University. DeepSong is a project which aims to raise the general public's awareness of the progress in the capacity of artificial intelligence. This is acheived by creating a "song writer" which is a neural network model which has been trained on the poets / lyrics chosen by you. The DeepSong interface allows you to select several singers (or bands). It then collects the respective lyrics and trains a neural network on the corpus. The result is a new 'singer' which is a combination of all the singers/bands you chose.<br/>
After that you can start generating songs lyrics from that new 'artist' you have created or play the 'Artificial Singers Game'.<br/>
Have fun :)

<br/>

## Dependencies:
* [Python 3.6](https://www.python.org/downloads/)
* Install PyTorch: <br/>
first install [Anaconda](https://www.anaconda.com/download/). <br/>
Then, if you under Windows: <br/>
```
conda install -c peterjc123 pytorch
```

If you are under Linux / MacOS: see instructions on [pytorch.org](https://www.pytorch.org)<br/>
* Install BeautifulSoup 4: <br/>
```
pip install beautifulsoup4
```
* Install tqdm: <br/>
```
conda install -c conda-forge tqdm
```
OR
```
pip install tqdm
```
<br/>

## Running DeepSong:
After installing all the dependencies, simply download and extract the project's files and: <br/>
```
python deepsong.py
```
you should get <br/>
```
#########################
## Welcome to DeepSong ##
#########################


>>> To create a new artist type n,
>>> To train a model on existing corpus [.txt file] type c,
>>> To generate songs from an existing model, type g
```

## Running the 'Artificial Singers Game':
After installing all the dependencies, simply download and extract the project's files. <br/>
You need to place at least 2 trained models (created in the DeepSong interface) in the 'models' directory. For each model model_name.pt you need to create model_name.txt which contains the artists you chose for the model in the DeepSong interface (each artist in a seperate line). This text file is for the Sparql quries (when a user ask for a hint in the game, it collects information about the artists and combinds them into a new imaginary character). <br/>
Then: <br/>
```
python game.py
```
you should get, for example <br/>
```
##### Welcome the the Artificial Singers Game! #####
In order to start the game, all the models need to be
placed in the models directory (a .pt file) including a .txt
file with the same name in which all the singers the model
composed of is written inside (each singer in a seperate line).
You can create models using the DeepSong interface.
To start the game, press Enter.

Ok, lets start!
For each generated stanza, you need to indentify the right singer which created it.
For a hint, type h.
To save the stanza as a xml TEI file, type s.
To which model (singer) this stanza belongs?
she thought i don't know
i see me from the dirty street of my mind
know the light
i know i feel like the way i don't like you
1. 60s 2. 90s
h
Some details about the model which has generated this stanza:
One of the artist's favorite genres is Blues_rock
This band member's or singer's hometown is Oxfordshire
Please choose an answer
2
You are right! nice :)
```

For any question: nadavloebl@gmail.com
