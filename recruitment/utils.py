from __future__ import unicode_literals

import datetime
import os.path
from django.utils import timezone
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User, Group
from fair.models import Fair
from companies.models import Company
from people.models import Programme
from .models import Role, RecruitmentPeriod, RecruitmentApplication

def get_or_create_role(name, description=None, parent_role=None):
    group = Group.objects.get_or_create(name=name)[0]
    role = Role.objects.get_or_create(name=name)[0]
    role.description = description
    role.parent_role = parent_role
    role.group = group
    role.save()
    return role

def assign_groups_to_all_users():
    for user in User.objects.all():
        recruitment_application = user.recruitmentapplication_set.filter(status='accepted').exclude(delegated_role=None).first()
        if recruitment_application:
            recruitment_application.delegated_role.add_user_to_groups(user)


def create_user_and_stuff(username, first_name, last_name, email, role_name, parent_role_name, recruitment_period_name, fair_name):
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

    fair = Fair.objects.get_or_create(
            year=2016,
            name=fair_name
    )[0]

    if parent_role_name:
        parent_role = get_or_create_role(parent_role_name, '')

    recruitment_period = RecruitmentPeriod.objects.filter(fair=fair, name=recruitment_period_name).first()
    if not recruitment_period:
        recruitment_period = RecruitmentPeriod.objects.create(
            fair=fair,
            name=recruitment_period_name,
            start_date = datetime.datetime(2016, 1, 1),
            end_date = datetime.datetime(2016, 1, 1),
            interview_end_date = datetime.datetime(2016, 1, 1)
        )

    role = get_or_create_role(name=role_name, description='', parent_role=parent_role)
    recruitment_period.recruitable_roles.add(role)

    recruitment_application = RecruitmentApplication.objects.filter(user=user, recruitment_period=recruitment_period).first()
    if not recruitment_application:
        recruitment_application = RecruitmentApplication.objects.create(
            delegated_role=role,
            status='accepted',
            user=user,
            recruitment_period=recruitment_period
        )[0]

    if recruitment_application.status == 'accepted':
        role.add_user_to_groups(user)

def create_recruitment_period_from_csv(file_path, recruitment_period_name, year):
    fair_name = 'Armada ' + str(year)
    with open(file_path, encoding='utf-8') as f:
        for line in f:
                if line.strip():
                    values = line.split(',')
                    username = values[0].strip()
                    first_name = values[1].strip()
                    last_name = values[2].strip()
                    email = values[3].strip()
                    role_name = values[4].strip()
                    create_user_and_stuff(username, first_name, last_name, email, role_name, recruitment_period_name, recruitment_period_name + ' ' + str(year), fair_name)


def create_programmes():
    programmes = ["Business IT Engineering (B.Sc)", "Civil Engineering and Urban Management (M.Sc)",
     "Constructional Engineering (B.Sc)", "Design and Product Realisation (M.Sc)",
     "Electrical Engineering (B.Sc, M.Sc)", "Energy & Environment (M.Sc)",
     "Industrial Engineering and Management (M.Sc)", "Information and Communication Technology (B.Sc, M.Sc)",
     "Materials Design and Engineering (M.Sc)", "Media Technology (M.Sc)", "Computer Engineering (B.Sc)",
     "Computer Engineering and Electronics (B.Sc)", "Engineering Physics (M.Sc)", "Mechanical Engineering (B.Sc, M.Sc)",
     "Vehicle Engineering (M.Sc)", "Chemistry and Chemical Engineering (M.Sc)",
     "Computer Science and Engineering (M.Sc)", "Electrical Engineering and Economics (B.Sc)",
     "Engineering and of Education (M.Sc)", "Medical Engineering (M.Sc)", "Microelectronics (M.Sc)",
     "Architecture Programme", "Biotechnology (M.Sc)", "Chemical Engineering (B.Sc)", "Medical Technology (B.Sc)",
     "Property Development & Real Estate (B.Sc)", "Real Estate and Finance (B.Sc)"]

    for programme in programmes:
        if not Programme.objects.filter(name=programme).first():
            Programme.objects.create(name=programme)


import os

def create_armada_year(year):
    directory = os.path.dirname(os.path.abspath(__file__)) + '/Armada' + str(year)
    create_recruitment_period_from_csv(directory+'/pct.csv', 'Project Core Team', year)
    create_recruitment_period_from_csv(directory+'/ept.csv', 'Extended Project Team', year)

def create_armada_hosts():
    hosts_areas = [{"title":"Business relations and events","roles":[{"name":"Event Host","openPositions":12,"description":"THS Armada is more than just a career fair. It also includes events such as the 5 km Armada run, various case solving-challenges and theme lectures. As an Event Host you are a part of the team that makes sure every event is valuable for both students and the participating companies. You prefer to work in a team and you are positive and outgoing. Most of the events will take place before the fair, starting in late October."},{"name":"Lounge Host","openPositions":12,"description":"During the fair, there are two lounges, one in Nymble and one in KTHB available for the exhibitors and all members of the project. As a Lounge Host you are a part of the team that is responsible for the lounge interior and serving of food and beverages. You have a welcoming and service oriented attitude with good social skills. The position involves intensive work during a few days and it is important that you can handle stress and have a positive attitude. There will be early mornings, so it is a plus if you are a morning person."},{"name":"Service Host","openPositions":"12-16","description":"As a Service Host, you are responsible to provide the fair visitors the best service possible. The role includes both work at the information desk, the student lounge and the wardrobes. It’s important that you are service minded, positive and have good communication skills. You prefer to work in a team, are outgoing and have good social skills."},{"name":"Banquet Host","openPositions":8,"altDescription":"THS Banquet and the Club Armada that is taking place after the main dinner seating. The banquet team is responsible for the entire event, including both planning, shaping and running the operative duties before, during and after the banquet at the Ericsson Globe arenas facilities.","description":"Do you want to participate in one of KTH:s biggest event of the year than banquet host is something for you. With over 700 guests and 160 companies THS Armada present the largest university banquet held in Sweden. As a banquet host you will help the banquet team group leaders with the operative management during the banquet evening, this year at Annexet (Globe Arenas). We are therefore searching for an outgoing, driven and communicative person with an interest in events. Managing this kind of big events there are going to pop up unexpected problems so it´s also a plus if you are comfortable in taking own initiatives."},{"name":"Banquet host: Entertainment","openPositions":2,"description":"As a banquet host, where entertainment is the main focus, you will assist the team leader of entertainment. Most important is that the evening schedule is followed and that the entertainment sections are well organized. You will also have direct contact with the banquet compere and possible artists and therefore assist them. During the evening it can be quite stressful so we are searching for an outgoing, structured and communicative person who can handle stressful situations and of course are interested in event and entertainment."}]},{"title":"Logistics and fair","roles":[{"name":"Career Fair Host","openPositions":175,"description":"As a Career Fair Host, you are the exhibiting organisation’s contact person and ultimately the face of THS Armada to them. Before and during the fair you are responsible for the contact with the exhibitor and make sure they get the best service possible. Therefore it is important that you are service-oriented and have a professional attitude. The work of a Career fair host also includes preparing the fair halls in Nymble, KTHB and KTH Entré the weekend before the fair, as well as restore the halls afterwards. You have great social skills and prefer to work in a team."},{"name":"Task Force","openPositions":"10+10","description":"The Task force is the part of THS Armada that work with the logistics and technology before, during and after the fair. The team work together but are divided into two groups with different responsibilities. One part is responsible for the logistics, which includes taking care of the exhibitors goods. The other part is responsible for the technology which among other things includes supplying the exhibitors with electricity. As a part of the Task force you also work to resolve unforeseen problems that arise during the fair. As the role involves a lot of intensive work over a few days it is important that you are positive and want to create a good atmosphere within the team. You have good problem solving skills and are comfortable making your own decisions."},{"name":"University Relations Host","openPositions":"10","description":"Every year, representatives from other universities in Sweden are invited to THS Armada. As a University Relations Host you are a part of the team that welcomes these representatives. The team works together but you are responsible for one university by guiding them through the day and is available for answering any questions they might have. Together with the other host we are also going to held a party for the visiting universities. The work includes preparing and decorating the venue as well as make sure the representatives have the best evening possible. Other desirable qualities is that you prefer to work in a team and have good communication skills as the role includes contact with many different persons."}]},{"title":"Media and Communication","roles":[{"name":"Photographer","openPositions":5,"description":"As a Photographer, you are part of the team that documents everything that happens before and during THS Armada. This includes photographing the different events, the fair and the banquet. In the beginning of October you will also take individual portraits of all the members of the project. As a person you are creative, positive and outgoing. Previous experience of photography and work samples are a plus."},{"name":"Cameraman","openPositions":1,"description":"As the cameraman during the Armada Fair you are responsible for recording the live streamed material used in our Web-TV broadcast. We expect you to be aproblem solver and a team player, but also be able to work independently. Previous experience in video recording is meritorious, especially live-streaming."},{"name":"Audio Technician","openPositions":1,"description":"As the audio technician during the Armada Fair you are responsible for the audio during the live stream recordings. We expect you to have knowledge of audio recording and we want you to be a real team player. It is important that you are an independent worker and a problem solver. Previous experience in audio recording is meritorious."}]}]
    host = get_or_create_role(name='Host', description='', parent_role=None)
    for area in hosts_areas:
        for role in area['roles']:
            get_or_create_role(role['name'], role['description'], host)

def create_project_group():
    create_armada_year(2016)
    create_programmes()
    create_armada_hosts()
    assign_groups_to_all_users()