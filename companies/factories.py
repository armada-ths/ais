import factory

from .models import Company


class CompanyFactory(factory.DjangoModelFactory):
    name = factory.Faker("name")
    organisation_number = "ABC"
    website = "https://armada.nu"
    phone_number = "0707777777"

    class Meta:
        model = Company
