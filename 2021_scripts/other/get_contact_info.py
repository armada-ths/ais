from fair.models import Fair
from recruitment.models import RecruitmentApplication

fair = Fair.objects.filter(current=True)
applications = RecruitmentApplication.objects.filter(
    status="accepted", recruitment_period__fair=fair
)
out = "Name\tRole"

person_idx = 50

# print(applications[person_idx].user.email)
# print(applications[person_idx].user.email_user)
# print(applications[person_idx].user.email_user)
# print(applications[person_idx].user.teaminvitation_set)
# print(applications[person_idx].delegated_role)
# print(str(applications[person_idx].recruitment_period)[7:])

# for attr in dir(applications[0].user):
#     print(attr)


def takeFirst(elem):
    return elem[0]


def takeSecond(elem):
    return elem[1]


def takeThird(elem):
    return elem[2]


def takeForth(elem):
    return elem[2]


contacts = []

for application in applications:
    member_role = application.delegated_role.name
    member_group = application.delegated_role.organization_group
    member_type = application.recruitment_period.name
    first_name = application.user.first_name
    last_name = application.user.last_name
    email = application.user.email
    contacts.append([email, member_type, member_role, member_group])

contacts_without_PM = contacts[1:]
contacts_without_PM.sort(key=takeForth)
contacts_without_PM.sort(key=takeThird)
contacts_without_PM.sort(key=takeFirst)

contacts_without_PM = [contacts[0]] + contacts_without_PM
for contact in contacts_without_PM:
    print(f"{contact[0]},{contact[1]},{contact[2]}")

# for application in applications:
# 	out += '\n'
# 	out += application.user.first_name + " " + application.user.last_name
# 	out += '\t'
# 	out += application.delegated_role.name
# print(out)

# fh = open('contact_info.txt', 'w')
# fh.write(out)
# fh.close()
