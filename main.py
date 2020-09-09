# Aira Sofia Cosino
#
# final project
#
# Project milestone
#

import math

def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list
    containing the words in txt after it has been 'cleaned'
    """
    txt = txt.lower().replace(',', '').replace('.', '').replace('?', '').replace('!', '').replace(';', '').replace('-', '')
    return txt

def stems(s):
    """ accepts a string as a parameter; returns the stem of s
    """
    prefixes = ['anti', 'de', 'bi', 'dis', 'en', 'em', 'fore', 'in', 'im', 'inter', 'me', 'mis', 'non', 'pre', 'semi', 'super', 'un', ' trans', 'under', 'fore']
    suffixes = ['ing', 'ed', 'er', 'es', 'y', 'less', 'al', 'or', 'ore', 'on', 'ism', 'ist', 'ity', 'ty', 'ent', 'ment', 'ship', 'ness', 'tion', 'sion', 'ies']

    if len(s) > 2:
        for p in prefixes:
            if s[:len(p)] == p and len(s) > len(p):
                if len(s) - len(p) > 1:
                    s = s[len(p):]
                break
        for suff in suffixes:
            if s[-len(suff):] == suff and len(s) > len(suff):
                if len(s) - len(suff) > 1:
                    s = s[:-len(suff)]
                    if s[-1] == s[-2] and len(s) > 1:
                        s = s[:-1]
                break
    return s

def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries, d1 and d2, as inputs and computes
    and returns their log similarity score
    """
    score = 0
    total = sum([d1[i] for i in d1])
    for item in d2:
        if item in d1:
            score += math.log(d1[item] / total) * d1[item]
        else:
            score += math.log(0.5 / total) * d2[item]
    return score 

class TextModel:
    """ serves as a blueprint for objects that model a body of text
    """

    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string
        model_name as a parameter and initializing the attributes
        name, words, and word_lengths
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}

    def __repr__(self):
        """ returns a string that includes the name of the model as
        well as the sizes of the dictionaries for each feature of
        the text
        """
        s = ''
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths))
        return s

    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        
        word_list = clean_text(s).split()
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        for w in word_list:
            len_words = len(w)
            if len_words not in self.word_lengths:
                self.word_lengths[len_words] = 1
            else:
                self.word_lengths[len_words] += 1

        for w in word_list:
            t = stems(w)
            if t not in self.stems:
                self.stems[t] = 1
            else:
                self.stems[t] += 1

        word_list = s.split()
        r = 1
        for w in word_list:
            if '.' in w or '?' in w or '!' in w:
                if r in self.sentence_lengths:
                    self.sentence_lengths[r] += 1
                else:
                    self.sentence_lengths[r] = 1
            else:
                r += 1

    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring
        the similarity of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_len_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        stem_len_score = compare_dictionaries(other.stems, self.stems)
        sentence_len_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        return [word_score, word_len_score, stem_score, stem_len_score, sentence_len_score]

    def classify(self, source1, source2):
        """ compares the called TextModel object(self) to two other 'source'
        TextModel objects and determines which of these other TextModels is
        the more likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('Scores for', source1.name, scores1)
        print('Scores for', source2.name, scores2)
        sum_scores1 = sum(scores1)
        sum_scores2 = sum(scores2)
        if sum_scores1 > sum_scores2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)

    def add_file(self, filename):
        """ adds all of the text in the file identified by
        filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        add_txt = f.read()
        f.close()
        self.add_string(add_txt)

    def save_model(self):
        """ saves the TextModel object self by writing its
        various feauture dictionaties to files
        """
        filename = self.name + '_' + 'words'
        save_word = self.words
        f = open(filename, 'w')
        f.write(str(save_word))
        f.close()

        filename = self.name + '_' + 'word_lengths'
        save_word = self.word_lengths
        f = open(filename, 'w')
        f.write(str(save_word))
        f.close()

        filename = self.name + '_' + 'stems'
        save_word = self.stems
        f = open(filename, 'w')
        f.write(str(save_word))
        f.close()

        filename = self.name + '_' + 'sentence_lengths'
        save_word = self.sentence_lengths
        f = open(filename, 'w')
        f.write(str(save_word))
        f.close()

    def read_model(self):
        """ reads the stored dictionaries for the called
        TextModel object from their files and assigns
        them to the attributes of the called TextModel
        """
        filename = self.name + '_' + 'words'
        f = open(filename, 'r')
        read_str = f.read()
        f.close()
        self.words = dict(eval(read_str))

        filename = self.name + '_' + 'word_lengths'
        f = open(filename, 'r')
        read_str = f.read()
        f.close()
        self.word_lengths = dict(eval(read_str))

        filename = self.name + '_' + 'stems'
        f = open(filename, 'r')
        read_str = f.read()
        f.close()
        self.stems = dict(eval(read_str))

        filename = self.name + '_' + 'sentence_lengths'
        f = open(filename, 'r')
        read_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(read_str))

def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
