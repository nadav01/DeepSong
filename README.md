<p align="center"> 
<img src="https://i.imgur.com/wSIr6IY.png">
</p>
DeepSong is a little project which aims to raise the awareness of the progress in the capacity of artificial intelligence to the general public. The DeepSong interface let you choose couple of singers (or bands). It collects all the singers' lyrics from all times. Then, it traines a neural network on the corpus. The result is a new 'singer' which is a combination of all the singers/bands you chose.<br/>
After that you can start generating songs lyrics from that new artist you have created and play the 'Artificial Singers Game'.<br/>
Have fun :)

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

## Running:
After installing all the dependencies, simply download and extract the project's files and: <br/>
```
python deepsong.py
```

## Running the 'Artificial Singers Game':
After installing all the dependencies, simply download and extract the project's files. <br/.>
Within the same folder, create a new directory named 'models'. In this directory you need to place <br/>
at least 4 trained models (created in the DeepSong interface). For each model  model_name.pt you need to create <br/>
model_name.txt which contains the artists you chose for the model in the DeepSong interface (each artist in a seperate line). <br/>
This text file is for the Sparql quries (when a user ask for a hint in the game, it collects information about the artists and <br/>
combinds them into a new imaginary character. <br/>
Then: <br/>
```
python game.py
```
