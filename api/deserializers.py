from django.shortcuts import get_object_or_404
from matching.models import StudentQuestionBase, StudentQuestionType, StudentAnswerSlider, StudentAnswerGrading, WorkField, StudentAnswerWorkField, Continent, SwedenRegion, \
StudentAnswerRegion, StudentAnswerContinent, JobType, StudentAnswerJobType


def answer_slider(answer, student, question, survey):
    '''
    Validate and deserialize an answer to a question of type SLIDER
    Returns true if the question was validated sucessfuly and saved
    '''
    question = question.studentquestionslider
    if type(answer) is dict:
        if 'min' in answer and 'max' in answer \
        and (type(answer['min']) is float or type(answer['min']) is int) \
        and (type(answer['max']) is float or type(answer['max']) is int) \
        and answer['min'] <= answer['max'] \
        and answer['min'] >= question.min_value \
        and answer['max'] <= question.max_value:
            (answer_model, was_created) = StudentAnswerSlider.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer_min = answer['min']
            answer_model.answer_max = answer['max']
            answer_model.save()
            return True
    elif (type(answer) is float or type(answer) is int):
        if question.min_value <= answer <= question.max_value:
            (answer_model, was_created) = StudentAnswerSlider.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer_min = answer
            answer_model.answer_max = answer
            answer_model.save()
            return True
    return False


def answer_grading(answer, student, question, survey):
    '''
    Validate and deseralize an answer to a question of type GRADING
    Returns true if the question was validated sucessfuly and saved
    '''
    if type(answer) is int:
        sizes = [-(question.studentquestiongrading.grading_size - 1) / 2,
                question.studentquestiongrading.grading_size / 2]
        if (sizes[0] < answer < sizes[1]):
            question = question.studentquestiongrading
            (answer_model, was_created) = StudentAnswerGrading.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer = answer
            answer_model.save()
            return True
    return False


ANSWER_DESERIALIZERS = {
    StudentQuestionType.SLIDER.value : answer_slider,
    StudentQuestionType.GRADING.value : answer_grading
}


def answers(answers, student, survey):
    '''
    Create or modify question answers from payload data
    used by questions_PUT in api/views
    Returns (int, int):
        where the first int tells the number of saved answers (all of which passed validation)
        and the second one is total number of processed anwers (some of which may have failed validation)
    '''
    modified_count = 0
    total_count = 0
    for answer in answers:
        total_count += 1
        if type(answer) is dict and 'id' in answer and 'answer' in answer:
            question = StudentQuestionBase.objects.filter(pk=answer['id']).first()
            if question and question.question_type in ANSWER_DESERIALIZERS:
                if ANSWER_DESERIALIZERS[question.question_type](answer['answer'], student, question, survey):
                    modified_count += 1
    return (modified_count, total_count)


def student_profile(data, profile):
    '''
    Deserialize the data into the student_profile, validating the data on the way
    '''
    if type(data) is dict:
        if 'nickname' in data and type(data['nickname']) is str:
            profile.nickname = data['nickname']
        else:
            return False

        # optional fields
        if 'facebook_profile' in data and type(data['facebook_profile']) is str:
            profile.facebook_profile = data['facebook_profile']
        if 'linkedin_profile' in data and type(data['linkedin_profile']) is str:
            profile.linkedin_profile = data['linkedin_profile']
        if 'phone_number' in data and type(data['phone_number']) is str:
            profile.phone_number = data['phone_number']
        profile.save()
        return True
    else:
        return False


def int_id_list(selection_model, answer_model, answers, student, survey, field_name):
    '''
    Creates or modifies answers from an list of valid ids.

    used by questions_PUT in api/views

    Parameters:
        selection_model - the class of the model of the "questions", or the selection for answers
        answer_model    - the class of the model of the answers
        answers         - list of answers
        student         - the student to which to correspond the answers
        survey          - the current survey, to which the answers and the questions should relate to
        field_name      - a string name of the field that tells the relation between the answer and the choice models
    '''
    if hasattr(selection_model, 'survey'):
        fields = selection_model.objects.filter(survey=survey).all()
    else:
        fields = selection_model.objects.all()
    argument_dict = {
        'student' : student,
        field_name : None
    }
    for field in fields:
        argument_dict[field_name] = field
        if field.id in answers:
            (answer_instance, was_created) = answer_model.objects.get_or_create(**argument_dict)
            if (was_created):
                answer_instance.survey.add(survey)
                answer_instance.save()
        else:
            answer_instance = answer_model.objects.filter(**argument_dict).first()
            if answer_instance:
                answer_instance.delete()
