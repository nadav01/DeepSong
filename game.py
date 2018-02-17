import os, codecs, random, torch, argparse
from helpers import *
from model import *
from tei_creator import *
from create_person import *

class Generator:

    def __init__(self, filename):
        self.decoder = torch.load(filename)

    def generate(self, prime_str='A', predict_len=150, temperature=0.4, cuda=False):
        hidden = self.decoder.init_hidden(1)
        prime_input = Variable(char_tensor(prime_str).unsqueeze(0))

        if cuda:
            hidden = hidden.cuda()
            prime_input = prime_input.cuda()
        predicted = prime_str

        # Use priming string to "build up" hidden state
        for p in range(len(prime_str) - 1):
            _, hidden = self.decoder(prime_input[:,p], hidden)

        inp = prime_input[:,-1]

        for p in range(predict_len):
            output, hidden = self.decoder(inp, hidden)

            # Sample from the network as a multinomial distribution
            output_dist = output.data.view(-1).div(temperature).exp()
            top_i = torch.multinomial(output_dist, 1)[0]

            # Add predicted character to string and use as next input
            predicted_char = all_characters[top_i]
            predicted += predicted_char
            inp = Variable(char_tensor(predicted_char).unsqueeze(0))
            if cuda:
                inp = inp.cuda()

        return ''.join(predicted)

print('##### Welcome the the Artificial Singers Game! #####\n'
      'In order to start the game, all the models need to be\n'
      'placed in the models directory (a .pt file) including a .txt\n'
      'file with the same name in which all the singers the model\n'
      'composed of is written inside (each singer in a seperate line).\n'
      'You can create models using the DeepSong interface.\n'
      'To start the game, press Enter.')
start = input()
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
       'u', 'v', 'w', 'x', 'y', 'z']

# the keys are models filenames in the models dir and values are the .pt models
models = {}

for subdir, dirs, files in os.walk('models'):
    for file in files:
        if '.pt' in file: # consider only the .pt files
            filepath = subdir + os.sep + file
            # every model_name in the models dict holds a generator of its model
            models[file] = Generator(filepath)

# returns touple (question:string, right answer:int, the right answer model's name:string [for hint])
def gen_question():
    models_names = random.sample(models.keys(), 2)
    random.shuffle(models_names)
    ans = models_names[0]
    stanza = models[ans].generate(prime_str=random.sample(abc, 1))

    # genertaing random new lines
    splitted_stanza = stanza.split()
    first_newline = random.randint(1, int(len(splitted_stanza)/4))
    second_newline = random.randint(int(len(splitted_stanza)/4), int(len(splitted_stanza)/4)*2)
    third_newline = random.randint(int(len(splitted_stanza)/4)*2, int(len(splitted_stanza)/4)*3)
    stanza = ' '.join(splitted_stanza[:first_newline]) + '\n' + ' '.join(splitted_stanza[first_newline:second_newline]) + '\n' + ' '.join(splitted_stanza[second_newline:third_newline]) + '\n' + ' '.join(splitted_stanza[third_newline:])

    random.shuffle(models_names)
    q = 'To which model (singer) this stanza belongs?' + '\n' + stanza + '\n' + '1. ' + models_names[0].split('.')[0] + ' 2. ' + models_names[1].split('.')[0]
    ans_index = models_names.index(ans)
    model_name = models_names[ans_index]
    return q, ans_index+1, model_name


def get_hint(model_name):
    filename = 'models/' + model_name.split('.')[0]+'.txt'
    print('Some details about the model which has generated this stanza:')
    get_info(filename)

"""
The game
"""

print('Ok, lets start!\n'
      'For each generated stanza, you need to indentify the right singer which created it.\n'
      'For a hint, type h.\n'
      'To save the stanza as a xml TEI file, type s.')

while(True):
    question, answer, model_name = gen_question()
    print(question)
    stanza = question.split('?')[1].split('1.')[0]
    user_input = input()

    while user_input != '1' and user_input != '2':
        if user_input == 's':
            fname = 'models/' + model_name.split('.')[0]+'.txt'
            make_stanza_tei(stanza, fname, str(get_year(fname)))
            print('Please choose an answer')
            user_input = input()
        elif user_input == 'h':
            get_hint(model_name)
            print('Please choose an answer')
            user_input = input()
        elif user_input != '1' and user_input != '2':
            print('Invalid input. Please try again.')
            user_input = input()


    if user_input == '1' or user_input == '2':
        if int(user_input) == answer:
            print('You are right! nice :)')
        elif int(user_input) != answer:
            print('Wrong answer. The right answer is: ' + str(answer))

    print('\nNext question:')