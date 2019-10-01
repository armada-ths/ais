from django.shortcuts import get_object_or_404
from matching.models import StudentQuestionBase, StudentQuestionType, StudentAnswerSlider, StudentAnswerGrading, WorkField, StudentAnswerWorkField, Continent, SwedenRegion, \
StudentAnswerRegion, StudentAnswerContinent, JobType, StudentAnswerJobType
from exhibitors.models import Exhibitor, CatalogueIndustry, CatalogueValue, CatalogueEmployment, CatalogueLocation, CatalogueCompetence#CatalogueBenefit
from fair.models import current_fair

def matching(data):
    '''
    check the student answers data, validating the data on the way
    '''
    if type(data) is dict:
        industries = CatalogueIndustry.objects.values_list('pk', flat=True)
        values = CatalogueValue.objects.values_list('pk', flat=True)
        employments = CatalogueEmployment.objects.values_list('pk', flat=True)
        locations = CatalogueLocation.objects.values_list('pk', flat=True)
        competences = CatalogueCompetence.objects.values_list('pk', flat=True)


        validation_multi_set = {
            "industries" : industries,
            "values" : values,
            "employments" : employments,
            "locations" : locations,
            "competences": competences,
        }

        # Check that the values are lists and that
        # they are subsets of the possible values.
        # Also check that the weights, if given,
        # don't sum to zero.
        weight_sum = 0
        non_empties = len(validation_multi_set) + 1 # Count cities too
        for key, value_list in validation_multi_set.items():
            # check if list
            if isinstance(data[key]["answer"], (list,)):
                # can't be a subset if it's not an int
                if not set(data[key]["answer"]).issubset(set(value_list)):
                    return False

                if not "weight" in data[key]:
                    return False
                    
                    # The weight must be defined
                    return False

                if len(data[key]["answer"]) == 0:
                    non_empties -= 1    
                    # The weight will be forced to 0
                else:
                    weight_sum += data[key]["weight"] 

            else:
                return False

        # The cities value must be a string of comma-separated cities
        if not isinstance(data["cities"]["answer"], str):
            return False

        if not "weight" in data["cities"]:
            return False
        
        if data["cities"]["answer"] != "":
            # There is actually an answer for cities
            weight_sum += data["cities"]["weight"]
        else:
            # In this case, the weight will be forced to 0
            non_empties -= 1

        # Sum of weights must be non-zero for normalization to work
        if weight_sum == 0:
            return False

        # At least SOME answer must provide information
        if non_empties == 0:
            return False

        # The reponse_size variable must not be defined
        if "response_size" in data:
        # but it can't be 0 or negative
            if data["response_size"] <= 0:
                return False
            else:
                # It also can't be bigger than the number of exhibitors
                # in the current fair
                current_fair_id = current_fair()
                if current_fair_id is None: current_fair_id = 4 # Default to 2019
                max_response_size = Exhibitor.objects.filter(fair_id = current_fair_id).count()
                if data["response_size"] > max_response_size:
                    return False

        return True
    else:
        return False

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

def regions(regions, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views.
    '''
    for region_id in regions:
        region = get_object_or_404(SwedenRegion, region_id=region_id)
        StudentAnswerRegion.objects.get_or_create(student=student, region=region)


def continents(continents, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views.
    '''
    for continent_id in continents:
        continent = get_object_or_404(Continent, continent_id=continent_id)
        StudentAnswerContinent.objects.get_or_create(student=student, continent=continent)

def jobtype(jobtypes, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views. Uses the JobType defined in the Matching app.
    LATER: Change it to use the JobType model in the exhibitors app.
    '''
    for job_type_id in jobtypes:
        job_type = get_object_or_404(JobType, job_type_id=job_type_id)
        StudentAnswerJobType.objects.get_or_create(student=student, job_type=job_type)
