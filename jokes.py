# This is a joke generator class as per the christmas advent video
# https://youtu.be/7caCXRLmUJw

import random

class JokeFinished(Exception):
    pass

class JokeEngine():

    corpus = None

    def load_corpus(self, filename):
        with open(filename) as f:
            self.corpus = f.read()

    def _choose_char(self, target, target_length):
        options = []
        corp_length = len(self.corpus)
        
        index = 0
        try:
            while index < corp_length:
                index = self.corpus.index(target, index) + target_length
                if index < corp_length:
                    options.append(self.corpus[index])
                    
        except ValueError:
            pass
        
        if len(options) > 0:
            choice = random.choice(options)
        else:
            raise JokeFinished()
            
        if choice == "\n":
            raise JokeFinished()
        else:
            return choice

    def generate_joke(self, text, target_length=5, max_len=150):

        try:
            while max_len > 0:
                max_len -= 1
                
                x = text[-target_length:]
                next_char = self._choose_char(x, target_length)
                text += next_char
                
        except JokeFinished:
            pass

        return text