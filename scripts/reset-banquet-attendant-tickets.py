# If you get ValueError (invalied literal for int() with base 10) use this script!
# Will go through every BanquetAttendant and reset the ticket_type to None, to avoid problems with old data
# python manage.py shell < ./scripts/reset-banquet-attendant-tickets.py --settings local_settings

from banquet.models import BanquetteAttendant

for attendant in BanquetteAttendant.objects.all():
    attendant.ticket_type = None
    attendant.save()
