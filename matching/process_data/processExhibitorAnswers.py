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
#from gensim import corpora, models, similarities
import enchant
import re
from collections import Counter

class SpellChecker():

    def __init__(self, dict_name='en_US', max_dist=3):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        return(self.spell_dict.suggest(word))

    def check(self, word):
        return(self.spell_dict.check(word))

def genSubRegions(responses, survey_raw, survey_processed):
    '''
    not done, just returns a list of texts without any relation to exhibitors
    '''
    answers_raw_all = TextAns.objects.filter(response__in=responses)
    words = check_spelling(answers_raw_all)
    return(words)

def genWorkFields(responses, survey_raw, survey_processed, countFlag=False):
    '''
    Objects must be a list of matching.Response model objects
    not done, just returns a list of texts without any relation to exhibitors
    '''
    answers_raw_all = TextAns.objects.filter(response__in=responses)
    words = check_spelling(answers_raw_all, countFlag, True)
    return(words)

    #for ans in answer_filtered:
    #    print(ans)

def check_spelling(answers, countFlag=False, lowerFlag=False):
    '''
    be cool
    '''
    stop_words = set(stopwords.words('english') + ['',',', '.', '(', ')'])
    sc = SpellChecker()
    correctly_spelled = []
    incorrectly_spelled = []
    for ans_raw in answers:
        answers_raw = re.split(',|;', ans_raw.ans)
        #answers_raw = word_tokenize(ans_raw.ans)
        answers_filtered = [w for w in answers_raw if not w in stop_words]
        for ans in answers_filtered:
            ans = ans.strip(' ')
            if lowerFlag:
                ans = ans.lower()
            if ans:
                if sc.check(ans) == True:
                    correctly_spelled.append(ans)
                else:
                    splitted_ans = ans.split()
                    check_flag = True
                    for s_ans in splitted_ans:
                        if sc.check(s_ans) == False:
                            check_flag = False
                            incorrectly_spelled.append(ans)
                            break
                    if check_flag:
                        correctly_spelled.append(ans)
    if countFlag:
        most_common = Counter(correctly_spelled).most_common(20)
        most_common_incorrect = Counter(incorrectly_spelled).most_common(10)
        return(most_common, most_common_incorrect)

    return (set(correctly_spelled), set(incorrectly_spelled))
