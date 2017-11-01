'''
Preprocessing requires:
    nltk
    enchant
    gensim

Dependencies for gensim:
    pip install numpy
    pip install scipy
Then do:
    pip install --upgrade gensim

'''
from django.contrib.auth.models import User
from fair.models import Fair
from exhibitors.models import Exhibitor
from matching.models import Survey, Response, TextAns

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer as ps
from gensim import corpora, models, similarities
import enchant

class SpellChecker():

    def __init__(self, dict_name='en_US', max_dist=3):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        return(self.spell_dict.suggest(word))

    def check(self, word):
        return(self.spell_dict.check(word))

def genWorldRegions(responses, survey_raw, survey_processed):
    '''
    TODO when the db is set up correctly
    '''
    pass

def genSweRegions(responses, survey_raw, survey_processed):
    '''
    TODO when the db is
    '''
    pass

def genWorkFields(responses, survey_raw, survey_processed):
    '''
    Objects must be a list of matching.Response model objects
    '''
    stop_words = set(stopwords.words('english') + [',', '.', '(', ')'])
    answers_raw_all = TextAns.objects.filter(response__in=responses)
    sc = SpellChecker()
    for ans_raw in answers_raw_all:
        answer_raw = word_tokenize(ans_raw.ans)
        answer_filtered = [w for w in answer_raw if not w in stop_words]
        for ans in answer_filtered:
            if sc.check(ans) == False:
                print(ans)
                print(sc.replace(ans))
                print('===============')

    #for ans in answer_filtered:
    #    print(ans)
