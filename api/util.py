import csv
from django.http import HttpResponse
from collections import OrderedDict


def json_to_csv_response(file_name: str, data: list[OrderedDict]):
    response = HttpResponse(
        content_type="text/csv",
    )
    response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_name
    writer = csv.writer(response)

    for i, item in enumerate(data):
        # Write header
        if i == 0:
            writer.writerow(item.keys())

        writer.writerow(item.values())

    return response
