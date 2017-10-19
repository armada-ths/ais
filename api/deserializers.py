from matching.models import StudentQuestionBase, StudentQuestionType, StudentAnswerSlider, StudentAnswerGrading, WorkField, StudentAnswerWorkField

def answer_slider(answer, student, question, survey):
    '''
    Validate and deserialize an answer to a question of type SLIDER
    '''
    if 'min' in answer and 'max' in answer \
    and type(answer['min']) is float and type(answer['max']) is float \
    and answer['min'] <= answer['max']:
        question = question.studentquestionslider
        (answer_model, was_created) = StudentAnswerSlider.objects.get_or_create(question=question, student=student)
        if was_created:
            answer_model.survey.add(survey)
        answer_model.answer_min = answer['min']
        answer_model.answer_max = answer['max']
        return True
    return False


def answer_grading(answer, student, question, survey):
    '''
    Validate and deseralize an answer to a question of type GRADING
    '''
    if type(answer) is int:
        sizes = [(question.studentquestiongrading.grading_size - 1) / 2,
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
    '''
    modified = False
    for answer in answers:
        if 'id' in answer and 'answer' in answer:
            question = StudentQuestionBase.objects.get(pk=answer['id'])
            if question.question_type in ANSWER_DESERIALIZERS:
                if ANSWER_DESERIALIZERS[question.question_type](answer['answer'], student, question, survey):
                    modified = True
    return modified


def fields(fields, student, survey):
    '''
    Create or modify field answers from payload data
    used by questions_PUT in api/views
    '''
    work_fields = WorkField.objects.filter(survey=survey).all()
    for work_field in work_fields:
        (field_model, was_created) = StudentAnswerWorkField.objects.get_or_create(student=student, work_field=work_field)
        if was_created:
            field_model.survey.add(survey)
        field_model.answer = work_field.pk in fields
        field_model.save()
