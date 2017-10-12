from django.db import models

from enum import Enum, unique

from matching.models import MAX_QUESTION_LENGTH


# These question types are different from matching/models.py as we're interested in more specific options
# More are to follow?
@unique
class QuestionType(Enum):
    SLIDER = 'slider'
    GRADING = 'grading'

    def is_type(string):
        values = { item.value for item in QuestionType }
        return (string in values)


class QuestionBase(models.Model):
    '''
    A base model for all types of questions.
    
    ATTENTION! Trying to create an object of this model directly will raise an exception, as it's not intended to be used this way, create an object of one of the children instead!
    
    This is to hold all questions in one database, so that we can do more complicated things like rating, ordering or other.
    This model holds all common information for all types of questions, such as the question string.

    Additionally child models can be accessed though this one, by calling QuestionBase.childmodelname (note the small case),
    but it might raise a DoesNotExist exception. To avoid this we have a question_type, which should correspond to one of QuestionTypes.
    To see an example please refer to api/tests.py QuestionTestCase.test_models().

    This database isn't be abstract, as it will make querying and other related code more complicated.
    However, it would be more efficient that way as we wouldn't have a single huge table for all questions with additional tables for extra fields for each question type.

    Necessary fields:
        question (string) - the question
        question_type (string) - special field that should always correspond to the type of the related questiontype (a child of this model), and as such should not be written to directly
    '''

    # I feel like blank and null should not be true, but it's better for it to be the same as matching/models.py Question model
    question = models.CharField(max_length=MAX_QUESTION_LENGTH, blank=True, null=True)
    question_type = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'question'

    def save(self, *args, **kwargs):
        if QuestionType.is_type(self.question_type):
            return super(QuestionBase, self).save(*args, **kwargs)
        else:
            raise Exception('Trying to save a model <' + str(self) + '> of illegal type \'' + str(self.question_type) + '\'!')


class QuestionSlider(QuestionBase):
    '''
    A numerical question answered with a slider.

    Necessary fields:
        min_value (float) - the minimal value (left) for the slider
        max_value (float) - the maximal value (right) for the slider
    Optional fields:
        step (float) - the step of the slider
    '''
    min_value = models.FloatField()
    max_value = models.FloatField()
    step = models.FloatField(default=1.0, blank=True, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'slider question'

    def __init__(self, *args, **kwargs):
        if kwargs.get('question_type', None): kwargs.pop('question_type')
        self.question_type = QuestionType.SLIDER.value
        return super(QuestionSlider, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.question_type = QuestionType.SLIDER.value
        return super(QuestionSlider, self).save(*args, **kwargs)


class QuestionGrading(QuestionBase):
    '''
    Work in progress!

    
    '''

    class Meta:
        default_permissions = ()
        verbose_name = 'grading question'
