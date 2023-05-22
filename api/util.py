import csv
from django.http import HttpResponse
from collections import OrderedDict


def json_to_csv_response(file_name: str, data: list[OrderedDict]):
    # Add all unique header items to a set
    # in order to output in the right order
    headers = set()
    for item in data:
        for column in item.keys():
            headers.add(column)

    response = HttpResponse(
        content_type="text/csv",
    )
    response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_name
    writer = csv.writer(response)

    writer.writerow(list(headers))

    for item in data:
        writer.writerow([item.get(header) for header in headers])

    return response
