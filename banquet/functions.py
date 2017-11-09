from .models import BanquetteAttendant as BanquetAttendant, BanquetTable


def get_table(table_number):
        (table, was_created) = BanquetTable.objects.get_or_create(pk=table_number)
        if was_created:
            table.table_name = 'Table ' + str(table_number)
            table.number_of_seats = 8
            table.save()
        return table


def sit_attendants():
    '''
    A helper function that sits down BanquetAttendants at Tables (no optimisation right now)
    '''
    table_number = 1
    attendants_at_table = 0
    table = get_table(table_number)
    for attendant in BanquetAttendant.objects.all():
        if attendant.confirmed:
            attendants_at_table += 1
            if attendants_at_table > table.number_of_seats:
                table_number += 1
                table = get_table(table_number)
                attendants_at_table = 1
            attendant.table = table
            attendant.seat_number = attendants_at_table
            attendant.save()
