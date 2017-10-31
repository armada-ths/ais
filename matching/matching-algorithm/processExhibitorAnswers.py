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

import nltk
import enchant
import gensim

class SpellChecker():

    def __init__(self, dict_name='en_US', max_dist=3):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        suggestion = self.spell_dict.suggest(word)

def genWorldRegions(responses, survey_raw, survey_processed):
    pass

def genWorkFields(responses, survey_raw, survey_processed):
    '''
    Objects must be a list of matching.Response model objects
    '''
    pass
