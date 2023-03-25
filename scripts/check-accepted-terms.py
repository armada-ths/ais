from exhibitors.models import Exhibitor
from fair.models import Fair

accepted_terms_exhibitor = Exhibitor.objects.filter(
    accept_terms=True, fair=Fair.objects.get(current=True)
)
for a in accepted_terms_exhibitor:
    a.status = "complete_registration_terms"
    a.save()
