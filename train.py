import torch
import torch.nn as nn
from torch.autograd import Variable
import argparse
from random import randint
import os
from itertools import islice
from tqdm import tqdm
import generate

from helpers import *
from model import *
from generate import *
import generator

"""
A class for training a model on a lyrics.
based on: https://github.com/spro/char-rnn.pytorch
"""

class Trainer:

    def __init__(self, filename):

        self.filename = filename
        self.print_every = 50
        self.cuda = False

        print('>>> Do you want to adjust the parameters of the neural network? [y/n]')
        print('>>> (if no, the default parameters will be used)')
        decision = input()

        # default parameters
        if decision == 'n':
            self.model = 'gru'
            self.n_epochs = 2000
            self.print_every = 50
            self.hidden_size = 100
            self.n_layers = 2
            self.learning_rate = 0.01
            self.chunk_len = 400
            self.batch_size = 100
            self.cuda = False

        if decision != 'n':
            print('choose model [gru/lstm]')
            model = input()
            print('choose number of epochs to train')
            n_epochs = int(input())
            print('choose hidden size')
            hidden_size = int(input())
            print('choose number of layers')
            n_layers = int(input())
            print('choose learning rate')
            learning_rate = float(input())
            print('choose chunk length')
            chunk_len = int(input())
            print('choose batch size')
            batch_size = int(input())
            print('cuda? [y/n]')
            if input() == 'y':
                self.cuda = True

            self.model = model
            self.n_epochs = n_epochs
            self.hidden_size = hidden_size
            self.n_layers = n_layers
            self.learning_rate = learning_rate
            self.chunk_len = chunk_len
            self.batch_size = batch_size

        self.h = open(self.filename, "r+", -1, encoding='utf8').read()
        self.h = self.h.split('\n')
        self.num_h = len(self.h)

        self.decoder = CharRNN(
            n_characters,
            self.hidden_size,
            n_characters,
            model=self.model,
            n_layers=self.n_layers,
        )
        self.decoder_optimizer = torch.optim.Adam(self.decoder.parameters(), lr=self.learning_rate)
        self.criterion = nn.CrossEntropyLoss()

        if self.cuda:
            self.decoder.cuda()

        self.start = time.time()
        self.loss_avg = 0

        # begin training
        self.train()


    """
    generates chunk of length of chunklen + 1 because the cut off in random_training_set
    """
    def generate_chunk(self):
        chunk = self.h[randint(1, self.num_h-1)]
        if len(chunk) < self.chunk_len + 1:
            while len(chunk) < self.chunk_len + 1:
                n = randint(1, self.num_h - 1)
                chunk = chunk + self.h[n]
        if len(chunk) > self.chunk_len + 1:
            chunk = chunk[:self.chunk_len + 1]
        return chunk

    def random_training_set(self, chunk_len, batch_size):
        inp = torch.LongTensor(batch_size, chunk_len)
        target = torch.LongTensor(batch_size, chunk_len)
        for bi in range(batch_size):
            chunk = self.generate_chunk()
            inp[bi] = char_tensor(chunk[:-1])
            target[bi] = char_tensor(chunk[1:self.chunk_len+1])
        inp = Variable(inp)
        target = Variable(target)
        if self.cuda:
            inp = inp.cuda()
            target = target.cuda()
        return inp, target

    def train_(self, inp, target):
        hidden = self.decoder.init_hidden(self.batch_size)
        if self.cuda:
            hidden = hidden.cuda()
        self.decoder.zero_grad()
        loss = 0

        for c in range(self.chunk_len):
            output, hidden = self.decoder(inp[:,c], hidden)
            loss += self.criterion(output.view(self.batch_size, -1), target[:,c])

        loss.backward()
        self.decoder_optimizer.step()

        return loss.data[0] / self.chunk_len

    def save(self):
        self.save_filename = os.path.splitext(os.path.basename(self.filename))[0] + '.pt'
        torch.save(self.decoder, self.save_filename)
        print('Saved as %s' % self.save_filename)

    def train(self):
        try:
            print("Training for %d epochs..." % self.n_epochs)
            for epoch in tqdm(range(1, self.n_epochs + 1)):
                loss = self.train_(*self.random_training_set(self.chunk_len, self.batch_size))
                self.loss_avg += loss

                if epoch % self.print_every == 0:
                    print('[%s (%d %d%%) %.4f]' % (time_since(self.start), epoch, epoch / self.n_epochs * 100, loss))

            print("Saving...")
            self.save()

        except KeyboardInterrupt:
            print("Saving before quit...")
            self.save()

        print('>>> Start generating lyrics? [y/n]')
        answer = input()
        if answer == 'y':
            print('>>> To exit, type exit')
            gen = generator.Generator(self.save_filename)
            while answer != 'exit':
                print('>>> To generate a lyrics, please define:')
                print('>>> a prime text for the lyrics')
                p_str = input()
                print('>>> the length of the lyrics you want')
                len = int(input())
                print('>>> temperature? [higher is more chaotic, the default is 0.8]')
                temp = float(input())
                gen.generate(prime_str=p_str, predict_len=len, temperature=temp, cuda=False)