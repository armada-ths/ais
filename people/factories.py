import factory

from .models import Profile
from .models import Programme


class ProfileFactory(factory.DjangoModelFactory):
    name = factory.faker('name')
    year = 2016
    user = -1
    programme = factory.subFactory(ProgrammeFactory)

    class Meta:
        model = Profile


class ProgrammeFactory(factory.DjangoModelFactory):
    name = "Computer Science and Engineering (M.Sc)"

    class Meta:
        model = Programme
