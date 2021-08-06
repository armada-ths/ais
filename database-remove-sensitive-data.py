# To remove sensitive data from the AIS for developer purpose run each of these three scripts in the Django Python shell
# Sara Gustafsson, 2019

from recruitment.models import *
from fair.models import *
remove_years = ['2016','2017','2018', '2019', '2020', '2021']
for year in remove_years:
    recruitment_periods = RecruitmentPeriod.objects.filter(fair__year = year)
    for period in recruitment_periods:
        applications = RecruitmentApplication.objects.filter(recruitment_period = period)
        for application in applications:
            user = application.user
            application.delete()
            print(year, "    ", period, "    ", user)
            comments = RecruitmentApplicationComment.objects.filter(recruitment_application=application).delete()
            answers = CustomFieldAnswer.objects.filter(user=user).delete()

###############################################################################

from recruitment.models import *
from fair.models import *
year = '2021'
remove_periods = ['Operations Team', 'Developer', 'Project Manager', 'Project Group']
for period in remove_periods:
    print(period)
    recruitment_period = RecruitmentPeriod.objects.filter(fair__year = year, name = period)
    applications = RecruitmentApplication.objects.filter(recruitment_period = recruitment_period)
    for application in applications:
        user = application.user
        application.delete()
        print(user)
        comments = RecruitmentApplicationComment.objects.filter(recruitment_application=application).delete()
        answers = CustomFieldAnswer.objects.filter(user=user).delete()

###############################################################################

from recruitment.models import *
recruitment_period = RecruitmentPeriod.objects.filter(fair__year='2019', name='Host')
applications = RecruitmentApplication.objects.filter(recruitment_period = recruitment_period)
users = []
for application in applications:
    users.append(application.user)
print('Number of users in recruitment period: ', len(users))
all_answers = CustomFieldAnswer.objects.all()
for answer in all_answers:
    if answer.user not in users:
        answer.delete()
        print('Deleted answer')
    else:
        print('Did not delete: ', answer.user)