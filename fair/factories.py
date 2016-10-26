import factory

from .models import Fair


class FairFactory(factory.DjangoModelFactory):
    name = "Armada 2000"

    class Meta:
        model = Fair
