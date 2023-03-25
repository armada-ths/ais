from recruitment.models import *
from fair.models import *

remove_years = ["2020"]
for year in remove_years:
    recruitment_periods = RecruitmentPeriod.objects.filter(fair__year=year)
    for period in recruitment_periods:
        applications = RecruitmentApplication.objects.filter(recruitment_period=period)
        for application in applications:
            user = application.user
            application.delete()
            print(year, "    ", period, "    ", user)
            comments = RecruitmentApplicationComment.objects.filter(
                recruitment_application=application
            ).delete()
            answers = CustomFieldAnswer.objects.filter(user=user).delete()
