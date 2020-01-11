## Final Project
## Sam DeCosta

import math

def clean_text(txt):
    """ takes input string txt and returns a list containing the words in
        txt after it has been 'cleaned' (punctuation removed)
    """
    cleaned_text = txt
    for x in [',','.','?','!',';','e.g.',':','-']:
        cleaned_text = cleaned_text.replace(x,'')
    cleaned_text = cleaned_text.lower()
    listclean = cleaned_text.split()
    return listclean

def stem(s):
    """ takes input string s (a word) and returns the stem version of the word
    """
    word = s
    if len(word) > 3:
        if word[-2:] == 'es' and word[-3] == word[-4]:
            word = word[:-3]
        elif word[-2:] == 'es':
            word = word[:-2]
        if len(word) > 5:
            if word[-2:] == 'en' and word[-3] == word[-4]:
                word = word[:-3]
            elif word[-2] == 'en':
                word = word[:-2]
        if word[-1]  == 's':
            word = word[:-1]
        if len(word) > 5:
            if word[-3:] == 'ing':
                word = word[:-3]
                if word[-2] == word[-1]:
                    word = word[:-1]
        if word[-3:] == 'est' and len(word) > 5:
            word = word[:-3]
        elif word[-2:] == 'er':
            word = word[:-2]
        elif word[-2:] == 'ed' and len(word) > 4:
            word = word[:-2]
        elif word[-1] == 'y':
            word = word[:-1]
            word += 'i'
    return word

def compare_dictionaries(d1,d2):
    """ takes 2 feature dictionaries d1 and d2 and computes and returns their
        log similarity score
    """
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    for x in d2:
        if x in d1:
            score += d2[x] * math.log(d1[x]/total)
        else:
            score += d2[x] * math.log(0.5 / total)
    return score

class TextModel():
    """ blueprint for objects that model a body of text """

    def __init__(self, model_name):
        """ constructs a new TextModel that accepts string model_name and
            creates name, words, stems, sentance_lengths, dialogue starters,
            and word_lengths attributes
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.dialogue_starters = {}

    def __repr__(self):
        """ returns a string that includes the name of the model as well as
            the sizes of the dictionaries for each feature of text
        """
        text = ''
        text += 'text model name: ' + self.name + '\n '
        text += ' number of words: ' + str(len(self.words)) + '\n '
        text += ' number of word lengths: ' + str(len(self.word_lengths)) +  '\n '
        text += ' number of stems: ' + str(len(self.stems)) + '\n '
        text += ' number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n '
        text += ' number of dialogue starters: ' + str(len(self.dialogue_starters)) + '\n '
        return text

    def add_string(self,s):
        """ takes input string s and adds its pieces to all of the dictionaries
            of TextModel
        """
        sentences = s.split()
        count = 1
        enders = ['?','.','!']
        for x in sentences:
            for punctuation in enders:
                if punctuation in x:
                    if count not in self.sentence_lengths:
                        self.sentence_lengths[count] = 1
                    elif count > 1:
                        self.sentence_lengths[count] += 1
                    count = 0
            else:
                count += 1
        
        word_list = clean_text(s)

        checker = 0
        for i in range(len(s)):
            if s[i] =='"' and checker % 2 == 0 and i > 0:
                if s[i] not in self.dialogue_starters:
                    self.dialogue_starters[i] = 1
                else:
                    self.dialogue_starters[i] +=1
            

        for w in word_list:
            current_stem = stem(w)
            if current_stem not in self.stems:
                self.stems[current_stem] = 1
            else:
                self.stems[current_stem] += 1
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[(len(w))] = 1
            else:
                self.word_lengths[(len(w))] += 1

    def add_file(self,filename):
        """ takes input string filename, which identifies a file and adds all of
            the text in the file to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        self.add_string(f.read())

    def save_model(self):
        """ takes the TextModel and writes its dictionaries to files, with
            one file for each dictionary
        """
        f = open(self.name + '_words', 'w')
        f.write(str(self.words))
        f.close()
        f = open(self.name + '_word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close()
        f = open(self.name + '_stems', 'w')
        f.write(str(self.stems))
        f.close()
        f = open(self.name + '_sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        f = open(self.name + '_dialogue_starters', 'w')
        f.write(str(self.dialogue_starters))
        f.close()

    def read_model(self):
        """ reads stored dictionaries for the called TextModel object from
            their files and assigns them to the attributes of the TextModel
        """
        f =  open(self.name + '_words', 'r')
        d_str = f.read()
        f.close()
        self.words = dict(eval(d_str))
        f =  open(self.name + '_word_lengths', 'r')
        d_str = f.read()
        f.close()
        self.word_lengths = dict(eval(d_str))
        f =  open(self.name + '_stems', 'r')
        d_str = f.read()
        f.close()
        self.stems = dict(eval(d_str))
        f =  open(self.name + '_sentence_lengths', 'r')
        d_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(d_str))
        f =  open(self.name + '_dialogue_starters', 'r')
        d_str = f.read()
        f.close()
        self.dialogue_starters = dict(eval(d_str))

    def similarity_scores(self,other):
        """ computes and returns a list of log similarity scores measuring the
            similarity of self and other, one score for each type of feature
        """
        listscores = []
        
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        dialogue_score = compare_dictionaries(other.dialogue_starters, self.dialogue_starters)

        for x in [word_score, word_length_score, stem_score, sentence_score, dialogue_score]:
            listscores += [x]
        return listscores

    def classify(self, source1, source2):
        """ compares the called textModel object with two other source textmodel objets and
            determines which of these other textmodels is the more likely source of the called
            textModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        weighted_sum1 = 3 * scores1[0] + 2 * scores1[1] + scores1[2] + 3 * scores1[3] + scores1[4]
        weighted_sum2 = 3 * scores2[0] + 2 * scores2[1] + scores2[2] + 3 * scores2[3] + scores2[4]

        print('Scores for ' + source1.name + ':' + str(scores1))
        print('Scores for ' + source2.name + ':' + str(scores2))

        print(weighted_sum1)
        print(weighted_sum2)

        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        elif weighted_sum2 > weighted_sum1:
            print(self.name + ' is more likely to have come from ' + source2.name)
        else:
            print(self.name + ' is equally likely to have come from ' + source2.name + ' or ' + source1.name)

def run_tests():
    """ testing function comparing text to shakespeare and thoreau """
    source1 = TextModel('shakespeare')
    source1.add_file('shakespeare.txt')

    source2 = TextModel('thoreau')
    source2.add_file('walden.txt')

    source3 = TextModel('hawthorne')
    source3.add_file('hawthorne.txt')


    new1 = TextModel('walden_test')
    new1.add_file('waldentest.txt')
    new1.classify(source1, source2)

    new2 = TextModel('shakespeare_test')
    new2.add_file('mystery.txt')
    new2.classify(source1,source2)

    new4 = TextModel('emerson_test')
    new4.add_file('selfreliance.txt')
    new4.classify(source3,source2)

    
    

    
