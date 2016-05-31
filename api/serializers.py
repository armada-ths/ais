from collections import OrderedDict

def company_serializer(company):
    return OrderedDict({'id': company.pk,
            'name': company.name,
    })

def event_serializer(event):
    return OrderedDict({'id': event.pk,
            'name': event.name,
    })
