'''
A script that makes sure no ExhibitorView has invalid fields (if you deleted any in Exhibitor model).

Should be excecuted automatically after git push.
'''
from exhibitors.models import Exhibitor, ExhibitorView

valid_fields = [field.name for field in Exhibitor._meta.get_fields()]
for view in ExhibitorView.objects.all():
    choices = view.choices.split(' ')
    updated = False
    for field in choices:
        if field not in valid_fields:
            print('Found invalid field: ' + field)
            choices -= field
            updated = True
    
    if updated:
        str_choices = ''
        for field in choices:
            str_choices += ' ' + field
        view.choices = str_choices
        view.save()
